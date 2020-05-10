# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MPL-2.0

"""SenseHat adapter for Mozilla WebThings Gateway."""

from gateway_addon import Device, Property

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

            self.pairing = True
            print("info: Adapter started")

        except Exception as ex:
            print("error: Adding properties: " + str(ex))

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
        print("info: sense_hat." + self.name + " from " + str(self.value) + " to " + str(value))
        if self.name == 'message':
            if not self.device.properties['on'].value:
                bgColor = [0, 0, 0]
            else:
                colorString = self.device.properties['color'].value
                bgColor = [int(colorString[1:3], 0x10),
                           int(colorString[3:5], 0x10),
                           int(colorString[5:7], 0x10)]
            fgColor = [~ int(hex(bgColor[0]), 0x10) & 0xFF,
                       ~ int(hex(bgColor[1]), 0x10) & 0xFF,
                       ~ int(hex(bgColor[2]), 0x10) & 0xFF]
            self.device.controller.show_message(value, 0.1, fgColor, bgColor)

        elif self.name == 'color':
            if self.device.properties['on'].value and (value != self.value):
                color = [int(value[1:3], 0x10),
                         int(value[3:5], 0x10),
                         int(value[5:7], 0x10)]
                self.device.controller.clear(color)
        elif self.name == 'on':
            if value == False:
                self.device.controller.clear([0, 0, 0])
            else:
                colorString = self.device.properties['color'].value
                color = [int(colorString[1:3], 0x10),
                         int(colorString[3:5], 0x10),
                         int(colorString[5:7], 0x10)]
                self.device.controller.clear(color)
        elif self.name == 'rotation':
            if value != 0 and value != 90 and value != 180 and value != 270:
                print("warning: rotation must be 0, 90, 180 or 270")
                return
            if value != self.value:
                self.device.controller.set_rotation(value)

        else:
            print("warning: %s not handled" % self.name)
            return
        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)
