import json
from typing import Optional
import httpx
from pathlib import Path
import yaml


class Envar:
    def __init__(self, valuestring):
        self.name, self.value = valuestring.split("=")

    def __repr__(self) -> str:
        return f"{self.name}={self.value}"

class Service:
    def __init__(self, name:str, raw_service:dict):
        self.raw_service = raw_service
        self.name = name
        self.image, self.image_tag = self.raw_service["image"].split(":")
        self.description = self.raw_service["labels"][f"boatflix.{self.name}.description"]
        self.envars = [Envar(val) for val in self.raw_service.get("environment", {})]
        self._image_tag_options = None

    def __repr__(self) -> str:
        return self.name

    @property
    def link(self) -> Optional[str]:
        """Get the service URL based on the first port mapping"""
        ports = self.raw_service.get("ports", [])
        if not ports:
            return None
        # Port mapping format is "host_port:container_port"
        host_port = ports[0].split(":")[0]
        return f"http://localhost:{host_port}"

    @property
    def image_tag_options(self) -> list[str]:
        if self._image_tag_options is None:
            repo = self.image if "/" in self.image else f"library/{self.image}"
            response = httpx.get(f"https://hub.docker.com/v2/repositories/{repo}/tags")
            if not response.is_success:
                self._image_tag_options = []
            try:
                self._image_tag_options = [tag["name"] for tag in response.json()["results"]]
            except KeyError:
                self._image_tag_options = []
        return self._image_tag_options

    def update(self) -> dict:
        """updates the service dict to match the state"""
        self.raw_service["image"] = f"{self.image}:{self.image_tag}"
        return self.raw_service

    def get_envar(self, name:str)-> Envar:
        try:
            return next((e for e in self.envars if e.name == name))
        except StopIteration:
            raise ValueError(f"Envar {name} not found")


class Compose:
    def __init__(self):
        self.path = Path("/app/docker-compose.yml")
        self.raw_compose = yaml.safe_load(self.path.read_text())
        self.services = [Service(k,v) for k,v in self.raw_compose["services"].items()]

    def get_service(self, name:str)-> Service:
        try:
            return next((s for s in self.services if s.name == name))
        except StopIteration:
            raise ValueError(f"Service {name} not found")


    def render(self) -> None:
        """renders the compose file to match the state"""
        for service in self.services:
            service.update()
            self.raw_compose["services"][service.name] = service.raw_service
        self.path.write_text(yaml.dump(self.raw_compose))


class Config:
    def __init__(self):
        self.path = Path("/app/webapp/configuration.json")
        self.raw_config = json.loads(self.path.read_text())

    def get_config(self, name:str)-> dict:
        return self.raw_config[name]

    def render(self):
        self.path.write_text(json.dumps(self.raw_config, indent=4))
