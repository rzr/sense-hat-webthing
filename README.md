# SENSE-HAT WEBTHING #

[![GitHub forks](
https://img.shields.io/github/forks/rzr/sense-hat-webthing.svg?style=social&label=Fork&maxAge=2592000
)](
https://GitHub.com/rzr/sense-hat-webthing
)
[![PyPi](
https://img.shields.io/pypi/v/sense-hat-webthing.svg
)](
https://pypi.org/project/sense-hat-webthing/
)
[![Legal](
https://img.shields.io/badge/license-MPL--2.0-blue.svg
)](
https://github.com/rzr/sense-hat-webthing/blob/master/LICENSE
)
![Mastodon Follow](
https://img.shields.io/mastodon/follow/279303?domain=https%3A%2F%2Fmastodon.social&style=social
)

## ABOUT ##

Addon adapter for Mozilla IoT Gateway 
using python module to handle I2C sensors and GPIOs
of Raspberry Pi's extension board "SenseHat".

[![sense-hat-webthing](
https://repository-images.githubusercontent.com/259962704/e9f36600-92b5-11ea-9df7-c3e38c5af4dd#./file/sense-hat-adapter-0.0.5.png
)](
https://mastodon.social/@rzr/104143644945748115#:sensehat:
"sense-hat-webthing")

## USAGE ##

### PREREQUISITES ###

Install mozilla WebThing gateway on RaspberryPI (It was made for 
https://github.com/mozilla-iot/gateway/releases/download/0.12.0/gateway-0.12.0.img.zip
)

- Connect to device's wifi "WebThings Gateway FFFF" and then open http://gateway.local/,  Setup WiFi Setup
- Connect back to LAN Wifi open http://gateway.local/things again

### INSTALL ###

From "Settings" add-on menu:

- Add "and enable add-on
- Then add "SenseHat" from the things dashboard.

### CALIBRATE ###

For using Inertial measurement unit (IMU sensors),
calibration will help to get more accurate measurements.

```sh
sudo apt-get install librtimulib-utils

cd ~/.config/sense_hat/
mv -f RTIMULib.ini RTIMULib.ini.orig
RTIMULibCal

#| RTIMULibCal - using RTIMULib.ini
#| Settings file not found. Using defaults and creating settings file
#| Detected LSM9DS1 at standard/standard address
#| Using fusion algorithm RTQF
#| min/max compass calibration not in use
#| Ellipsoid compass calibration not in use
#| Accel calibration not in use
#| LSM9DS1 init complete
#| Options are: 
#| m - calibrate magnetometer with min/max
#| e - calibrate magnetometer with ellipsoid (do min/max first)
#| a - calibrate accelerometers
#| (...)

grep '=' RTIMULib.ini
```

If done correctly north should be indicated by edge where power LED is located
the compass value is actually the "yaw" value, while "pitch" is around this same edge.
Remaining "roll" value can be changed by rotating on longest middle axis of board.


### AUTOMATE ###

Once added in gateway, it can be used along the rule engine:

[![sense-hat-webthing](
https://files.mastodon.social/media_attachments/files/028/864/302/original/65d944b18b347d04.png
)](
https://mastodon.social/@rzr/104052909544715058#LavalVirtual2020
"sense-hat-webthing")


## DEVELOP ##

```sh
# From Settings / Developer / Enable SSH
# https://sensehat.mozilla-iot.org/settings/developer
ssh pi@gateway.local # password=raspberry
sudo systemctl stop mozilla-iot-gateway
rm -rf ~/.mozilla-iot/addons/sense-hat-*
cd ~/.mozilla-iot/addons/
git clone https://github.com/rzr/sense-hat-webthing sense-hat-adapter
make -C sense-hat-adapter help prep start # unprep # to restore
sudo systemctl restart mozilla-iot-gateway
sudo journalctl -f -xu mozilla-iot-gateway.service
```

From "/things" webpage "SenseHat" can be added (+, Add, Done)

Note that instead of restarting gateway,
from Web UI, any addon can disabled and enabled again.

## EXTRA: EXAMPLES ##

More examples can be also used as standone webthing server:

```sh
cd example
# If on debian, it will be faster:
sudo apt-get install python3-sense-hat 
pip3 install webthing 
# Or if not on debian:
# pip3 install -r requirements.txt 
./sense-hat-single-thing.py
```

Then add thing using "URL" adapter it should be discovered as (http://localhost:8888)

Same procedure for other exampl, like multiple things which is handling orientation sensor.

## MORE ##

For reference the following items are supported:

- <https://www.st.com/resource/en/datasheet/hts221.pdf>
- <https://www.st.com/resource/en/datasheet/lps25hb.pdf>
- <https://www.st.com/resource/en/datasheet/lsm9ds1.pdf>

Thanks to Geof Cohler (@gcohler) for support.

## RESOURCES ##

- <https://libraries.io/pypi/sense-hat-webthing>
- <https://pypi.org/project/sense-hat-webthing/>
- <https://mastodon.social/@rzr/104052909544715058#LavalVirtual2020>
- <https://github.com/mozilla-iot/addon-list/pull/822>
- <https://discourse.mozilla.org/t/is-there-an-add-on-for-pi-sense-hat/58024/5>
- <https://www.openhub.net/p/sense-hat-webthing>
- <https://github.com/rzr/mozilla-iot-generic-sensors-adapter/issues/13>
- <https://github.com/mozilla-iot/wiki/wiki#general-1>
- <https://github.com/mozilla-iot/gateway-addon-python>
- <https://hacks.mozilla.org/2018/02/creating-an-add-on-for-the-project-things-gateway/>
- <https://libraries.io/pypi/sense-hat>
- <https://www.raspberrypi.org/products/sense-hat/>
- <https://www.raspberrypi.org/documentation/hardware/sense-hat/>
- <https://github.com/astro-pi/python-sense-hat>
- <https://pythonhosted.org/sense-hat/api/>
- <https://github.com/raspberrypi/rpi-sense/>
- <https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat>
- <https://iot.mozilla.org/schemas/>
- <https://github.com/mozilla-iot/webthing-python/>
- <https://github.com/mozilla-iot/tplink-adapter>
- <https://github.com/mozilla-iot/eufy-adapter>

[![sense-hat-webthing](
https://files.mastodon.social/media_attachments/files/027/879/770/small/2711ddf5ac31f8bf.jpeg#./file/sense-hat-webthing.jpg
)](
https://mastodon.social/@rzr/104052909544715058#LavalVirtual2020
"sense-hat-webthing")
