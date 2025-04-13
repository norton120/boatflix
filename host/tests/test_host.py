from pytest import mark as m
from pathlib import Path
from host_manager import HostManager


@m.describe("When getting an api key for a service")
@m.context("and the service config exists")
@m.it("is able to get the api key")
def test_service_api_key(tmp_path):
    sonarr = (tmp_path / "sonarr").mkdir(parents=True, exist_ok=True)
    # copy the sample config to the tmp path
    (sonarr / "config.xml").write_text(Path("tests/assets/sample_config.xml").read_text())
    host_manager = HostManager()
    api_key = host_manager.retrieve_arr_api_key("sonarr", tmp_path)
    assert api_key == "be47ce5bb8d846ef9e7fc41f559ee8e5" # see /tests/assets/sample_config.xml