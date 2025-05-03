from typing import Optional, Type
from pathlib import Path
import httpx
import xml.etree.ElementTree as ET
from abc import ABC
import json
from webapp.logger import logger
logger = logger.getChild(__name__)

class ArrApi(ABC):
    """generic api for arr services"""

    service_name: str
    port: int
    version: str = "v3"
    config_path: Optional[Path] = None

    @property
    def api_key(self) -> str:
        """get the api key from the config file"""
        config = self.config_path or Path(f"/configs/{self.service_name}/config.xml")
        parsed = ET.parse(config)
        api_key = parsed.find("ApiKey")
        if api_key is None:
            raise ValueError("ApiKey not found in config")
        return api_key.text

    def disable_auth(self) -> None:
        """disable auth for the service"""
        base_url = f"http://{self.service_name}:{self.port}/api/{self.version}"
        logger.info(f"Disabling auth for {self.service_name} at {base_url}")
        client = httpx.Client(base_url=base_url, headers={"X-Api-Key": self.api_key})
        endpoint = "config/host"
        response = client.get(endpoint)
        if not response.is_success:
            raise Exception(f"Failed to get {self.service_name} config: {response.text} ({response.status_code})")
        payload = response.json()
        payload["AuthenticationMethod"] = "basic"
        payload["AuthenticationRequired"] = "disabledForLocalAddresses"
        payload["Username"] = "boatflix"
        payload["Password"] = "boatflix"
        payload["PasswordConfirmation"] = "boatflix"
        update = client.put(endpoint, json=payload)
        if not update.is_success:
            raise Exception(f"Failed to disable auth for {self.service_name}: {update.text} ({update.status_code})")
        return update.json()

    def prolarr_application_payload(self) -> dict:
        """get the application payload for Prowlarr"""
        title = self.service_name.capitalize()
        return {
            "syncLevel": "fullSync",
            "enable": True,
            "fields": [
                {"name":"prowlarrUrl",
                 "value":"http://prowlarr:9696"
                },
                {"name":"baseUrl",
                 "value":f"http://{self.service_name.lower()}:{self.port}"
                },
                {"name":"apiKey",
                 "value":self.api_key
                },
                {"name":"syncCategories",
                 "value":self.sync_categories
                },
                {"name":"syncRejectBlocklistedTorrentHashesWhileGrabbing",
                 "value":False}
            ],
            "implementationName": title,
            "implementation": title,
            "configContract": f"{title}Settings",
            "infoLink": f"https://wiki.servarr.com/prowlarr/supported#{title}",
            "tags": [],
            "name": self.service_name
        }



class RadarrApi(ArrApi):
    """api for radarr"""

    service_name = "radarr"
    port = 7878
    sync_categories = [2000, 2010, 2020, 2030, 2040, 2045, 2050, 2060, 2070, 2080, 2090]

class SonarrApi(ArrApi):
    """api for sonarr"""

    service_name = "sonarr"
    port = 8989
    sync_categories = [5000, 5010, 5020, 5030, 5040, 5045, 5050, 5090]

class LidarrApi(ArrApi):
    """api for lidarr"""

    version = "v1"
    service_name = "lidarr"
    port = 8686
    sync_categories = [3000,3010,3030,3040,3050,3060]

class ReadarrApi(ArrApi):
    """api for readarr"""

    version = "v1"
    service_name = "readarr"
    port = 8787
    sync_categories = [3030, 7000, 7010, 7020, 7030, 7040, 7050, 7060]


class ProwlarrApi(ArrApi):
    """api for prowlarr"""

    service_name = "prowlarr"
    port = 9696
    version = "v1"

    def create_flaresolverr_tag(self) -> None:
        """create a tag in Prowlarr"""
        client = httpx.Client(base_url=f"http://{self.service_name}:{self.port}/api/{self.version}/", headers={"X-Api-Key": self.api_key})
        response = client.get("tag")
        if not response.is_success:
            raise Exception(f"Failed to get tags for {self.service_name}: {response.text} ({response.status_code})")
        if any(tag["label"] == "flaresolverr" for tag in response.json()):
            logger.info(f"flaresolverr tag already exists for {self.service_name}")
            return
        response = client.post("tag", json={"label": "flaresolverr"})
        if not response.is_success:
            raise Exception(f"Failed to create flaresolverr tag for {self.service_name}: {response.text} ({response.status_code})")
        return response.json()

    def set_indexer_proxy(self) -> None:
        """set indexer proxy in Prowlarr"""
        client = httpx.Client(base_url=f"http://{self.service_name}:{self.port}/api/{self.version}/", headers={"X-Api-Key": self.api_key})
        request = client.get("indexerproxy")
        if not request.is_success:
            raise Exception(f"Failed to get indexers for {self.service_name}: {request.text} ({request.status_code})")
        if request.json():
            logger.info(f"Indexer proxy already set for {self.service_name}")
            return
        payload = json.loads(Path("/app/webapp/assets/indexer_proxy.json").read_text())
        response = client.post("indexerproxy", json=payload)
        if not response.is_success:
            raise Exception(f"Failed to set indexer proxy for {self.service_name}: {response.text} ({response.status_code})")
        return response.json()

    def add_application(self, application: Type[ArrApi]) -> None:
        """add an application to Prowlarr"""
        def is_app(data: dict) -> bool:
            return data["name"].lower() == application.service_name.lower()

        client = httpx.Client(base_url=f"http://{self.service_name}:{self.port}/api/{self.version}/", headers={"X-Api-Key": self.api_key})
        response = client.get("applications")
        if not response.is_success:
            raise Exception(f"Failed to get applications for {self.service_name}: {response.text} ({response.status_code})")
        if any(is_app(app) for app in response.json()):
            logger.info(f"{application.service_name} already exists for {self.service_name}")
            return
        response = client.post("applications", json=application.prolarr_application_payload())
        if not response.is_success:
            raise Exception(f"Failed to add application {application.service_name} for {self.service_name}: {response.text} ({response.status_code})")
        return response.json()

    def set_indexers(self) -> None:
        """set indexer services in Prowlarr"""
        client = httpx.Client(base_url=f"http://{self.service_name}:{self.port}/api/{self.version}/", headers={"X-Api-Key": self.api_key})
        request = client.get("indexer")
        if not request.is_success:
            raise Exception(f"Failed to get indexers for {self.service_name}: {request.text} ({request.status_code})")
        if request.json():
            logger.info(f"Indexers already set for {self.service_name}")
            return
        for indexer in json.loads(Path("/app/webapp/assets/indexers.json").read_text()):
            response = client.post("indexer", json=indexer)
            if not response.is_success:
                raise Exception(f"Failed to set indexer {indexer['name']} for {self.service_name}: {response.text} ({response.status_code})")
            logger.info(f"Indexer {indexer['name']} set for {self.service_name}")
        return


