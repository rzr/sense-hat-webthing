# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MPL-2.0

"""SenseHat adapter for Mozilla WebThings Gateway."""

import threading
import time

from gateway_addon import Device, Property

_POLL_INTERVAL = 1

_DEBUG = False

class SenseHatImuDevice(Device):
    """SenseHat IMU device type."""

    def __init__(self, adapter):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        """

        Device.__init__(self, adapter, 'sense-hat-imu')

        self._id = self.id = 'sense-hat-imu'
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
        self._type = ['MultiLevelSensor']
        try:
            self.properties['yaw'] = SenseHatImuProperty(
                self,
                'yaw',
                {
                    '@type': 'LevelProperty',
                    'label': "Yaw",
                    'type': 'number',
                    'description': "Yaw Angle (North)",
                    'unit': 'º',
                    'minimum': -180,
                    'maximum': 180,
                    'readOnly': True
                },
                0)

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

            self.properties['compass'] = SenseHatImuProperty(
                self,
                'compass',
                {
                    '@type': 'OnOffProperty',
                    'label': "Compass",
                    'type': 'boolean',
                    'readOnly': False
                },
                True)

            self.properties['gyro'] = SenseHatImuProperty(
                self,
                'gyro',
                {
                    '@type': 'OnOffProperty',
                    'label': "Gyro",
                    'type': 'boolean',
                    'readOnly': False
                },
                True)

            self.properties['accel'] = SenseHatImuProperty(
                self,
                'accel',
                {
                    '@type': 'OnOffProperty',
                    'label': "Accel",
                    'type': 'boolean',
                    'readOnly': False
                },
                True)

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
    """ Webthing property for motion sensors"""

    def __init__(self, device, name, description, value):
        """ Initialize the object """
        Property.__init__(self, device, name, description)
        self.device = device
        self.title = name
        self.name = name
        self.description = description
        self.value = value
        self.set_cached_value(value)

    def update(self):
        """ read sensors values and notify """
        if self.name == 'pitch' or \
           self.name == 'roll' or \
           self.name == 'yaw':
            orientation = self.device.controller.orientation
            value = orientation[self.name] - 180.
            if _DEBUG:
                print("update: %s=%f" % (self.name, value))
        else:
            if _DEBUG:
                print("warning: %s update: not handled" % self.name)
            return
        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)


    def set_value(self, value):
        """ En/Dis/able sensors """
        if value != self.value:
            config = {'compass_enabled': self.device.properties['compass'].value,
                      'gyro_enabled': self.device.properties['gyro'].value,
                      'accel_enabled': self.device.properties['accel'].value}
            config[self.name + "_enabled"] = value
            print(config)
            self.device.controller.set_imu_config(**config)
            self.set_cached_value(value)
            self.device.notify_property_changed(self)
