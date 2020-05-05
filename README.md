# SENSE-HAT WEBTHING #

[![GitHub forks](
https://img.shields.io/github/forks/rzr/sense-hat-webthing.svg?style=social&label=Fork&maxAge=2592000
)](
https://GitHub.com/rzr/sense-hat-webthing
)
![Mastodon Follow](
https://img.shields.io/mastodon/follow/279303?domain=https%3A%2F%2Fmastodon.social&style=social
)

## ABOUT ##

Addon adapter for Mozilla IoT Gateway 
using python module to handle I2C sensors and GPIOs
of Raspberry Pi's extension board "SenseHat".

[![sense-hat-webthing](
https://repository-images.githubusercontent.com/259962704/f411a980-8aea-11ea-94f4-aad36c651769#./file/sense-hat-webthing.jpg
)](
https://mastodon.social/@rzr/104052909544715058#LavalVirtual2020
"sense-hat-webthing")

## USAGE ##

From add-on menu:

- Add and enable add-on
- Wait the time that dependencies are downloaded and setup
  (ssh to look for "python3 -m pip install")
- Then add "SenseHat" from the things dashboard.

## DEVELOP ##

```sh
# From Settings / Developer / Enable SSH
# https://sensehat.mozilla-iot.org/settings/developer
ssh pi@gateway.local # password=raspberry
sudo systemctl stop mozilla-iot-gateway
rm -rf ~/.mozilla-iot/addons/sense-hat-*
cd ~/.mozilla-iot/addons/
git clone --depth 1  https://github.com/rzr/sense-hat-webthing sense-hat-adapter
sudo systemctl restart mozilla-iot-gateway
sudo journalctl -f -xu mozilla-iot-gateway.service
# From UI / Enable Addon
#| (...)
#| May 05 16:51:33 gateway run-app.sh[2496]: 2020-05-05 16:51:33.347 INFO   : sense-hat-adapter: The following NEW packages will be installed:
#| May 05 16:51:33 gateway run-app.sh[2496]: 2020-05-05 16:51:33.351 INFO   : sense-hat-adapter:   libblas3 libgfortran5 libimagequant0 liblapack3 liblcms2-2 librtimulib-utils
#| May 05 16:51:33 gateway run-app.sh[2496]: 2020-05-05 16:51:33.356 INFO   : sense-hat-adapter:   librtimulib7 libwebpdemux2 python3-numpy python3-olefile python3-pil
#| May 05 16:51:33 gateway run-app.sh[2496]: 2020-05-05 16:51:33.359 INFO   : sense-hat-adapter:   python3-rtimulib python3-sense-hat
#| (...)
```

Note that instead of restarting gateway,
from Web UI, any addon can disabled and enabled again.

## MORE ##

For reference the following items are supported:

- <https://www.st.com/resource/en/datasheet/hts221.pdf>
- <https://www.st.com/resource/en/datasheet/lps25hb.pdf>
- <https://www.st.com/resource/en/datasheet/lsm9ds1.pdf>

Thanks to Geof Cohler (@gcohler) for support.

## RESOURCES ##

- <https://mastodon.social/@rzr/104052909544715058#LavalVirtual2020>
- <https://discourse.mozilla.org/t/is-there-an-add-on-for-pi-sense-hat/58024/5>
- <https://github.com/rzr/mozilla-iot-generic-sensors-adapter/issues/13>
- <https://github.com/mozilla-iot/wiki/wiki#general-1>
- <https://github.com/mozilla-iot/gateway-addon-python>
- <https://hacks.mozilla.org/2018/02/creating-an-add-on-for-the-project-things-gateway/>
- <https://www.raspberrypi.org/products/sense-hat/>
- <https://www.raspberrypi.org/documentation/hardware/sense-hat/>
- <https://github.com/astro-pi/python-sense-hat>
- <https://pythonhosted.org/sense-hat/api/>
- <https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat>
- <https://github.com/mozilla-iot/tplink-adapter>
- <https://github.com/mozilla-iot/eufy-adapter>
