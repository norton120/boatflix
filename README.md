# Boatflix

![screen grab of home page](/webapp/assets/screen_grab.png)

Boatflix is a complete media management stack designed for remote/disconnected life (like on a boat). It consists of:
- Media aquisition and management stack of [Servarr](https://wiki.servarr.com/) projects and all the required support services
- Media player stack ([Jellyfin](https://jellyfin.org/) for movies, TV, music and [Calibre](https://calibre-ebook.com/) for books)
- Network managers such as the VPN, Wireless AP, and PiHole ad blocker

## Why?
Living on an intentionally remote setup such as a sailboat is often about a measure of independence. Internet can be unavailable or unreasonable (Starlink/PepLink hardware is prohibitively power hungry for casual movie watching at anchor). 

There is also something very satisfying about cutting that perpetual online tether, silencing the relentless stream of connection and allowing yourself some solitude; if you have to reconnect every time you want to watch a movie, risk getting a barage of emails just to play a few songs on Spotify... it can ruin your moment of freedom. That is why Boatflix exists! An onboard, offline archive of media - music, movies, TV, and books - that you can enjoy while totally disconnected from the rest of the world.


## Motivation
I built the first iteration of Boatflix for all the reasons stated above. My longterm goal for Boatflix is to publish a suggested hardware list, matching pre-baked iso image, and a simple instruction manual so users can plug-and-play a complete media stack for their vessel with just a few steps.

## Notable decisions thus far

- Boatflix is designed for content to be consumed on a designated AP (ie the `boatflix` wifi network) that Boatflix itself provides. This allows a user to power down all other wifi/network hardware and still use Boatflix to watch/listen/read. If you have a power-hungry 5g/Starlink router for normal workday internet, you need none of that for playback.

- Boatflix requires a VPN tunnel to reach out to the internet and get content. Boats can be anywhere in the world, and laws/rules about what content you can and cannot download vary wildly, so it is just safest to tunnel everything. That way you don't find yourself arrested off the coast of Iran for downloading cat videos.

> [!WARNING]
> **Yes**, you _could_ potentially use Boatflix to download copywritten content illegally from torrent websites, but we all know you'd never do that because you are a good, upstanding citizen. As a reminder, always be careful not to download content if it is illegal where you are (or plan to be in the future). Keep your physical media copies safe somewhere back on land as proof that you have a legal right to the stuff you put on your Boatflix. Otherwise, stick to content that is available freely (such as content in the public domain, public with open licenses etc).

- Boatflix expects a hardwired connection to the internet to download content. This was a choice to simplify setup and maintenence, assuming most people will have some kind of router onboard, and it is less confusing than setting up a wifi connection AND a wifi access point. If people really want a wireless option instead it would be pretty easy to add to the setup page, file an issue.

## WIP elements
- [ ] A startup script to run the new `host_manager.py` as a daemon looping.
- [ ] Update boatflix.service, paths, and add boatflix.service to systemd on install.
- [ ] `Update` in the GUI which executes some form of git pull. ? how will we deal with docker compose overwrites ? maybe
  `git update-index --assume-unchanged` on the compose file once installed? yeah that could be messy but programming is hard sometimes.
- [ ] The mounting of the hdd needs to be tested and completed on a Pi, container dev doesn't cut it (no comperable `/dev/sda1` etc).
- [ ] All the XML updates to the `arr` services that need to be correctly pointed to prowlarr and bazarr. At the momment this is done manually and that's a pain and unnessesary.
- [ ] PiHole has had zero config and testing.
- [ ] All the `arr` services should be moved inside the VPN for safety.
- [ ] Docker volume mounts are likely not in the right place anymore.
- [ ] Service logs: these will have similar naming patterns, and since we are keeping them really small just read_text and dump them into a log page in the GUI.

## Helpful Things

- ssh into the box with `boatflix@boatflix.local`. password is `boatflix`
- the admin user/passwords for all things are always `boatflix`:`boatflix`. Use your LAN settings for security not the software, this is intended as a LAN only stack.
- to debug the `boatflix.service` (service file that runs on start) use the command `journalctl -e -u boatflix.service` - this prints out logs for the service.
- currently, updates to the `boatflix.service` file must be manually copied vi `sudo cp /home/boatflix/boatflix/stackarr/boatflix.service /etc/systemd/system/` - this needs to be corrected.

## Hopes and Dreams
- A jukebox on-device client that can be remote controlled either via webapp or hardware interface. This would allow the Boatflix box to be hooked directly into the ship sound system and play music inside or on-deck as desired, going server -> speakers without having to go server -> client -> cast to receiver -> speakers :vomit:.
- A polished Calbire "library" experience with hardware. Ideally each Kindle owner can plug into a dedicated USB port somewhere and sync a managed personal library with that device automatically.
- Really, really good docs.


<a href="https://buymeacoffee.com/ethanknox" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
