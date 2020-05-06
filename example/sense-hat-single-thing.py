# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MPL-2.0

"""Example webthing"""

from __future__ import division
import logging
from sense_hat import SenseHat
from webthing import (Property, SingleThing, Thing, Value,
                      WebThingServer)
import tornado.ioloop


class SenseHatThing(Thing):
    """A Thing which updates its measurement every few seconds."""

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:my-sense-hat-1234',
            'My Sense Hat',
            ['MultiLevelSensor'],
            'A web connected sense hat'
        )
        self.sense = SenseHat()
        self.sense.set_imu_config(False, True, False)
        self.level = Value(0.0)
        self.add_property(
            Property(self,
                     'level',
                     self.level,
                     metadata=
                     {'title': 'Angle',
                      'type': 'number',
                      'description': 'North',
                      'minimum': 0,
                      'maximum': 360,
                      'unit': 'degrees',
                      'readOnly': True,
                     }))

        logging.debug('starting the sensor update looping task')
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update_level,
            1000
        )
        self.timer.start()

    def update_level(self):
        new_level = self.sense.get_compass()
        logging.debug("setting new compass level: %s", new_level)
        self.level.notify_of_external_update(new_level)

    def cancel_update_level_task(self):
        self.timer.stop()


def run_server():

    thing = SenseHatThing()
    server = WebThingServer(SingleThing(thing), port=8888)
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
