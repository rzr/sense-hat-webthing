#!/usr/bin/env python3
# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MPL-2.0

"""Example webthing"""

from __future__ import division
import logging
from sense_hat import SenseHat
from webthing import (Property, MultipleThings, Thing, Value,
                      WebThingServer)
import tornado.ioloop

controller = SenseHat()

class SenseHatThingSensor(Thing):
    """A Thing controlling Sensors of SenseHat"""

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:my-sense-hat-sensor-1234',
            'SenseHat Sensor',
            [],
            'A web connected sense hat'
        )
        controller.set_imu_config(True, True, True)
        self.compass = Value(0.0)
        self.add_property(
            Property(self,
                     'compass',
                     self.compass,
                     metadata=
                     {'title': 'Compass',
                      'type': 'number',
                      'description': 'Angle to North',
                      'unit': 'º',
                      'minimum': 0,
                      'maximum': 360,
                      'readOnly': True,
                     }))

        self.orientation_pitch = Value(0.0)
        self.add_property(
            Property(self,
                     'orientation_pitch',
                     self.orientation_pitch,
                     metadata=
                     {'title': 'Pitch',
                      'type': 'number',
                      'description': 'Angle pitch',
                      'unit': 'd',
                      'minimum': 0,
                      'maximum': 360,
                      'readOnly': True,
                     }))

        self.orientation_roll = Value(0.0)
        self.add_property(
            Property(self,
                     'orientation-roll',
                     self.orientation_roll,
                     metadata=
                     {'title': 'Roll',
                      'type': 'number',
                      'description': 'Angle',
                      'unit': 'd',
                      'minimum': 0,
                      'maximum': 360,
                      'readOnly': True,
                     }))

        self.orientation_yaw = Value(0.0)
        self.add_property(
            Property(self,
                     'orientation_yaw',
                     self.orientation_yaw,
                     metadata=
                     {'title': 'Yaw',
                      'type': 'number',
                      'description': 'Angle',
                      'unit': 'd',
                      'minimum': 0,
                      'maximum': 360,
                      'readOnly': True,
                     }))

        logging.debug('info: starting the sensor update looping task')
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update_properties,
            1000
        )
        self.timer.start()

    def update_properties(self):
        orientation = controller.get_orientation()
        self.orientation_pitch.notify_of_external_update(orientation["pitch"])
        self.orientation_roll.notify_of_external_update(orientation["roll"])
        self.orientation_yaw.notify_of_external_update(orientation["yaw"])
        compass = controller.get_compass()
        self.compass.notify_of_external_update(compass)

    def cancel_update_properties_task(self):
        self.timer.stop()


class SenseHatThingLight(Thing):
    """A Thing controlling Matrix LED part of SenseHat"""

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:my-sense-hat-light-1234',
            'SenseHat Light',
            ['OnOffSwitch', 'Light'],
            'A web connected lamp'
        )

        self.add_property(
            Property(self,
                     'on',
                     Value(True, lambda v: self.toggle(v)),
                     metadata={
                         '@type': 'OnOffProperty',
                         'title': 'On/Off',
                         'type': 'boolean',
                         'description': 'Whether the lamp is turned on',
                     }))

    def toggle(self, state):
        print('info light state: ', state)
        controller.show_message("on" if bool(state) else "off")


def run_server():
    light = SenseHatThingLight()
    sensor = SenseHatThingSensor()
    server = WebThingServer(MultipleThings([light, sensor],
                                           'SenseHat'),
                            port=8888)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')

if __name__ == '__main__':
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()
