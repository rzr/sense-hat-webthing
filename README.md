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

From "Settings" add-on menu:

- Add "and enable add-on
- Then add "SenseHat" from the things dashboard.

## DEVELOP ##

```sh
# From Settings / Developer / Enable SSH
# https://sensehat.mozilla-iot.org/settings/developer
ssh pi@gateway.local # password=raspberry
sudo systemctl stop mozilla-iot-gateway
rm -rf ~/.mozilla-iot/addons/sense-hat-*
cd ~/.mozilla-iot/addons/
sudo apt-get remove -y \
  libblas3 libgfortran5 libimagequant0 liblapack3 liblcms2-2 librtimulib-utils \
  librtimulib7 libwebpdemux2 \
  python3-numpy python3-olefile python3-pil  python3-rtimulib python3-sense-hat
git clone https://github.com/rzr/sense-hat-webthing sense-hat-adapter
cd sense-hat-adapter
./setup.sh
python3 main.py
sudo systemctl restart mozilla-iot-gateway
sudo journalctl -f -xu mozilla-iot-gateway.service
```

From "/things" webpage "SenseHat" can be added (+, Add, Done)

Note that instead of restarting gateway,
from Web UI, any addon can disabled and enabled again.

## EXTRA: EXAMPLE ##

An extra example can be also used as standone webthing server:

```sh
cd example
pip3 install webthing
python sense-hat-single-thing.py
```

## MORE ##

For reference the following items are supported:

- <https://www.st.com/resource/en/datasheet/hts221.pdf>
- <https://www.st.com/resource/en/datasheet/lps25hb.pdf>
- <https://www.st.com/resource/en/datasheet/lsm9ds1.pdf>

Thanks to Geof Cohler (@gcohler) for support.

## RESOURCES ##

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
- <https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat>
- <https://iot.mozilla.org/schemas/>
- <https://github.com/mozilla-iot/webthing-python/>
- <https://github.com/mozilla-iot/tplink-adapter>
- <https://github.com/mozilla-iot/eufy-adapter>
