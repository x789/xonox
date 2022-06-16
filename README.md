# XONOX
An alternative service for legacy NOXON(tm) devices.

## Getting Started
### Installation
Install the module and all of its dependencies via pip:
```
pip install xonox
```

### Start Service
Run the service:
```
python -m xonox
```

### Configure Environment
The NOXON(tm) devices locate their services via DNS. To allow them to find the alternative service, you need to configure your local DNS so that the following names point to the host that runs `xonox`.
- legacy.noxonserver.eu
- gate1.noxonserver.eu

### Add Stations to the Station List
You can add stations to `xonox` by POSTing its metadata to the `/station` endpoint.
```
curl --location --request POST 'http://192.168.15.129/station' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Radio Swiss Pop",
    "description": "Radio Swiss Pop Live Stream",
    "streamUrl": "http://stream.srg-ssr.ch/m/rsp/mp3_128"
}'
```
Please note that `streamUrl` needs to point to the MP3 stream and not to a playlist (M3U). If you don't know how to get this information for your favorite station, have a look at the [RadioBrowser](https://www.radio-browser.info/) project.

__For now, added stations are not stored permanently. They get lost when `xonox` is restarted. This will be fixed in the future (see roadmap below).__

## Missing Features
`xonox` is far way from completeness. These things are missing so far:
- Playlist support
- A GUI to manage the station list
- Store stations permanently
- Support favorites/presets


(c) 2022 TillW - Licensed to you under the AGPL v3.0