# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MPL-2.0

"""SenseHat adapter for Mozilla WebThings Gateway."""

from sense_hat import SenseHat
from gateway_addon import Adapter
from .sense_hat_device import SenseHatDevice


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
            self.controller = SenseHat()
            device = SenseHatDevice(self)
            self.handle_device_added(device)
            if self.DEBUG:
                print("sense_hat_device created")
            self.devices['sense-hat'].connected = True
            self.devices['sense-hat'].connected_notify(True)

        except Exception as ex:
            print("Could not create sense_hat_device: " + str(ex))
