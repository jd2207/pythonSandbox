#-------------------------------------------------------------------------------
# Name:        comPortDet.py
# Purpose:
#
# Author:      Joash Robinson, Francesco Saracino
#
# Created:     16/04/2014
# Copyright:   (c) NVIDIA 2014
#-------------------------------------------------------------------------------
import os
import sys
import re
import logging
import time
from modules import serial as serial

if sys.platform in ['cygwin', 'win32']:
    import _winreg as winreg


try:
    os.environ['PL1TESTBENCH_ROOT_FOLDER']
except KeyError:
    os.environ['PL1TESTBENCH_ROOT_FOLDER'] = os.sep.join(os.path.abspath(__file__).split(os.sep)[0:-4])
    #print ">> os.environ['PL1TESTBENCH_ROOT_FOLDER']=%s" % os.environ['PL1TESTBENCH_ROOT_FOLDER']
else:
    pass

#sys.path.append(os.sep.join(os.environ['PL1TESTBENCH_ROOT_FOLDER'].split(os.sep)[:]+['lib', 'common', 'config']))


from modules.common.config.cfg_error import *



def extract_portnum(portNumStr):
    portNum = None
    m_obj = re.search(r'COM(\d+)', portNumStr, re.I)
    if m_obj:
        portNum = m_obj.group(1)
        return int(portNum)
    else:
        portNum = None
    return portNum


def auto_detect_port_win(portName, suppressPrint):
    logger=logging.getLogger('auto_detect_port_win')

    usb_enum_dict = {'MODEM_PORT':'0', 'AT_PORT':'1', 'LOGGING_PORT':'2'}

    try:
        enum_instanceVal = usb_enum_dict[portName.upper()]
    except KeyError:
        logger.warning("%s is not supported" % portName)
        return None
    try:
        path = 'SYSTEM\\CurrentControlSet\\Services\\usbser\\Enum'
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    except WindowsError:
        logger.error("not able to detect port")
        return None

    try:
        value, dummy = winreg.QueryValueEx (hkey, enum_instanceVal)
        vid_pid = value.split('\\')[1]  # get vid and pid from value list
        instance = value.split('\\')[2] # get vid/pid instance from value list
        # now use the above values to get the correct entry into USB enum list
        # of the windows registry
        deviceParamsPath = os.path.join('SYSTEM\CurrentControlSet\Enum\USB',
                                        vid_pid, instance, 'Device Parameters' )

        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, deviceParamsPath)
        portStr = ""
        portStr, dummy = winreg.QueryValueEx (hkey, "PortName")
    except Exception:
        #print traceback.format_exc()
        if not suppressPrint:
            logger.info("Auto detection of %s com port failed" % portName)
        else:
            pass
        return None

    if portStr:
        portNum = extract_portnum(portStr) - 1
    else:
        return None

    if not suppressPrint:
        logger.info("Auto detection SUCCESS port: %s" % portStr)

    return portNum



def auto_detect_port_linux(portName):
    import subprocess

    logger=logging.getLogger('auto_detect_port_linux')

    portName = portName.upper()
    portMap  = { 'MODEM_PORT':0, 'AT_PORT':1, 'LOGGING_PORT':2 }

    try:
        portIndex = int(portMap[portName])
    except:
        logger.error("%s is unsupported" %portName)
        return None

    # Retrieve the list of the available ttyACM ports
    devnull = open(os.devnull, 'wb')
    proc    = subprocess.Popen("ls /dev/ttyACM*", shell=True, stdout=subprocess.PIPE, stderr=devnull)
    cmd_out = proc.stdout.readlines()
    devnull.close()
    if (not cmd_out):                                            # If empty no ttyUSB detected
        logger.debug('No active ttyACM detected')
        return None

    # Remove the newline at the end
    ttyACM_l =[x.rstrip(os.linesep) for x in cmd_out]
    if 0: logger.debug('ttyACM_l          : %s' % ttyACM_l)

    # Check and select the ttyUSB ports that can be opened
    ttyACM_active_l=[]
    ttyACM_selected=None
    for ttyACM in ttyACM_l:
        try:
            ser = serial.Serial(ttyACM, timeout=10)
            if 0: logger.debug("Found active %s" % ttyACM)
            ser.close()
            ttyACM_active_l.append(ttyACM)
        except serial.SerialException:
            logger.debug("Cannot open %s" % ttyACM)
            continue

    logger.debug('ttyACM_active_l   : %s' % ttyACM_active_l)

    # Select the port
    try:
        ttyACM_selected=ttyACM_active_l[portIndex]
    except IndexError:
        ttyACM_selected=None
        logging.error('%s could not be detected' % portName)
    else:
        logger.debug("Port Name: %s, Map: %s" %(portName, ttyACM_selected))

    return ttyACM_selected



def auto_detect_port(portName, suppressPrint=0):
    logger=logging.getLogger('auto_detect_port')

    logger.debug("Auto port detection of %s" %portName)

    if sys.platform in ['cygwin', 'win32']:
        portNum = auto_detect_port_win(portName, suppressPrint)
        return portNum

    elif sys.platform in ['linux', 'linux2', 'linux3']:
        portNum = auto_detect_port_linux(portName)
        return portNum
    else:
        logger.error("Not supported")
        return None



def poll_for_port(portName="Modem_port", timeout_sec=60, poll_time_sec=5):
    logger=logging.getLogger('poll_for_port')
    remaining_time = timeout_sec
    found_port   = None
    logger.debug("timeout set to %s [sec] : " % remaining_time)

    while remaining_time > 0:
        time.sleep(poll_time_sec)
        remaining_time -= poll_time_sec
        logger.debug("remaining time %s" %remaining_time)
        try:
            found_port=auto_detect_port(portName=portName, suppressPrint=1)
            if not found_port is None: break
        except:
            continue
    return found_port


if __name__ == '__main__':

    from cfg_multilogging import cfg_multilogging
    cfg_multilogging('DEBUG', 'Serial_ComPortDet.LOG')
    logger=logging.getLogger('Serial_ComPortDet')

    if 0:
        modemPortNum = auto_detect_port("Modem_port")
        if modemPortNum is None:
            logger.error("MODEM port not found")
        logger.info("Selected MODEM port : %s " % modemPortNum)

        atPortNum = auto_detect_port("at_port")
        if atPortNum is None:
            logger.error("AT port not found")
        logger.info("Selected AT port : %s " % atPortNum)

    if 1:
        if poll_for_port(portName="Modem_port") is None:
            logger.error("No active serial port found")

        if poll_for_port(portName="at_port") is None:
            logger.error("No active serial port found")

        if poll_for_port(portName="Logging_port") is None:
            logger.error("No active serial port found")



