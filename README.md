
## What works
- compose up starts all the services at the respective locations
- boatflix.local gets you an index

## What doesn't work
- mounting the HD (`/dev/sda1` to `/mnt` assuming there's only 1 disk) on startup
- creating the simlink between `/mnt` and `/data/media` if it does not already exist
- starting the compose once the mount has been created
- routing between containers inside the VPN by DNS - they cannot see container names or boatflix.local, they need the hardcoded IP at the moment (it's likely a wireguard issue)
- startup disk mount just passes (`||true`) right now but should really be smarter than this


## Helpful Things

- ssh into the box with `boatflix@boatflix.local`. password is `boatflix`
- the admin user/passwords for all things are always `boatflix`:`boatflix`. Use your LAN settings for security not the software, this is intended as a LAN only stack.
- to debug the `boatflix.service` (service file that runs on start) use the command `journalctl -e -u boatflix.service` - this prints out logs for the service.
- updates to the `boatflix.service` file must be manually copied vi `sudo cp /home/boatflix/boatflix/stackarr/boatflix.service /etc/systemd/system/`
