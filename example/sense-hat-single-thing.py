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

        logging.debug('starting the sensor update looping task')
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update_properties,
            1000
        )
        self.timer.start()

    def update_properties(self):
        compass = self.sense.get_compass()
        logging.debug("update: compass=%s", compass)
        self.compass.notify_of_external_update(compass)

    def cancel_update_properties_task(self):
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
