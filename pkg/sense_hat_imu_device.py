# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MPL-2.0

"""SenseHat adapter for Mozilla WebThings Gateway."""

import threading
import time

from gateway_addon import Device, Property

_POLL_INTERVAL = 1

class SenseHatImuDevice(Device):
    """SenseHat IMU device type."""

    def __init__(self, adapter):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        """

        Device.__init__(self, adapter, 'sense-hat-imu')

        self._id = 'sense-hat-imu'
        self.id = 'sense-hat-imu'
        self.adapter = adapter
        self.controller = adapter.controller
        self.controller.set_imu_config(True, True, True)

        self.name = 'SenseHatImu'
        self.description = 'Expose SenseHat IMU sensors'
        self.links = [
            {
                'rel': 'alternate',
                'mediaType': 'text/html',
                'href': adapter.URL
            }
        ]
        self._type = []
        try:
            self.properties['pitch'] = SenseHatImuProperty(
                self,
                'pitch',
                {
                    '@type': 'LevelProperty',
                    'label': "Pitch",
                    'type': 'number',
                    'description': 'Pitch Angle',
                    'unit': 'º',
                    'minimum': -180,
                    'maximum': 180,
                    'readOnly': True
                },
                0)
            self.properties['roll'] = SenseHatImuProperty(
                self,
                'roll',
                {
                    '@type': 'LevelProperty',
                    'label': "Roll",
                    'type': 'number',
                    'description': "Roll Angle",
                    'unit': 'º',
                    'minimum': -180,
                    'maximum': 180,
                    'readOnly': True
                },
                0)
            self.properties['yaw'] = SenseHatImuProperty(
                self,
                'yaw',
                {
                    '@type': 'LevelProperty',
                    'label': "Yaw",
                    'type': 'number',
                    'description': "Yaw Angle",
                    'unit': 'º',
                    'minimum': -180,
                    'maximum': 180,
                    'readOnly': True
                },
                0)

            thread = threading.Thread(target=self.poll)
            thread.daemon = True
            thread.start()

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


class SenseHatImuProperty(Property):

    def __init__(self, device, name, description, value):
        Property.__init__(self, device, name, description)
        self.device = device
        self.title = name
        self.name = name
        self.description = description
        self.value = value
        self.set_cached_value(value)

    def update(self):
        if self.name == 'pitch' or \
           self.name == 'roll' or \
           self.name == 'yaw':
            orientation = self.device.controller.orientation
            value = orientation[self.name] - 180.
        else:
            if False:
                print("warning: %s update: not handled" % self.name)
            return
        print("update: %s=%f" % (self.name, value))
        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)
