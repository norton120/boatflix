
## What works
- compose up starts all the services at the respective locations
- boatflix.local gets you an index

## What doesn't work
- mounting the HD (`/dev/sda1` to `/mnt` assuming there's only 1 disk) on startup
- creating the simlink between `/mnt` and `/data/media` if it does not already exist
- starting the compose once the mount has been created
- routing between containers inside the VPN by DNS - they cannot see container names or boatflix.local, they need the hardcoded IP at the moment (it's likely a wireguard issue)
- startup disk mount just passes (`||true`) right now but should really be smarter than this