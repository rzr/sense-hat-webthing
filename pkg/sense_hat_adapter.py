# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MPL-2.0

"""SenseHat adapter for Mozilla WebThings Gateway."""

from sense_hat import SenseHat
from gateway_addon import Adapter, Database, Device, Property

from os import path
import os
import threading
import time

_POLL_INTERVAL = 5


class SenseHatAdapter(Adapter):
    """Adapter for Sense Hat"""

    def __init__(self, verbose=False):
        """
        Initialize the object.

        verbose -- whether or not to enable verbose logging
        """

        self.pairing = False
        self.addon_name = 'sense-hat'
        self.DEBUG = True
        self.name = self.__class__.__name__
        self.URL = 'https://github.com/rzr/sense-hat-webthing'
        Adapter.__init__(self,
                         self.addon_name, self.addon_name, verbose=verbose)

        try:
            device = SenseHatDevice(self)
            self.handle_device_added(device)
            if self.DEBUG:
                print("sense_hat_device created")
            self.devices['sense-hat'].connected = True
            self.devices['sense-hat'].connected_notify(True)

        except Exception as ex:
            print("Could not create sense_hat_device: " + str(ex))


class SenseHatDevice(Device):
    """SenseHat device type."""

    def __init__(self, adapter):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        """

        Device.__init__(self, adapter, 'sense-hat')

        self._id = 'sense-hat'
        self.id = 'sense-hat'
        self.adapter = adapter
        self.controller = SenseHat()
        self.controller.set_imu_config(False, True, False)

        self.name = 'Sense Hat'
        self.name = 'SenseHat'
        self.description = 'Expose SenseHat sensors and actuators'
        self.links = [
            {
                'rel': 'alternate',
                'mediaType': 'text/html',
                'href': adapter.URL
            }
        ]
        self._type = []
        try:
            self.properties['humidity'] = SenseHatProperty(
                self,
                "humidity",
                {
                    '@type': 'NumberProperty',
                    'label': "Humidity",
                    'type': 'integer',
                    'unit': '%',
                    'readOnly': True
                },
                0)
            self.properties['message'] = SenseHatProperty(
                self,
                "message",
                {
                    '@type': 'StringProperty',
                    'label': "Message",
                    'type': 'string'
                },
                "")
            self.properties['pressure'] = SenseHatProperty(
                self,
                "pressure",
                {
                    '@type': 'NumberProperty',
                    'label': "Pressure",
                    'readOnly': True,
                    'type': 'number',
                    'unit': 'hPa'
                },
                0)
            self.properties['temperature'] = SenseHatProperty(
                self,
                "temperature",
                {
                    '@type': 'NumberProperty',
                    'label': "Temperature",
                    'type': 'integer',
                    'unit': 'ºC',
                    'readOnly': True
                },
                0)
            self.properties['color'] = SenseHatProperty(
                self,
                "color",
                {
                    '@type': 'ColorProperty',
                    'label': "Color",
                    'type': 'string',
                    'readOnly': False
                },
                '#ffffff')
            self.properties['compass'] = SenseHatProperty(
                self,
                "compass",
                {
                    '@type': 'NumberProperty',
                    'label': "Compass",
                    'type': 'integer',
                    'description': 'Angle to North ',
                    'unit': 'º',
                    'minimum': 0,
                    'maximum': 360,
                    'readOnly': True
                },
                0)

            t = threading.Thread(target=self.poll)
            t.daemon = True
            t.start()
            self.pairing = True
            print("info: Adapter started")

        except Exception as ex:
            print("error: Adding properties: " + str(ex))

    def poll(self):
        """Poll the device for changes."""
        while True:
            time.sleep(_POLL_INTERVAL)
            try:
                for prop in self.properties.values():
                    prop.update()
            except Exception as ex:
                print("error: Polling properties: " + str(ex))
                continue


class SenseHatProperty(Property):

    def __init__(self, device, name, description, value):
        Property.__init__(self, device, name, description)
        self.device = device
        self.title = name
        self.name = name
        self.description = description
        self.value = value
        self.set_cached_value(value)

    def update(self):
        if self.name == 'humidity':
            value = self.device.controller.humidity
        elif self.name == 'pressure':
            value = self.device.controller.get_pressure()
        elif self.name == 'temperature':
            value = self.device.controller.temperature
        elif self.name == 'compass':
            value = self.device.controller.get_compass()
        else:
            print("warning: %s not handled" % self.name)
            return
        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)

    def set_value(self, value):
        if self.name == 'message':
            self.device.controller.show_message(value)
        elif self.name == 'color':
            color = [int(value[1:3], 0x10),
                     int(value[3:5], 0x10),
                     int(value[5:7], 0x10)]
            self.device.controller.clear(color)
        else:
            print("warning: %s not handled" % self.name)
            return
