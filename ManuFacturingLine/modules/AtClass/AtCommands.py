#-------------------------------------------------------------------------------
# Name:        AtCommands
# Purpose:
#
# Author:      yongz
#
# Created:     26/11/2014
# Copyright:   (c) yongz 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, sys, serial,re,time,serial,logging,re

from modules.common.com.Serial_ComPortDet import auto_detect_port
from modules.common.config.cfg_error import *
import _winreg as winreg
import itertools

class myAndroidModem:
    """Anriod port forwarding class"""
    def __init__(self, port_tag, timeout=3):
        self.timeout   = timeout


class mySerialAtModem:
    """Seral port class"""
    def __init__(self, port_tag, timeout=3):
        self.timeout   = timeout
        self.port_tag   = port_tag
        self.modeminfo = "N/A"
        try:
            self.open()
        except serial.SerialException, e:
            print("Unable to open port %s: %s" % (port_tag, e))
            sys.exit(ERRCODE_SYS_SERIAL_CONN)

        print("AT port %s open" % (port_tag))


    def open (self):
        kwargs = { 'baudrate': 9600, 'bytesize': 8, 'parity': 'N', 'stopbits': 1, 'timeout': self.timeout }
        is_url = isinstance(self.port_tag, str) and '://' in self.port_tag
        if is_url:
            self.hdlr = serial.serial_for_url(self.port_tag, **kwargs)
        else:
            self.hdlr = serial.Serial(self.port_tag, **kwargs)

    def swreset(self, pause=20):
        cmd_str=r'at%ireset'
        logging.debug("(%s, return=%s)" % (cmd_str, self.send_cmd(cmd_str)))
        logging.info("Waiting for %s [sec] DUT booting " % pause)
        time.sleep(pause)


    def close(self):
        logger=logging.getLogger('Serial_Modem.close')
        self.hdlr.close()
        logger.debug("Closed COM %s" % self.port_tag)


    def send_cmd(self, cmd_str=r'AT', rsp_str ='OK'):
        """
        Send AT command, cmd_str
        Check response, rsp_str
        """
        logger=logging.getLogger('Serial_Modem.send_cmd')
        try:
            text_str = "AT command"
            logger.debug("%-15s:\t%s" %(text_str, cmd_str))
            cmd_str = cmd_str + '\r\n'
            self.hdlr.write(cmd_str)      # write a string
            if not 'ireset' in cmd_str:
                self.hdlr.write(cmd_str)      # write a string
                reg_expr = r'\b' + re.escape(rsp_str) + r'\b'
                response, matchObj = self.read_resp(reg_expr)

                if matchObj:
                    text_str = "Response"
                    logger.debug("%-15s:\t%s" %(text_str, matchObj.group()))
                    return (0, response)
                else:
                    logger.debug("Expected STR response not found")
                    text_str ="Response"
                    logger.debug("%-15s:\t%s" %(text_str, response))
                    return (1, response)
            else:
                self.hdlr.write(cmd_str)      # write a string
                logger.info("Modem RESET in progress...")
                return (0, "N/A for RESET")

        except serial.SerialException, e:
            print("Unable to send command to port %s: %s" % (self.port_tag, e))
            sys.exit(ERRCODE_SYS_SERIAL_CONN)
        else:
            pass


    def read_resp(self, reg_expr):
        '''Read from the serial device until a string matching reg_expr is
        found, or the timeout elapses.'''
        iteration=0
        resp_buf = ""
        expiry = time.time() + self.timeout
        while expiry - time.time() > 0:
            iteration +=1
            #print "Iteration %d" % iteration
            _s = self.hdlr.read(2**16)
            resp_buf += _s
            matchObj = re.search (reg_expr, resp_buf, re.M|re.I)
            if matchObj:
                break
            time.sleep(0.1)

        return resp_buf, matchObj

class BasicAtCommads(mySerialAtModem):
    """generic mode class"""
    def __init__(self, port_tag, timeout=0.5):
        #init base-class
        mySerialAtModem.__init__(self, port_tag, timeout)

    def _send_cmd(self, cmd_str):
        ret, msg = mySerialAtModem.send_cmd(self,cmd_str)
        return  ret, msg

    def mode(self,mode):
        self._send_cmd(r'at%mode='+str(mode))

    def getSWversion(self):
        self._send_cmd(r'at+gmr')

    def getProductCfg(self):
        self._send_cmd( r'at%idmpcfg=productConfig,2')

    def getSerialNo(self):
        ret, msg = self._send_cmd( r'at%iparam')
        m = re.findall('(?<=:\s).*',msg)
        out = re.sub(r"[\x01-\x1F\x7F]", "", m[0])
        return out

class RadioAtCommads(mySerialAtModem):
    """At command used for radio control class"""
    def __init__(self, port_tag, timeout=0.5):
        #init base-class
        mySerialAtModem.__init__(self, port_tag, timeout)

    def _send_cmd(self, cmd_str):
        ret, msg = mySerialAtModem.send_cmd(self,cmd_str)
        return  ret, msg

    def mode(self,mode):
        self._send_cmd(r'at%mode='+str(mode))

    def bands(self):
        self.mode(0)
        self._send_cmd(r'at%inwmode?')

    def Band3GTest_RxOn(self,band):
        self._send_cmd( r'at%3gband=' + str(band))
        self._send_cmd( r'at %3grxenable=m,on')
        self._send_cmd( r'at %3grxenable=m,off')

    def Band2GTest_RxOn(self,band):
        self._send_cmd( r'at %gsmband='+str(band))
        self._send_cmd( r'at %gsmenable=on')
        self._send_cmd( r'at %gsmenable=off')

    def BandLteTest_RxOn(self,band):
        self._send_cmd( r'at%lteband=' + str(band))
        self._send_cmd( r'at %rfrxenable=m,on')
        self._send_cmd( r'at %rfrxenable=m,off')

class myUsbRelay:
    """usb prot class for usb relay board"""
    def __init__(self, port_tag):
        self.ser = serial.Serial(port_tag)  # open serial port

    def getport(self):
        path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        except WindowsError:
            raise IterationError

        for i in itertools.count():
            try:
                val = winreg.EnumValue(key, i)
                print val
                #yield (str(val[1]), str(val[0]))
            except EnvironmentError:
                break

    def usbrelayOn(self):
        self.ser.write("\xFF\x01\x01")

    def usbrelayOff(self):
        self.ser.write("\xFF\x01\x00")

    def close(self):
        self.ser.close()

#-------------------------------------------------------------------------------
def test():
    atPortNum = auto_detect_port("Modem_port")
    if atPortNum is None:
        print "no AT port detected"
        return 0
    else : print "Selected AT mode port : %s " % atPortNum
    atModem = BasicAtCommads(atPortNum)
    msg = atModem.getSerialNo()
    print "this is "+ msg
    atModem.close()
    return 1

def test1():
    sw = myUsbRelayModem(161)
    sw.usbrelayOn()
    sw.close()

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    test1()
