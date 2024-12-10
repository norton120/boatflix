import socket
import httpx
import streamlit as st
from streamlit_themes import set_preset_theme
from streamlit_card import card as st_card
from dotenv import dotenv_values, set_key


SERVICES = [
    "webapp",
    "jellyfin",
    "jellyseer",
    "prowlarr",
    "flaresolverr",
    "qbittorrent",
    "lidarr",
    "radarr",
    "readarr",
    "calibre",
    "sonarr",
    "bazarr",
    "gluetun",
    "raspap"
]

set_preset_theme("Beach")


st.title("Boatflix")


class Envars:

    def __init__(self):
        self.path = ".env"
        self.values = dotenv_values(self.path)

    def set_key(self, key, value):
        set_key(self.path, key, value)

    def get_key(self, key):
        return self.values.get(key)

envars = Envars()

def draw_pia():
    with st.container(border=1):
        st.write("**PIA Credentials**")
        username = st.text_input("PIA Username", key="PIA_USER", help="Enter your PIA username", value=envars.get_key("PIA_USER"))
        password = st.text_input("PIA Password", type="password", key="PIA_PASS", help="Enter your PIA password", value=envars.get_key("PIA_PASS"))
        if st.button("Save Credentials"):
            response = httpx.post('https://www.privateinternetaccess.com/api/client/v2/token', data={
                "username": username,
                "password": password
            })
            try:
                _ = response.json()["token"]
                envars.set_key("PIA_USER", username)
                envars.set_key("PIA_PASS", password)
                envars.set_key("DOCKER_PROFILE", "running")
                st.success("Credentials saved")
            except (KeyError, IndexError):
                st.error("Invalid credentials")



if not (envars.get_key("PIA_USER") and envars.get_key("PIA_PASS")):
    st.write("Boatflix requires a [PIA](https://www.privateinternetaccess.com/) account to run.")
    envars.set_key("DOCKER_PROFILE", "setup")
    draw_pia()

# set envars

# check if envars are set to start other containers

# links to apps
if envars.get_key("DOCKER_PROFILE") == "running":
    for row in range(0, len(SERVICES), 2):
        cols = st.columns(2, gap="small")
        for index, service in enumerate(SERVICES[row:row+2]):
            with cols[index]:
                st_card(title=service,
                        text="thing",
                        image="http://placekitten.com/200/300",
                        url="http://localhost:8080",
                        styles={
        "card": {
            "height": "auto",
            "width": "auto",
            "min-width": "100%",
            "min-height": "200px",
            "border-radius": "1rem",
            "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
        },
        "text": {
            "font-family": "serif",
        }
    }
                        )

    st.write("### Settings")

    draw_pia()

    # get local ip
    local_ip_address = socket.gethostbyname(socket.gethostname())
    st.toggle("Use .local",
            help="When set, boatflix will use .local domain names for services instead of IP:port",
            key="USE_LOCAL")




    with st.expander("Advanced"):
        with st.container(border=1):
            st.write("**Container Versions**")
            st.write("You can specify container versions explicitly. If you don't specify a version, the latest version will be used.")

            def set_version(key):
                envars.set_key(key, st.session_state[key])

            for service in SERVICES:
                key = f"{service.upper()}_VERSION"
                version = st.text_input(service,
                                        placeholder="latest",
                                        key=key,
                                        value=envars.get_key(key),
                                        on_change=set_version,
                                        args=(key,))