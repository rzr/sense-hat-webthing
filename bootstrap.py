# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MPL-2.0

"""
This script exists to ensure that required dependencies are present.

To prevent the need for building dependencies for every possible OS/arch/Python
combination, this script will build the required dependencies. After doing so,
or if the dependencies are already present, main.py will be started.
"""

import os
import subprocess
import sys


_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def install_packages():
    """Install all requirements."""
    cmd = ('./setup.sh')
    try:
        subprocess.check_call(cmd,
                              stderr=subprocess.STDOUT,
                              shell=True,
                              cwd=_BASE_DIR)
        return True
    except subprocess.CalledProcessError as e:
        print(e)
        return False


try:
    from sense_hat import SenseHat

except ImportError:
    # If installation failed, exit with 100 to tell the gateway not to restart
    # this process.
    if not install_packages():
        sys.exit(100)

os.execl(sys.executable, sys.executable, os.path.join(_BASE_DIR, 'main.py'))
