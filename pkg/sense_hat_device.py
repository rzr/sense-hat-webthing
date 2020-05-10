# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MPL-2.0

"""SenseHat adapter for Mozilla WebThings Gateway."""

from sense_hat import SenseHat
from gateway_addon import Device, Property
import threading
import time

_POLL_INTERVAL = 5

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
        self.controller = adapter.controller
        self.controller.set_imu_config(False, True, False)

        self.name = 'Sense Hat'
        self.name = 'SenseHat'
        self.description = 'Expose SenseHat sensors'
        self.links = [
            {
                'rel': 'alternate',
                'mediaType': 'text/html',
                'href': adapter.URL
            }
        ]
        self._type = ['TemperatureSensor']
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
                    '@type': 'TemperatureProperty',
                    'label': "Temperature",
                    'type': 'number',
                    'unit': 'ºC',
                    'readOnly': True
                },
                0)
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
            self.properties['down'] = SenseHatProperty(
                self,
                "down",
                {
                    '@type': 'PushedProperty',
                    'label': "Down",
                    'type': 'boolean',
                    'readOnly': True
                },
                False)
            self.properties['left'] = SenseHatProperty(
                self,
                "left",
                {
                    '@type': 'PushedProperty',
                    'label': "Left",
                    'type': 'boolean',
                    'readOnly': True
                },
                False)
            self.properties['right'] = SenseHatProperty(
                self,
                "right",
                {
                    '@type': 'PushedProperty',
                    'label': "Right",
                    'type': 'boolean',
                    'readOnly': True
                },
                False)
            self.properties['up'] = SenseHatProperty(
                self,
                "up",
                {
                    '@type': 'PushedProperty',
                    'label': "Up",
                    'type': 'boolean',
                    'readOnly': True
                },
                False)
            t = threading.Thread(target=self.poll)
            t.daemon = True
            t.start()

            events = threading.Thread(target=self.handle_events)
            events.daemon = True
            events.start()

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
                print(prop.name)
                continue

    def handle_events(self):
        while True:
             event = self.controller.stick.wait_for_event(True)
             prop = self.properties[event.direction]
             value = True if (str(event.action) == 'held') else False
             prop.set_cached_value_and_notify(value)

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
            if False:
                print("warning: %s update: not handled" % self.name)
            return
        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)

