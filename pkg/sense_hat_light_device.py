# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MPL-2.0

"""SenseHat adapter for Mozilla WebThings Gateway."""

from gateway_addon import Device, Property

_DEBUG = False

class SenseHatLightDevice(Device):
    """SenseHat device type."""

    def __init__(self, adapter):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        """
        Device.__init__(self, adapter, 'sense-hat-light')
        self._id = 'sense-hat-light'
        self.id = 'sense-hat-light'
        self.adapter = adapter
        self.controller = adapter.controller

        self.name = 'SenseHatLight'
        self.description = 'Expose SenseHat actuators'
        self.links = [
            {
                'rel': 'alternate',
                'mediaType': 'text/html',
                'href': adapter.URL
            }
        ]
        self._type = ['ColorControl', 'Light', 'OnOffSwitch']
        try:
            self.properties['message'] = SenseHatProperty(
                self,
                "message",
                {
                    '@type': 'StringProperty',
                    'label': "Message",
                    'type': 'string'
                },
                "")
            self.controller.show_message("")

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
            self.controller.clear([0xFF, 0xFF, 0xFF])

            self.properties['on'] = SenseHatProperty(
                self,
                "on",
                {
                    '@type': 'OnOffProperty',
                    'label': "Switch",
                    'type': 'boolean',
                    'readOnly': False
                },
                False)
            self.controller.clear([0, 0, 0])

            self.properties['rotation'] = SenseHatProperty(
                self,
                "rotation",
                {
                    '@type': 'NumberProperty',
                    'label': "Rotation",
                    'type': 'integer',
                    'description': 'Rotation of LED matrix',
                    'unit': 'degrees',
                    'enum': [0, 90, 180, 270]
                },
                0)
            self.controller.set_rotation(0)

            self.properties['dim'] = SenseHatProperty(
                self,
                'dim',
                {
                    '@type': 'BooleanProperty',
                    'label': "Dim",
                    'type': 'boolean',
                    'description': 'Low light for dark environement',
                },
                False)
            self.controller.low_light = False
            
            self.pairing = True
            print("info: Adapter started")

        except Exception as ex:
            print("error: Adding properties: " + str(ex))

    @staticmethod
    def hex_to_rgb(text):
        """ Convert #RRBBGG to list of integer [0-255]"""
        color = [int(text[1:3], 0x10),
                 int(text[3:5], 0x10),
                 int(text[5:7], 0x10)]
        return color

    @staticmethod
    def invert_color(bg_color):
        """ Invert color from list of integers"""
        fg_color = [~ int(hex(bg_color[0]), 0x10) & 0xFF,
                    ~ int(hex(bg_color[1]), 0x10) & 0xFF,
                    ~ int(hex(bg_color[2]), 0x10) & 0xFF]
        return fg_color

class SenseHatProperty(Property):

    def __init__(self, device, name, description, value):
        Property.__init__(self, device, name, description)
        self.device = device
        self.title = name
        self.name = name
        self.description = description
        self.value = value
        self.set_cached_value(value)

    def set_value(self, value):
        if _DEBUG:
            print("info: sense_hat." + self.name + " from " + str(self.value) + " to " + str(value))
        if self.name == 'message':
            if not self.device.properties['on'].value:
                bg_color = [0, 0, 0]
            else:
                text = self.device.properties['color'].value
                bg_color = SenseHatLightDevice.hex_to_rgb(text)
            fg_color = SenseHatLightDevice.invert_color(bg_color)
            self.device.controller.show_message(value, 0.1, fg_color, bg_color)

        elif self.name == 'color':
            if self.device.properties['on'].value:
                bg_color = SenseHatLightDevice.hex_to_rgb(value)
                self.device.controller.clear(bg_color)

        elif self.name == 'on':
            if value == False:
                self.device.controller.clear([0, 0, 0])
            else:
                text = self.device.properties['color'].value
                bg_color = SenseHatLightDevice.hex_to_rgb(text)
                self.device.controller.clear(bg_color)

        elif self.name == 'rotation':
            if value != 0 and value != 90 and value != 180 and value != 270:
                print("warning: rotation must be 0, 90, 180 or 270")
                return
            if value != self.value:
                self.device.controller.set_rotation(value)

        elif self.name == 'dim':
            self.device.controller.low_light = value

        else:
            if _DEBUG:
                print("warning: %s not handled" % self.name)
            return
        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)
