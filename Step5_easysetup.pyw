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


import sys
import platform
import os
import subprocess
import logging
import locale
import glob
import zipfile


MIICRAFT_VERSION = "_V05"
MIICRAFT_DST_PATH = "c:\\MiiCraft"+MIICRAFT_VERSION+"\\"
MIICRAFT_SRC_PATH = os.getcwd()+"\\"
MIICRAFT_MSG_INTERRUPT_SETUP = \
"""Setup is not complete. If you exit now, you may run Setup again
at another time to complete the installation.

Exit Setup?"""
MIICRAFT_MSG_COMPLETE_SETUP_TMP = \
"""Setup has finished installing MiiCraft on your computer.
The application may be launched by selecting the MiiCraftSuite.py
in INSTALL_PATH

Click button to exit Setup."""
MIICRAFT_MSG_COMPLETE_SETUP = \
MIICRAFT_MSG_COMPLETE_SETUP_TMP.replace("INSTALL_PATH", MIICRAFT_DST_PATH)


MIICRAFT_BTN_YES = 0x00000001
MIICRAFT_BTN_NO = 0x00000002
MIICRAFT_BTN_YESNO = MIICRAFT_BTN_YES | MIICRAFT_BTN_NO


MIICRAFT_CTRL_SHOW_DIALOG_THEN_CHECK = 3
MIICRAFT_CTRL_CHECK = 2
MIICRAFT_CTRL_SUCCESS = 1
MIICRAFT_CTRL_FAIL = 0
MIICRAFT_CTRL_SHOW_DIALOG_THEN_EXIT = -1


# Setting log system
logging.basicConfig(filename="log.txt", filemode='a', datefmt='%m/%d %H:%M:%S',
                    format='%(asctime)s, %(name)s [%(levelname)s] %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger('easysetup.py')
logger.debug("Setup MiiCraft Start")
logger.debug("VERSION: %s" % MIICRAFT_VERSION)
logger.debug("INSTALL_PATH: %s" % MIICRAFT_DST_PATH)
logger.debug("EXECUTE: %s" % sys.argv[0])
logger.debug("PWD: %s" % os.getcwd())
logger.debug("PYTHON VERSION: %s" % sys.version)
logger.debug("PLATFORM: %s" % platform.platform())
logger.debug("PATH: %s" % sys.path)
logger.debug("LOCAL: %s,%s" % locale.getlocale())
    

# Compatible Python3
if sys.hexversion >= 0x030000F0:
    from tkinter import *
    from tkinter.filedialog import askopenfilename
    import winreg
    
    def unicode(text, codec):
        return text.encode(codec)
else:
    from Tkinter import *
    from tkFileDialog import askopenfilename
    import _winreg as winreg


# Get user home path
ENV_HOMEPATH = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']
logger.debug("ENV_HOMEPATH=%s" % ENV_HOMEPATH)


# Check serial module
ENV_MOD_SERIAL_VERSION = ""
try:
    import serial
    ENV_MOD_SERIAL_VERSION = serial.VERSION
    ENV_HAS_SERIAL = True
except ImportError:
    ENV_HAS_SERIAL = False
logger.debug("ENV_HAS_SERIAL=%d(%s)" %
             (ENV_HAS_SERIAL, ENV_MOD_SERIAL_VERSION))


# Check PIL module
ENV_MOD_PIL_VERSION = ""
try:
    import PIL
    ENV_HAS_PIL = True
except ImportError:
    ENV_HAS_PIL = False
logger.debug("ENV_HAS_PIL=%d(%s)" %
             (ENV_HAS_PIL, ENV_MOD_PIL_VERSION))


# Check VPython module
ENV_MOD_VPYTHON_VERSION = ""
try:
    import visual
    ENV_MOD_VPYTHON_VERSION = visual.version[0]
    ENV_HAS_VPYTHON = True
except ImportError:
    ENV_HAS_VPYTHON = False
logger.debug("ENV_HAS_VPYTHON=%d(%s)" %
             (ENV_HAS_VPYTHON, ENV_MOD_VPYTHON_VERSION))














"""
Check python version
"""
def checkPython2(state=0):
    result = MIICRAFT_CTRL_FAIL
    try:
        isPython2 = subprocess.call("Sources\\Misc\\checker.py 0", shell=True)
    except:
        logger.debug("%s call fail" % sys._getframe().f_code.co_name)
    if state == 0:
        if isPython2:
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_FAIL
        state += 1
    elif state == 1:
        if isPython2:
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_SHOW_DIALOG_THEN_EXIT
    logger.debug("%s(%d)=%d" % (sys._getframe().f_code.co_name, state, result))
    return (result, state)

def installPython26():
    """Install Python 2.6.6"""
    logger.debug("%s entry" % sys._getframe().f_code.co_name)
    try:
        subprocess.call("msiexec /i python-2.6.6.msi")
    except:
        logger.debug("%s call fail" % sys._getframe().f_code.co_name)
    logger.debug("%s exit" % sys._getframe().f_code.co_name)
    return True

MIICRAFT_SETUP_STEP1_DIALOG1 = (
"Error",
"Please install Python2.6.6 then run setup again",
None,
MIICRAFT_BTN_YES,
None)

MIICRAFT_SETUP_STEP1 = (
"MiiCraftSuite is based on Python2 (2.6 and above)",
checkPython2, 0,
"Install Python 2.6.6",
installPython26, 0,
(None, MIICRAFT_SETUP_STEP1_DIALOG1))


"""
Check PySerial module
"""
def checkPySerial(state=0):
    result = MIICRAFT_CTRL_FAIL
    try:
        hasPySerial = subprocess.call("Sources\\Misc\\checker.py 1", shell=True)
    except:
        logger.debug("%s call fail" % sys._getframe().f_code.co_name)
    if state == 0:
        if hasPySerial:
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_FAIL
        state += 1
    elif state == 1:
        if hasPySerial:
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_SHOW_DIALOG_THEN_EXIT
    logger.debug("%s(%d)=%d" % (sys._getframe().f_code.co_name, state, result))
    return (result, state)

def installPySerial():
    logger.debug("%s entry" % sys._getframe().f_code.co_name)
    try:
        subprocess.call("Sources\\pyserial-2.5.win32.exe")
    except:
        logger.debug("%s call fail" % sys._getframe().f_code.co_name)
    logger.debug("%s exit" % sys._getframe().f_code.co_name)
    return True

MIICRAFT_SETUP_STEP2_DIALOG1 = (
"Error",
"Please install PySerial then run setup again",
None,
MIICRAFT_BTN_YES,
None)

MIICRAFT_SETUP_STEP2 = (
"PySerial is a bridge between device and PC",
checkPySerial, 0,
"Install PySerial module",
installPySerial, 10000,
(None, MIICRAFT_SETUP_STEP2_DIALOG1))


"""
Check PIL module
"""
def checkPIL(state=0):
    result = MIICRAFT_CTRL_FAIL
    try:
        hasPIL = subprocess.call("Sources\\Misc\\checker.py 2", shell=True)
    except:
        logger.debug("%s call fail" % sys._getframe().f_code.co_name)
    if state == 0:
        if hasPIL:
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_FAIL
        state += 1
    elif state == 1:
        if hasPIL:
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_SHOW_DIALOG_THEN_EXIT
    logger.debug("%s(%d)=%d" % (sys._getframe().f_code.co_name, state, result))
    return (result, state)

def installPIL():
    """Install PIL module"""
    logger.debug("%s entry" % sys._getframe().f_code.co_name)
    version=0x0206
    try:
        version= subprocess.call("Sources\\Misc\\checker.py", shell=True)
    except:
        logger.debug("%s call fail" % sys._getframe().f_code.co_name)
    try:
        if version == 0x0206:
            subprocess.call("Sources\\PIL-1.1.7.win32-py2.6.exe")
        elif version == 0x0207:
            subprocess.call("Sources\\PIL-1.1.7.win32-py2.7.exe")
    except:
        logger.debug("%s call fail" % sys._getframe().f_code.co_name)
    logger.debug("%s exit" % sys._getframe().f_code.co_name)
    return True

MIICRAFT_SETUP_STEP3_DIALOG1 = (
"Error",
"Please install PIL then run setup again",
None,
MIICRAFT_BTN_YES,
None)

MIICRAFT_SETUP_STEP3 = (
"Using PIL to do image processing",
checkPIL, 0,
"Install PIL module",
installPIL, 10000,
(None, MIICRAFT_SETUP_STEP3_DIALOG1))


"""
Check PySerial module
"""
def checkVPython(state=0):
    """Check VPython module"""
    result = MIICRAFT_CTRL_FAIL
    try:
        hasVPython = subprocess.call("Sources\\Misc\\checker.py 3", shell=True)
    except:
        logger.debug("%s call fail" % sys._getframe().f_code.co_name)
    if state == 0:
        if hasVPython:
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_FAIL
        state += 1
    elif state == 1:
        if hasVPython:
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_SHOW_DIALOG_THEN_EXIT
    logger.debug("%s(%d)=%d" % (sys._getframe().f_code.co_name, state, result))
    return (result, state)

def installVPython():
    """Install PIL module"""
    logger.debug("%s entry" % sys._getframe().f_code.co_name)
    version=0x0206
    try:
        version= subprocess.call("Sources\\Misc\\checker.py", shell=True)
    except:
        logger.debug("%s call fail" % sys._getframe().f_code.co_name)
    try:
        if version == 0x0206:
            subprocess.call("Sources\\VPython-Win-Py2.6-5.72.exe")
        elif version == 0x0207:
            subprocess.call("Sources\\VPython-Win-Py2.7-5.72.exe")
    except:
        logger.debug("%s call fail" % sys._getframe().f_code.co_name)
    logger.debug("%s exit" % sys._getframe().f_code.co_name)
    return True

MIICRAFT_SETUP_STEP4_DIALOG1 = (
"Error",
"Please install VPython then run setup again",
None,
MIICRAFT_BTN_YES,
None)

MIICRAFT_SETUP_STEP4 = (
"VPython is a good 3D library", 
checkVPython, 0,
"Install VPython module",
installVPython, 0,
(None, MIICRAFT_SETUP_STEP4_DIALOG1))


"""
Check ImageMagick
"""
def enumerateReg(group, keyName):
    """Enumerate windows registry"""
    subkeys = list()
    i = 0
    try:
        key = winreg.OpenKey(group, keyName)
    except WindowsError:
        return subkeys
    try:
        while True:
            subkey = winreg.EnumKey(key, i)
            subkeys.append(subkey)
            i += 1
    except WindowsError:
        pass
    winreg.CloseKey(key)
    return subkeys

def checkImageMagick():
    """Check ImageMagick"""
    hasImageMagick = False
    version = ""
    keys = enumerateReg(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE")
    for key in keys:
        if key == "ImageMagick":
            hasImageMagick = True
            break
    keys = enumerateReg(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\ImageMagick")
    if len(keys) > 0:
       version = keys[0] 
    logger.debug("%s hasImageMagick=%d(%s)" %
                  (sys._getframe().f_code.co_name, hasImageMagick, version))
    return hasImageMagick

def checkImageMagick2(state=0):
    result = MIICRAFT_CTRL_FAIL
    hasImageMagick = checkImageMagick()
    if state == 0:
        if hasImageMagick:
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_FAIL
        state += 1
    elif state == 1:
        if hasImageMagick:
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_SHOW_DIALOG_THEN_EXIT
    logger.debug("%s(%d)=%d" % (sys._getframe().f_code.co_name, state, result))
    return (result, state)

def installImageMagick():
    """Install ImageMagick"""
    logger.debug("%s entry" % sys._getframe().f_code.co_name)
    try:
        subprocess.call("Sources\\ImageMagick-6.7.6-8-Q16-windows-dll.exe")
    except:
        logger.debug("%s call fail" % sys._getframe().f_code.co_name)
    logger.debug("%s exit" % sys._getframe().f_code.co_name)
    return True

MIICRAFT_SETUP_STEP5_DIALOG1 = (
"Error",
"Please install ImageMagick then run setup again",
None,
MIICRAFT_BTN_YES,
None)

MIICRAFT_SETUP_STEP5 = (
"Use ImageMagick to convert images in a variety of formats",
checkImageMagick2, 0,
"Install ImageMagick",
installImageMagick, 0,
(None, MIICRAFT_SETUP_STEP5_DIALOG1))


"""
Install MiiCraft
"""
def createMiiCraftFolder():
    # Create $HOME\.miicraft and $HOME\.miicraft\output
    if not os.path.isdir(ENV_HOMEPATH+"\\.miicraft"):
        os.mkdir(ENV_HOMEPATH+"\\.miicraft")
    if not os.path.isdir(ENV_HOMEPATH+"\\.miicraft\\output"):
        os.mkdir(ENV_HOMEPATH+"\\.miicraft\\output")
    # Create C:\MiiCraft
    if not os.path.isdir(MIICRAFT_DST_PATH):
        os.mkdir(MIICRAFT_DST_PATH)
    if not os.path.isdir(MIICRAFT_DST_PATH+"\\skeinforge"):
        os.mkdir(MIICRAFT_DST_PATH+"\\skeinforge")
    return True

def checkMiiCraftFolder():
    result = True
    if not os.path.isdir(ENV_HOMEPATH+"\\.miicraft"):
        logger.error("No %s\\.miicraft folder" % ENV_HOMEPATH)
        result = False
    if not os.path.isdir(ENV_HOMEPATH+"\\.miicraft\\output"):
        logger.error("No %s\\.miicraft\\output folder" % ENV_HOMEPATH)
        result = False
    if not os.path.isdir(MIICRAFT_DST_PATH):
        logger.error("No %s folder" % MIICRAFT_DST_PATH)
        result = False
    if not os.path.isdir(MIICRAFT_DST_PATH+"\\skeinforge"):
        logger.error("No %s\\skeinforge folder" % MIICRAFT_DST_PATH)
        result = False
    logger.debug("%s result=%d" % (sys._getframe().f_code.co_name, result))
    return result

def makeMiiCraftCopyList():
    os.chdir("Sources")
    fileList = list()
    fileList += glob.glob("*.py")
    fileList += glob.glob("*.ini")
    fileList += glob.glob("*.gif")
    fileList += glob.glob("*.png")
    for (dirpath, dirnames, filenames) in os.walk("Samples"):
        fileList.append(dirpath+"\\")
        for i in range(len(filenames)):
            file = os.path.join(dirpath, filenames[i])
            fileList.append(file)
    os.chdir(MIICRAFT_SRC_PATH)
    return fileList

def installMiiCraft(fileList):
    os.chdir(MIICRAFT_DST_PATH)
    dir = MIICRAFT_SRC_PATH+"Sources"
    for name in fileList:
        if name.endswith('\\'):
            if not os.path.isdir(name):
                os.mkdir(name)
        else:
            infile = open(os.path.join(dir, name), 'rb')
            outfile = open(name, 'wb')
            outfile.write(infile.read())
            infile.close()
            outfile.close()
    os.chdir(MIICRAFT_SRC_PATH)
    return True

def checkMiiCraft(fileList):
    result = True
    os.chdir(MIICRAFT_DST_PATH)
    for name in fileList:
        if name.endswith('\\'):
            if not os.path.isdir(name):
                logger.error("No %s folder" % name)
                result = False
        else:
            if not os.path.isfile(name):
                logger.error("No %s" % name)
                result = False
    os.chdir(MIICRAFT_SRC_PATH)
    return result


def checkMiiCraft2(state=0):
    result = MIICRAFT_CTRL_FAIL
    if state == 0:
        # check create folder
        createMiiCraftFolder()
        if checkMiiCraftFolder():
            result = MIICRAFT_CTRL_CHECK
        else:
            result = MIICRAFT_CTRL_SHOW_DIALOG_THEN_EXIT
        state += 1
    elif state == 1:
        fileList = makeMiiCraftCopyList()
        installMiiCraft(fileList)
        result = MIICRAFT_CTRL_CHECK
        state += 1
    elif state == 2:
        fileList = makeMiiCraftCopyList()
        if checkMiiCraft(fileList):
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_SHOW_DIALOG_THEN_EXIT
    logger.debug("%s(%d)=%d" % (sys._getframe().f_code.co_name, state, result))
    return (result, state)

MIICRAFT_SETUP_STEP6_DIALOG0 = (
"Error",
"No emought space or limits of authority to install", 
None,
MIICRAFT_BTN_YES,
None)

MIICRAFT_SETUP_STEP6 = (
("The MiiCraft is installed in %s as default" % MIICRAFT_DST_PATH),
checkMiiCraft2, 0,
None,
None, 0,
(MIICRAFT_SETUP_STEP6_DIALOG0, None, MIICRAFT_SETUP_STEP6_DIALOG0))


"""
Install Skeinforge
"""
def installSkeinforge():
    zfobj = zipfile.ZipFile(MIICRAFT_SRC_PATH+"Sources\\50_reprap_python_beanshell.zip")
    os.chdir(MIICRAFT_DST_PATH)
    dir = 'skeinforge'
    for name in zfobj.namelist():
        if name.endswith('/'):
            if not os.path.isdir(os.path.join(dir, name)):
                os.mkdir(os.path.join(dir, name))
        else:
            outfile = open(os.path.join(dir, name), 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()
    os.chdir(MIICRAFT_SRC_PATH)
    return True

def checkSkeinforge():
    result = True
    zfobj = zipfile.ZipFile(MIICRAFT_SRC_PATH+"Sources\\50_reprap_python_beanshell.zip")
    os.chdir(MIICRAFT_DST_PATH)
    dir = 'skeinforge'
    for name in zfobj.namelist():
        if name.endswith('/'):
            subdir = os.path.join(dir, name)
            if not os.path.isdir(subdir):
                logger.error("No %s//%s folder" % (MIICRAFT_DST_PATH, subdir))
                result = False
        else:
            file = os.path.join(dir, name)
            if not os.path.isfile(file):
                logger.error("No %s//%s folder" % (MIICRAFT_DST_PATH, file))
                result = False
    if result:
        execFile = MIICRAFT_DST_PATH+"skeinforge\\skeinforge_application\\skeinforge.py"
        try:
            subprocess.call(execFile, shell=True)
        except:
            logger.error("Can't execute %s" % execFile)
            result = False
    os.chdir(MIICRAFT_SRC_PATH)
    logger.debug("%s result=%d" % (sys._getframe().f_code.co_name, result))
    return result

def checkSkeinforge2(state=0):
    result = MIICRAFT_CTRL_FAIL
    if state == 0:
        installSkeinforge()
        result = MIICRAFT_CTRL_CHECK
        state += 1
    elif state == 1:
        if checkSkeinforge():
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_SHOW_DIALOG_THEN_EXIT
    logger.debug("%s(%d)=%d" % (sys._getframe().f_code.co_name, state, result))
    return (result, state)

MIICRAFT_SETUP_STEP7_DIALOG0 = (
"Error",
"File is corrupted, please re-download and setup again",
None,
MIICRAFT_BTN_YES,
None)

MIICRAFT_SETUP_STEP7 = (
"Skeinforge is a good tool to slice 3D model", 
checkSkeinforge2, 0,
None,
None, 0,
(None, MIICRAFT_SETUP_STEP7_DIALOG0))


"""
Select calibration file
"""
def checkCalibrationFile():
    result = True
    if not os.path.isfile(MIICRAFT_DST_PATH+"CorrectRGB_MASK.png"):
        result = False
    return result

def installCalibrationFile():
    longfilename = askopenfilename(title='Put CorrectRGB_MASK.png', filetypes=[('PNG files', '*.png')], initialdir = "output")
    if longfilename is None or longfilename == "":
        return False
    os.chdir(MIICRAFT_DST_PATH)
    infile = open(longfilename , 'rb')
    outfile = open("CorrectRGB_MASK.png", 'wb')
    outfile.write(infile.read())
    infile.close()
    outfile.close()
    os.chdir(MIICRAFT_SRC_PATH)
    return True

def checkCalibrationFile2(state=0):
    result = MIICRAFT_CTRL_FAIL
    if state == 0:
        if checkCalibrationFile():
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_FAIL
        state += 1
    elif state == 1:
        if checkCalibrationFile():
            result = MIICRAFT_CTRL_SUCCESS
        else:
            result = MIICRAFT_CTRL_SHOW_DIALOG_THEN_EXIT
    logger.debug("%s(%d)=%d" % (sys._getframe().f_code.co_name, state, result))
    return (result, state)

MIICRAFT_SETUP_STEP8_DIALOG1 = (
"Error",
"Please get a right CorrectRGB_MASK.png",
None,
MIICRAFT_BTN_YES,
None)

MIICRAFT_SETUP_STEP8 = (
"Search CorrectRGB_MASK.png", 
checkCalibrationFile2, 0,
None,
installCalibrationFile, 0,
(None, MIICRAFT_SETUP_STEP8_DIALOG1))


MIICRAFT_SETUP_STEP = (
                       MIICRAFT_SETUP_STEP1,
                       MIICRAFT_SETUP_STEP2, 
                       MIICRAFT_SETUP_STEP3, 
                       MIICRAFT_SETUP_STEP4, 
                       MIICRAFT_SETUP_STEP5, 
                       MIICRAFT_SETUP_STEP6, 
                       MIICRAFT_SETUP_STEP7, 
                       MIICRAFT_SETUP_STEP8)


class MiiCraftMsgDialog(Toplevel):
    """Message dialog"""
    
    def __init__(self, parent,
                  title=None,
                  message=None,
                  photo=None,
                  btnBoxType=MIICRAFT_BTN_YES):
        Toplevel.__init__(self, parent)
        # Window setting
        self.transient(parent)
        self.resizable(False, False)
        self.configure(bg="#ffffff")
        self.geometry("+%d+%d" % (parent.winfo_x()+160, parent.winfo_y()+90))
        self.parent = parent
        # Show title
        if title is not None:
            self.title(title)
        else:
            self.title("")
        # Show message
        if message is not None:
            self.labelMsg= Label(self, text=message, justify=LEFT)
            self.labelMsg.grid(row=0, columnspan=4, sticky=W+E+N+S)
            self.labelMsg.configure(bg="#ffffff")
        # Show photo
        if photo is not None:
            self.photoMsg = PhotoImage(file=photo)
            self.labelImage = Label(self, image=self.photoMsg)
            self.labelImage.grid(row=1, columnspan=4, sticky=W+E+N+S)
            self.labelImage.configure(bg="#ffffff")
        # Show button
        self.parent.dialogReturn = 0
        self.btnBox = MiiCraftButtonBoxWidget(self, btnBoxType, self.clickBtnBox)
        self.btnBox.grid(row=2, column=3, sticky=E)
        # Event
        self.protocol("WM_DELETE_WINDOW", self.cancel)
    
    def clickBtnBox(self):
        self.parent.dialogResult = self.btnBox.result
        self.cancel()
    
    def cancel(self):
        self.destroy()


class MiiCraftButtonBoxWidget(Frame):
    """Button box"""
    
    def __init__(self, parent=None, type=MIICRAFT_BTN_YES, callback=None):
        Frame.__init__(self, parent)
        self.pack()
        self.configure(bg="#ffffff")
        
        self.callback = callback
        self.result = 0
        self.photoYes = PhotoImage(file="Sources\\Misc\\btn-yes.gif")
        self.photoNo = PhotoImage(file="Sources\\Misc\\btn-no.gif")
        # Select type
        if type & MIICRAFT_BTN_YES:
            self.btnYes = Button(self, image=self.photoYes, command=self.clickYes)
            self.btnYes.grid(row=0, column= 0, sticky=W+E+N+S)
            self.btnYes.configure(bg="#ffffff")
            self.btnYes.configure(activebackground="#aaffaa")
            self.btnYes.configure(borderwidth=0)
        if type & MIICRAFT_BTN_NO:
            self.btnNo = Button(self, image=self.photoNo, command=self.clickNo)
            self.btnNo.grid(row=0, column=1, sticky=W+E+N+S)
            self.btnNo.configure(bg="#ffffff")
            self.btnNo.configure(activebackground="#ffaaaa")
            self.btnNo.configure(borderwidth=0)
    
    def clickYes(self):
        self.result = MIICRAFT_BTN_YES
        self.doCallback()
    
    def clickNo(self):
        self.result = MIICRAFT_BTN_NO
        self.doCallback()
    
    def doCallback(self):
        if self.callback is not None:
            self.callback()


class MiiCraftLEDBarWidget(Frame):
    """LED bar"""
    
    def __init__(self, parent=None, number=1):
        Frame.__init__(self, parent)
        self.pack()
        self.configure(bg="#ffffff")
        
        self.number = number # total LED number
        self.photoLEDs = (
                          PhotoImage(file="Sources\\Misc\\task-status-01.gif"),
                          PhotoImage(file="Sources\\Misc\\task-status-02.gif"),
                          PhotoImage(file="Sources\\Misc\\task-status-03.gif"))
        self.labelLEDs = list()
        for i in range(number):
            self.labelLEDs.append(Label(self, image=self.photoLEDs[0]))
            self.labelLEDs[i].grid(row=0, column= i, sticky=W+E+N+S)
            self.labelLEDs[i].configure(bg="#ffffff")
    
    def dark(self):
        for i in range(self.number):
             self.labelLEDs[i].configure(image=self.photoLEDs[0])
    
    def light(self, index):
        if index < 0:
            self.dark()
        elif index > self.number:
            return
        if index != self.number:
            self.labelLEDs[index].configure(image=self.photoLEDs[1])
        for i in range(0, index):
             self.labelLEDs[i].configure(image=self.photoLEDs[2])


class MiiCraftBannerWidget(Frame):
    """Banner, show the introduction and operating guide of MiiCraft"""
    
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        self.configure(bg="#ffffff")
        
        # [TODO] automatically load image from folder
        self.photoBanners = (
                             PhotoImage(file="Sources\\Misc\\index-banner-01.gif"),
                             PhotoImage(file="Sources\\Misc\\index-banner-02.gif"),
                             PhotoImage(file="Sources\\Misc\\index-banner-03.gif"))
        self.now = 0 # show which one
        self.number = len(self.photoBanners) # total banner number
        self.labelBanner = Label(self, image=self.photoBanners[self.now])
        self.labelBanner.grid(row=0, sticky=W+E+N+S)
        self.labelBanner.configure(bg="#ffffff")
    
    def showNext(self):
        self.now += 1
        self.now %= self.number
        self.labelBanner.configure(image = self.photoBanners[self.now])
    
    def showPre(self):
        self.now += self.number - 1
        self.now %= self.number
        self.labelBanner.configure(image = self.photoBanners[self.now])


class MiiCraftSetupMainWidget(Frame):
    """Main widget"""
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack()
        self.configure(bg="#ffffff")
        self.parent = parent
        self.wait = 500 # waiting time
        
        # Message dialog, show what's hasppen at now
        self.dialogResult = 0 # Hold the result of the message dialog
        # Banner, show the introduction and operating guide of MiiCraft
        self.banner = MiiCraftBannerWidget(self)
        self.banner.grid(row=0, columnspan=3, sticky=W+E+N+S)
        # LED bar, show the running step
        self.majorStep = 0 # change major task
        self.minorStep = 0 # control status of task
        self.microStep = 0 # identify flag of task
        self.stepLEDBar = MiiCraftLEDBarWidget(self, len(MIICRAFT_SETUP_STEP))
        self.stepLEDBar.grid(row=1, column=2, sticky=E)
        # Message bar. show some information about setup status
        self.message = Label(self, text="")
        self.message.grid(row=1, columnspan=2, sticky=W)
        self.message.configure(bg="#ffffff")
        # Timer, background task
        self.after(2000, self.changeBanner)
        self.after(1000, self.runSetupStep)
        
    def changeBanner(self):
        self.banner.showNext()
        self.after(2000, self.changeBanner)
    
    def updateLEDBar(self):
        self.stepLEDBar.light(self.majorStep)
        self.majorStep += 1
        self.after(1000, self.updateLEDBar)
    
    def runSetupStep(self):
        if self.majorStep >= len(MIICRAFT_SETUP_STEP):
            # Setup is complete
            self.stepLEDBar.light(self.majorStep)
            self.complete()
            return
        stepInfo = MIICRAFT_SETUP_STEP[self.majorStep]
        stepMsg = stepInfo[0]
        stepCheck = stepInfo[1]
        stepCheckWait = stepInfo[2]
        stepSolutionMsg = stepInfo[3]
        stepSolution = stepInfo[4]
        stepSolutionWait = stepInfo[5]
        stepDialogList = stepInfo[6]
        wait = self.wait
        if self.minorStep == 0:
            # Show checking message and light LED
            if stepMsg is not None:
                self.message.configure(text=stepMsg)
            self.stepLEDBar.light(self.majorStep)
            self.minorStep = 1
        elif self.minorStep == 1:
            # Do checking
            result, self.microStep = stepCheck(self.microStep)
            if result == MIICRAFT_CTRL_SHOW_DIALOG_THEN_CHECK:
                # Show dialog
                self.dialogResult = 0
                stepDialog = stepDialogList[self.microStep]
                if stepDialog is not None:
                    popDialog = MiiCraftMsgDialog(self,
                                                   title=stepDialog[0],
                                                   message=stepDialog[1],
                                                   photo=stepDialog[2],
                                                   btnBoxType=stepDialog[3])
                    self.wait_window(popDialog)
                    reply = stepDialog[4]
                    self.microStep = reply(self.dialogResult)
                # Check again
                self.minorStep = 0
            elif result == MIICRAFT_CTRL_CHECK:
                # Check again
                self.minorStep = 0
            elif result == MIICRAFT_CTRL_SUCCESS:
                # Goto next major task
                self.majorStep += 1
                self.minorStep = 0
                self.microStep = 0
            elif result == MIICRAFT_CTRL_FAIL:
                # Try solution
                self.minorStep = 2
            elif result == MIICRAFT_CTRL_SHOW_DIALOG_THEN_EXIT:
                # Show dialog
                self.dialogResult = 0
                stepDialog = stepDialogList[self.microStep]
                if stepDialog is not None:
                    popDialog = MiiCraftMsgDialog(self,
                                                   title=stepDialog[0],
                                                   message=stepDialog[1],
                                                   photo=stepDialog[2],
                                                   btnBoxType=stepDialog[3])
                    self.wait_window(popDialog)
                    reply = stepDialog[4]
                    if reply is not None:
                        self.microStep = reply(self.dialogResult)
                # Leave setup
                self.parent.destroy()
            if stepCheckWait > 0:
                wait = stepCheckWait
        elif self.minorStep == 2:
            # Show solution message
            if stepSolutionMsg is not None:
                self.message.configure(text=stepSolutionMsg)
            self.minorStep = 3
        elif self.minorStep == 3:
            # Do solution then check again
            if stepSolution is not None:
                stepSolution()
            if stepSolutionWait > 0:
                wait = stepSolutionWait
            self.minorStep = 0
        self.after(wait, self.runSetupStep)
    
    def cancel(self):
        popDialog = MiiCraftMsgDialog(self,
                                       title="Warning",
                                       message=MIICRAFT_MSG_INTERRUPT_SETUP,
                                       photo=None, 
                                       btnBoxType=MIICRAFT_BTN_YESNO)
        self.wait_window(popDialog)
        if self.dialogResult == MIICRAFT_BTN_YES:
            self.parent.destroy()
    
    def complete(self):
        popDialog = MiiCraftMsgDialog(self,
                                       title="Completing the MiiCraft Setup",
                                       message=MIICRAFT_MSG_COMPLETE_SETUP,
                                       photo=None, 
                                       btnBoxType=MIICRAFT_BTN_YES)
        self.wait_window(popDialog)
        self.parent.destroy()


if __name__ == '__main__':
    root = Tk()
    root.title("Setup MiiCraft 3D Printer")
    root.iconbitmap(default='Sources\\Misc\\favicon.ico')
    root.resizable(False, False)
    app = MiiCraftSetupMainWidget(root)
    root.protocol("WM_DELETE_WINDOW", app.cancel)
    root.mainloop()
    sys.exit()
