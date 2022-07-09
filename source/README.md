# xonox
An alternative infrastructure-service for legacy NOXON(tm) devices.

## Compatible Devices
The following devices were reported as compatible:
* Noxon(tm) iRadio
* Noxon(tm) iRadio 300/360
* Noxon(tm) iRadio 400

## Getting Started
### Installation
Install the module and all of its dependencies via pip:
```
pip install xonox
```

### Start Service
If you want `xonox` to listen on all bound IP-addresses:
```
python -m xonox
```
If you want `xonox` to listen only on a single IP-address you can use the `--host` parameter to specify it.
```
python -m xonox --host 192.168.3.3
```

### Configure Your Environment
The NOXON(tm) devices locate their services via DNS. To allow them to find the alternative service, you need to configure your local DNS so that the following names point to the host that runs `xonox`.
- legacy.noxonserver.eu
- gate1.noxonserver.eu

## Manage Your Station List
#### Add Stations
You can add stations to `xonox` by POSTing its metadata to the `/station` endpoint.
```
curl --location --request POST 'http://legacy.noxonserver.eu/station' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Radio Swiss Pop",
    "description": "Radio Swiss Pop Live Stream",
    "streamUrl": "http://stream.srg-ssr.ch/m/rsp/mp3_128"
}'
```
Please note that `streamUrl` needs to point to the MP3 stream and not to a playlist (M3U). If you don't know how to get this information for your favorite station, have a look at station list of the [RadioBrowser](https://www.radio-browser.info/) project.
Remember that the Noxon(tm) iRadios do not support HTTPS. Therefore you need to __supply an HTTP-URL__.

#### Get the List
```
curl --location --request GET 'http://legacy.noxonserver.eu/station'
```

#### Remove a Station
```
curl --location --request DELETE 'http://legacy.noxonserver.eu/station/0'
```

## Configuration File
By default, `xonox` writes its configuration and station-list to a file called `xonox.conf` inside the user's home directory. If this causes problems on your system, you can specify the storage directory using the `--config-dir` parameter.

## Changelog
### 0.0.7 (Work in Progress)
- [Added support for preset-buttons](https://github.com/x789/xonox/issues/9)
- [Order stations alphabetically](https://github.com/x789/xonox/issues/10)

### 0.0.6
- Fixed [Management API does not return JSON](https://github.com/x789/xonox/issues/4)
- Fixed [Non-unique station-IDs](https://github.com/x789/xonox/issues/3)

### 0.0.5
- __BREAKING CHANGE__ If the service shall bound to a specific ip-address, it must be provided via `--host` and not the positional parameter like in previous versions.
- Added possibility to configure the location of `xonox.config` via command-line parameter `--config-dir`.
- Fixed 'config not found'

### 0.0.4 (Withdrawn)
- Added persistence of the station list.

### 0.0.3
- First publicly available release

(c) 2022 TillW - Licensed to you under the AGPL v3.0