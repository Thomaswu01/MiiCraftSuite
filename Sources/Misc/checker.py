#
# -*- coding: utf-8 -*-
#
# Copyright 2012 YoungOptics Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging
import sys
import os


# Setting log system
logging.basicConfig(filename="log.txt", filemode='a', datefmt='%m/%d %H:%M:%S',
                    format='%(asctime)s, %(name)s [%(levelname)s] %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger('checker.py')
logger.debug("EXECUTE: %s" % sys.argv[0])
logger.debug("PWD: %s" % os.getcwd())
logger.debug("PYTHON VERSION: %s" % sys.version)


ENV_MOD_SERIAL_VERSION = ""
try:
    import serial
    ENV_MOD_SERIAL_VERSION = serial.VERSION
    ENV_HAS_SERIAL = True
except ImportError:
    ENV_HAS_SERIAL = False
logger.debug("ENV_HAS_SERIAL=%d(%s)" %
             (ENV_HAS_SERIAL, ENV_MOD_SERIAL_VERSION))

ENV_MOD_PIL_VERSION = ""
try:
    import PIL
    ENV_HAS_PIL = True
except ImportError:
    ENV_HAS_PIL = False
logger.debug("ENV_HAS_PIL=%d(%s)" %
             (ENV_HAS_PIL, ENV_MOD_PIL_VERSION))

ENV_MOD_VPYTHON_VERSION = ""
try:
    import visual
    ENV_MOD_VPYTHON_VERSION = visual.version[0]
    ENV_HAS_VPYTHON = True
except ImportError:
    ENV_HAS_VPYTHON = False
logger.debug("ENV_HAS_VPYTHON=%d(%s)" %
             (ENV_HAS_VPYTHON, ENV_MOD_VPYTHON_VERSION))


# Check Python version
def checkPythonVersion():
    """MiiCraftSuite is based on Python 2.6 and above,
    but is not compatible with Python 3.x.
    """
    isPython2 = False
    if sys.hexversion >= 0x020600F0:
        isPython2 = True
    if sys.hexversion >= 0x030000F0:
        isPython2 = False
    logger.debug("%s isPython2=%d" % (sys._getframe().f_code.co_name, isPython2))
    return isPython2

# Get Python version
def getPythonVersion():
    version = sys.hexversion >> 16
    return version

# Check serial module
def checkPySerial():
    """Check PySerial module"""
    hasPySerial = False
    if sys.version_info[0] == 2:
        hasPySerial = ENV_HAS_SERIAL
    logger.debug("%s hasPySerial=%d" % (sys._getframe().f_code.co_name, hasPySerial))
    return hasPySerial


# Check PIL module
def checkPIL():
    """Check PIL module"""
    hasPIL = False
    if sys.version_info[0] == 2:
        hasPIL = ENV_HAS_PIL
    logger.debug("%s hasPIL=%d" % (sys._getframe().f_code.co_name, hasPIL))
    return hasPIL


# Check VPython module
def checkVPython():
    """Check VPython module"""
    hasVPython = False
    if sys.version_info[0] == 2:
        hasVPython = ENV_HAS_VPYTHON
    logger.debug("%s hasVPython=%d" % (sys._getframe().f_code.co_name, hasVPython))
    return hasVPython


if __name__ == '__main__':
    result = 0
    if len(sys.argv) > 1:
        selection = int(sys.argv[1])
        if selection == 0:
            result = checkPythonVersion()
        elif selection == 1:
            result = checkPySerial()
        elif selection == 2:
            result = checkPIL()
        elif selection == 3:
            result = checkVPython()
    else:
        result = getPythonVersion()
    print result
    sys.exit(result)
