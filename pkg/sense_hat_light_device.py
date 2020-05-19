# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MPL-2.0

"""SenseHat adapter for Mozilla WebThings Gateway."""

from gateway_addon import Device, Property

_DEBUG = True

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
            self.properties['character'] = SenseHatProperty(
                self,
                'character',
                {
                    '@type': 'StringProperty',
                    'label': "Character",
                    'type': 'string'
                },
                "")
            self.controller.show_letter("")

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

    def show(self, **kargs):
        """ Refresh matrix light """
        args = {}
        for prop in self.properties.keys():
            if prop not in kargs:
                args[prop] = self.properties[prop].value
            else:
                args[prop] = kargs[prop]
        character = str(args['character'] if args['character'] else " ")[0:1]
        if args['on']:
            bg_color = SenseHatLightDevice.hex_to_rgb(str(args['color']))
            fg_color = SenseHatLightDevice.invert_color(bg_color)
        else:
            bg_color = [0, 0, 0]
            fg_color = SenseHatLightDevice.hex_to_rgb(str(args['color']))

        self.controller.show_letter(character, fg_color, bg_color)
        if 'message' in kargs.keys():
            self.controller.show_message(args['message'], 0.1, fg_color, bg_color)

class SenseHatProperty(Property):
    """ Matrix LCD parms"""

    def __init__(self, device, name, description, value):
        Property.__init__(self, device, name, description)
        self.device = device
        self.title = name
        self.name = name
        self.description = description
        self.value = value
        self.set_cached_value(value)

    def set_value(self, value):
        """ Handle properties changes """
        if _DEBUG:
            print("info: sense_hat." + self.name + " from " + str(self.value) + " to " + str(value))
        if value == self.value:
            return
        if self.name == 'rotation':
            if value != 0 and value != 90 and value != 180 and value != 270:
                print("warning: rotation must be 0, 90, 180 or 270")
                return
            if value != self.value:
                self.device.controller.set_rotation(value)

        elif self.name == 'dim':
            self.device.controller.low_light = value

        else:
            args = {}
            args[self.name] = value
            self.device.show(**args)

        self.set_cached_value(value)
        self.device.notify_property_changed(self)
