import datetime
import json
from pathlib import Path
import subprocess

class HostManager:
    """There are various tasks that Boatflix needs to do on the host. This is the send/receive interface for those tasks."""
    ROOT_MOUNT_POINT = "/mnt"
    CONFIG_FILE = "/boatflix/webapp/configuration.json"

    def __init__(self):
        self.config_file = Path(self.CONFIG_FILE)
        self.config = json.load(self.config_file.read_text())


    def persist_config(self):
        """Persist the config to the config file."""
        self.config_file.write_text(json.dumps(self.config, indent=4))

    # get usb hard drive mount options
    def get_drive_options(self) -> None:
        """Get the mountable options for the usb hard drive."""

        raw_devices = subprocess.check_output(["blkid", "/dev/sd*"]).decode("utf-8")
        devices = raw_devices.split("\n")
        # parse the responses from blkid into mount_point, type, label, and UUID
        mount_options = []
        # TODO: need a way to test this and get the right device list
        for device in devices:
            if device:
                mount_point, type, label, uuid = device.split()
                mount_options.append = {
                    "mount_point": mount_point,
                    "type": type,
                    "label": label,
                    "uuid": uuid
                }
        self.config["hard_drive"]["drive_options"] = mount_options
        self.persist_config()

    # mount the usb hard drive
    def mount_drive(self):
        """Mount the usb hard drive."""
        selected_drive_device = self.config["hard_drive"]["selected_drive_device"]
        if not selected_drive_device:
            raise ValueError("No drive device selected")
        subprocess.check_call(["mount", selected_drive_device, self.ROOT_MOUNT_POINT])
        subprocess.check_call(["chmod", "777", self.ROOT_MOUNT_POINT])
        subprocess.check_call(["systemctl", "daemon-reload"])

    @property
    def state_is_stale(self):
        """Check if the compose has been updated since the last restart."""
        # get timestamp of compose file
        compose_file = Path("/boatflix/docker-compose.yml")
        restarted_at = self.config["status"]["restarted_at"] or 0
        return compose_file.stat().st_mtime.timestamp() > restarted_at

    def restart_docker_compose(self):
        profile = 'running' if self.config["status"]["startup_complete"] else 'startup'
        subprocess.run(["docker","compose", "--profile", profile, "down"])
        self.config["status"]["restarted_at"] = datetime.now().timestamp()
        self.persist_config()
        if self.state_is_stale:
            subprocess.run(["docker","compose", "--profile", "running", "build", "--no-cache"]) # always rebuild the whole thing via running
        subprocess.run(["docker","compose", "--profile", profile, "up", "-d"])

    def update_arr_configs(self):
        """Update the xml config files of all the arr services to use the correct url for prowlarr, flaresolverr, etc
        otherwise this has to be manually done in the GUI :vomit:
        """
        pass
