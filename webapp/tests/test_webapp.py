from pytest import mark as m

from webapp.persist import Compose

@m.describe("When a service instance is created")
@m.context("and it is in the docker registry")
@m.it("is able to get the image tag options")
@m.vcr()
def test_image_tag_options():
    compose = Compose()
    pihole = compose.services[-1]

    assert "latest" in pihole.image_tag_options
    assert "development" in pihole.image_tag_options

@m.describe("When a service instance is created")
@m.context("and it has envars")
@m.it("is able to get the envars")
def test_envars():
    compose = Compose()
    vpn = compose.get_service("vpn")
    assert vpn.get_envar("VPN_SERVICE_PROVIDER").value == "private internet access"



