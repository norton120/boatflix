# STACKARR
a total stack for the boatflix project. Movies, Music, TV, and Books all
locally sourced and easy to add via torrents/usenets.

**NOTE: It'll take about 5 minutes for all the services to come alive when you reboot the pi. Speed to startup is not a priority here ;)**

## What works
- compose up starts all the services at the respective locations

- boatflix.local gets you an index

*In systemd via boatflix.service*

- mounting whatever is in `/dev/sda1` to `/mnt` (so make sure that's the data HD) via systemd on startup

- starting the docker compose via systemd on startup

## What doesn't work
- creating the simlink between `/mnt` and `/data/media` if it does not already exist (did it once manually didn't bother automating)

- routing between containers inside the VPN by DNS - they cannot see container names or boatflix.local, they need the hardcoded IP at the moment (it's likely a wireguard issue). Everything is hardcoded to 192.168.50.51 (a peplink IP from the default CIDR, so you can hardcode that in your peplink).

- startup disk mount just passes (`||true`) right now but should really be smarter than this


## Helpful Things

- ssh into the box with `boatflix@boatflix.local`. password is `boatflix`
- the admin user/passwords for all things are always `boatflix`:`boatflix`. Use your LAN settings for security not the software, this is intended as a LAN only stack.
- to debug the `boatflix.service` (service file that runs on start) use the command `journalctl -e -u boatflix.service` - this prints out logs for the service.
- updates to the `boatflix.service` file must be manually copied vi `sudo cp /home/boatflix/boatflix/stackarr/boatflix.service /etc/systemd/system/`
