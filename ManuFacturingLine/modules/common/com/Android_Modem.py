'''
Created on 15 Sep 2013

@author: fsaracino
'''

import sys, os, socket, time, logging, re, subprocess


try: 
    os.environ['PL1TESTBENCH_ROOT_FOLDER']
except KeyError:
    os.environ['PL1TESTBENCH_ROOT_FOLDER'] = os.sep.join(os.path.abspath('').split(os.sep)[0:-3])
#    print ">> os.environ['PL1TESTBENCH_ROOT_FOLDER']=%s" % os.environ['PL1TESTBENCH_ROOT_FOLDER']
else:
    pass

sys.path.append(os.sep.join(os.environ['PL1TESTBENCH_ROOT_FOLDER'].split(os.sep)[:]+['common', 'config']))


from cfg_error import *

def adb_device_tag():
    logger=logging.getLogger('adb_modem_tag')
    adb=AdbCom()
    devtag = adb.device_tag()
    logger.info("Device tag : %s" % devtag)
    del adb
    return devtag

def adb_modem_reboot():
    logger=logging.getLogger('adb_modem_reboot')
    adb=AdbCom()
    adb.reboot()
    del adb
    
def adb_modem_off():
    logger=logging.getLogger('adb_modem_off')
    adb=AdbCom()
    adb.dut_off()
    del adb
    logger.info("Modem OFF")
    
    
def adb_modem_on():
    logger=logging.getLogger('adb_modem_on')
    adb=AdbCom()
    adb.dut_on()
    del adb
    logger.info("Modem ON")

     
def adb_modem_info():
    logger=logging.getLogger('adb_modem_info')
    adb=AdbCom()
    modeminfo=adb.dut_info()
    del adb
    return modeminfo


def adb_modem_config(rat, rfband, usimemu):
    logger=logging.getLogger('adb_modem_config')
    adb=AdbCom()
    adb.dut_config(rat, rfband, usimemu)
    del adb


def adb_airplanemode_off():
    logger=logging.getLogger('adb_airplanemode_off')
    adb=AdbCom()
    adb.dut_airplanemode_off()
    del adb

def adb_airplanemode_on():
    logger=logging.getLogger('adb_airplanemode_on')
    adb=AdbCom()
    adb.dut_airplanemode_on()
    del adb



class AdbCom(object):
    # List of supported devices 
    TAG_LGD802    = 'g2_open_com'
    TAG_CERES     = 'ceres'
    #TAG_SAMS4MINI = 'serranoltexx'
    DEVICE_TAG_L = [TAG_CERES, TAG_LGD802]
    
    AIRPLANE_MODE_OFF       = 0
    AIRPLANE_MODE_ON        = 1
    AIRPLANE_MODE           = { AIRPLANE_MODE_OFF:'OFF',  AIRPLANE_MODE_ON:'ON' }
    
    def __init__(self, tcp_port=5039, tcp_port_beanie=32766):
        self.host            = 'localhost'
        self.proto           = socket.AF_INET
        self.type            = socket.SOCK_STREAM
        self.maxchar         = 2048
        self.adb_port_at     = '/dev/ttySHM2'
        self.tcp_port        = tcp_port
        self.adb_port_beanie = '/dev/ttySHM4'
        self.tcp_port_beanie = tcp_port_beanie
        
        self.airplane_mode   = -1
        #self.config()
        self.hsocket         = -1
        self.modeminfo       = "None"


    # ------------------------------------------------------------------------------------------ #
    #                                     PRIVATE METHODS                                        #
    # ------------------------------------------------------------------------------------------ #       
    def _open(self):
        logger=logging.getLogger('AdbCom.open')
        try:
            logger.debug("Opening socket ...")
            self.hsocket = socket.socket(self.proto, self.type)
            self.hsocket.connect((self.host, self.tcp_port))
        except:
            logger.error("ADB connection failure on socket %s: errcode=%s, descr=%s" % (self.tcp_port, ERRCODE_SYS_SOCKET_CONN, error_table[ERRCODE_SYS_SOCKET_CONN]))
            sys.exit(ERRCODE_SYS_SOCKET_CONN)
        else:
            logger.debug("Socket Opened")


    def _close(self):
        logger=logging.getLogger('AdbCom._close')
        devtag=self.device_tag()      

        if devtag == self.TAG_CERES:
            self.hsocket.close()
            logger.debug("Socket closed")
            time.sleep(0.3)        
        else:
            pass


    # ------------------------------------------------------------------------------------------ #
    #                                     PUBLIC METHODS                                         #
    # ------------------------------------------------------------------------------------------ #       
    def device_tag(self):
        logger=logging.getLogger('AdbCom.device_tag')
        devtag = subprocess.Popen("adb shell getprop ro.product.name", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]            
        devtag=re.sub('[ |\t|\n\r]+','', devtag)
        if self.TAG_LGD802 in devtag :
            devtag = self.TAG_LGD802 
        elif self.TAG_CERES in devtag:
            devtag = self.TAG_CERES
        else:
            pass    
        logger.info("Device tag %s" % devtag)
        return devtag
    
    
    def reboot(self, tsec=60):
        logger=logging.getLogger('AdbCom.reboot')
        devtag=self.device_tag()
        logger.info("Rebooting modem")
        os.system('adb reboot')
        self.insert_pause(tsec)
        os.system('adb kill-server')
        os.system('adb start-server')
        os.system('adb wait-for-device')
        os.system('adb get-state')
        #os.system('adb shell svc power stayon true')
        os.system('adb devices')
 
        if devtag == self.TAG_CERES:
            logger.info("Waiting for ADB to start as root. It may take up to 2 minutes")

            #os.system('adb shell stop ril-daemon')
            os.system('adb root')         
            os.system('adb wait-for-device')
            os.system('adb remount')

            # Check if AT port exists
            cmd='adb shell ls %s ' % (self.adb_port_at)
            logger.debug(cmd)        
            if os.system(cmd):
                logger.error('/AT port %s not detected' % self.adb_port_at)
                return 1

            # Bridge AT port           
            cmd='adb forward tcp:%d dev:%s' % (self.tcp_port, self.adb_port_at) 
            logger.debug(cmd)
            os.system(cmd)
 
            # Chech if BEANIE port exists
            cmd='adb shell ls %s ' % (self.adb_port_beanie)
            logger.debug(cmd)        
            if os.system(cmd):
                logger.warning('Beanie port %s not detected' % self.adb_port_beanie)
                return 1
            
            cmd='adb forward tcp:%d dev:%s' % (int(self.tcp_port_beanie), self.adb_port_beanie)
            logger.debug(cmd)
            os.system(cmd)
                            
        logger.info("modem READY")
           
           
    def dut_off(self, tsec=60):
        logger=logging.getLogger('AdbCom.dut_off')
        devtag=self.device_tag()
        logger.info("Switching modem OFF")
        
        if devtag == self.TAG_CERES:
            cfg_modem_cmd_l = ['at+cfun=0']
            res = 0
            for cmd in cfg_modem_cmd_l: 
                (ret, msg)=self.send_command(cmd)
                if ret:
                    res = 1
                    break
            if res:
                logger.error('AT command (%s) failure' % cmd)
                sys.exit(ERRCODE_SYS_COM_FAILURE)        
        else:
			pass
            #self.dut_airplanemode_on()
            #self.reboot(tsec=60)
#        self.dut_airplanemode_on()
           
            
    def dut_on(self):
        logger=logging.getLogger('AdbCom.dut_on')
        devtag=self.device_tag()
        logger.info("Switching modem ON")
        
        if devtag == self.TAG_CERES:
#            self.dut_airplanemode_off()

            cmd_l = ['at+cfun=1']
            res = 0
            for cmd in cmd_l: 
                (ret, msg)=self.send_command(cmd)
                if ret:
                    res = 1
                    break
            if res:
                logger.error('AT command (%s) failure' % cmd)
                sys.exit(ERRCODE_SYS_COM_FAILURE)        
        else:
            logger.info("Device %s ready for reboot" % devtag)
            self.reboot(tsec=60)
        
        
    def dut_config(self, rat, rfband, usimemu):
        logger=logging.getLogger('AdbCom.dut_config')
        
        devtag=self.device_tag()
        logger.info("Configuring modem : %s" % devtag)
        
        if devtag == self.TAG_CERES:
            # Prepare command list
            if (rat =='LTE'):
                cmd_l = [ r'at+cfun=0', 
                          r'at%inwmode=0,E,1', 
                          r'at%%inwmode=1,E%s,1' % (rfband) , 
                          r'at%%isimemu=%s' % (usimemu)]
            elif (rat =='WCDMA'):
                cmd_l = [ r'at+cfun=0', 
                          r'at%inwmode=0,U,1', 
                          r'at%%isimemu=%s' % (usimemu)]
            elif (rat =='GSM'):     
                cmd_l = [ r'at+cfun=0', 
                          r'at%inwmode=0,G,1', 
                          r'at%%isimemu=%s' % (usimemu)]
            else:     
                logger.error('Invalid RAT %s' % (rat))
                sys.exit(ERRCODE_TEST_PARAM_INVALID)

            # Send command list    
            res = 0
            for cmd in cmd_l: 
                (ret, msg)=self.send_command(cmd)
                if ret:
                    res = 1
                    break
            if res:
                logger.error('AT command (%s) failure' % cmd)
                sys.exit(ERRCODE_SYS_COM_FAILURE)        
        else:
            logger.info("Nothing to do")


    def dut_info(self):
        logger=logging.getLogger('AdbCom.dut_info')
        devtag=self.device_tag()
        if devtag == self.TAG_CERES:
            cmd_l = [ r'at+cfun=0', 
                      r'AT%IDBGTEST']
            res = 0
            for cmd in cmd_l: 
                (ret, msg)=self.send_command(cmd)
                if ret:
                    res = 1
                    break
            if res:
                logger.error('AT command (%s) failure' % cmd)
                sys.exit(ERRCODE_SYS_COM_FAILURE)
            else:
                modeminfo=msg      
        else:
            modeminfo=" Platform : %s " % devtag
        return modeminfo


    def  dut_airplanemode_on(self, timeout=3):
        logger=logging.getLogger('AdbCom.dut_airplanemode_on')
        
        res=0 
        
        num_iter      = 0
        NUM_ITER_MAX  = timeout
        POLL_INTERVAL = 1
        
        # Retirve AIRPLANE MODE status
        airplane_mode = subprocess.Popen("adb shell settings get global airplane_mode_on", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]
        airplane_mode = int(re.match(r"[0-1].*$", airplane_mode).group(0))
        
        if airplane_mode == self.AIRPLANE_MODE_OFF:
            while (num_iter < NUM_ITER_MAX):
                logging.debug("Toggling AIRPLANE MODE to %s. Iteration %s of %s" % (self.AIRPLANE_MODE_ON, num_iter+1, NUM_ITER_MAX))
                # Toggle status
                subprocess.Popen("adb shell settings put global airplane_mode_on 1", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]
                subprocess.Popen("adb shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]
                time.sleep(POLL_INTERVAL)
                # Read back and check the status                
                airplane_mode = subprocess.Popen("adb shell settings get global airplane_mode_on", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]
                #airplane_mode = re.sub('[ |\t|\n|\r]+','', airplane_mode)
                airplane_mode = int(re.match(r"[0-1].*$", airplane_mode).group(0))

                time.sleep(POLL_INTERVAL)                
                if airplane_mode == self.AIRPLANE_MODE_ON: break
                # Next iteration 
                num_iter += 1
                            
        if num_iter == NUM_ITER_MAX:
            logger.error("FAILURE switching airplane mode ON")
            res = 1
            #sys.exit(ERRCODE_SYS_DUT_TIMEOUT)
        else:
            logger.debug("Airplane mode is %s" % self.AIRPLANE_MODE[airplane_mode])
        return res
 

    def  dut_airplanemode_off(self, timeout=3):
        logger=logging.getLogger('AdbCom.dut_airplanemode_off')
        
        res=0 
        
        num_iter      = 0
        NUM_ITER_MAX  = timeout
        POLL_INTERVAL = 1
        
        # Retirve AIRPLANE MODE status
        airplane_mode = subprocess.Popen("adb shell settings get global airplane_mode_on", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]
        airplane_mode = int(re.match(r"[0-1].*$", airplane_mode).group(0))

        if airplane_mode == self.AIRPLANE_MODE_ON:
            while (num_iter < NUM_ITER_MAX):
                logger.debug("Toggling AIRPLANE MODE to %s. Iteration %s of %s" % (self.AIRPLANE_MODE_OFF, num_iter+1, NUM_ITER_MAX))
                # Toggle status
                subprocess.Popen("adb shell settings put global airplane_mode_on 0", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]
                subprocess.Popen("adb shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]
                time.sleep(POLL_INTERVAL)
                # Read back and check the status                
                airplane_mode = subprocess.Popen("adb shell settings get global airplane_mode_on", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate()[0]
                airplane_mode = int(re.match(r"[0-1].*$", airplane_mode).group(0))
                time.sleep(POLL_INTERVAL)                
                if airplane_mode == self.AIRPLANE_MODE_OFF: break
                # Next iteration 
                num_iter += 1
                            
        if num_iter == NUM_ITER_MAX:
            logger.error("FAILURE switching airplane mode ON")
            res = 1
            #sys.exit(ERRCODE_SYS_DUT_TIMEOUT)
        else:
            logger.debug("Airplane mode is %s" % self.AIRPLANE_MODE[airplane_mode])
        return res
 

    def dut_nverase(self):
        logger=logging.getLogger('AdbCom.dut_nverase')
        report=""

        devtag=self.device_tag()
        if devtag == self.TAG_CERES:
            cmd_l = [ r'at+cfun=0',
                      #r'at+cgsn',
                      r'at%mode=2',
                      r'at%nverase',
                      #r'at%imei=a,b,...',
                      r'at%mode=0']            
            res = 0
            for cmd in cmd_l: 
                (ret, msg)=self.send_command(cmd)
                if ret:
                    res = 1
                    break
                    report += ("Response for CMD(%s) : CODE = %s  MSG = %s" % (cmd, ret, msg))
            if res:
                logger.error('AT command (%s) failure' % cmd)
                sys.exit(ERRCODE_SYS_COM_FAILURE)
            logger.info("NVERASE completed")        
        else:
            pass
        
        return report
                 
                 
    def send_command(self, cmd_str, rsp_str ='OK'):
        self._open()
        logger=logging.getLogger('AdbCom.send_command')
        logger.info("Sending (%s), Expecting (%s)" % (cmd_str, rsp_str))
        
        tsleep = 1
        if cmd_str == "at%itr:?": tsleep = 10
        
        self.hsocket.send((cmd_str+'\r\n').encode())
        
        time.sleep(tsleep)
        recv_str = self.hsocket.recv(self.maxchar)
        #print recv_str 
        reg_expr = r'\b' + re.escape(rsp_str) + r'\b'
        matchObj = re.search (reg_expr, recv_str, re.M|re.I)
        status=-1
        if matchObj:
            text_str = "Response"
            logger.debug("%-15s:\t%s" %(text_str, matchObj.group()))
            status=0
        else:
            logger.debug("Expected STR response not found")
            text_str ="Response"
            logger.debug("%-15s:\t%s" %(text_str, recv_str))
            status=1
        self._close()    
        return (status, recv_str)
    
        
    def insert_pause(self, tsec=10, step=5):        
        logger=logging.getLogger('insert_pause')
        logger.debug("Pause %s [sec]" % tsec)
        remaining_time=tsec
        while remaining_time > 0:
            time.sleep(step)
            remaining_time -= step
            logger.info("remaining time : %s [sec]" % remaining_time)
    

            


    
if __name__ == '__main__':

    import sys, os
    sys.path.append(os.sep.join(os.path.abspath('..').split(os.sep)[:]+['config']))
    
    from cfg_multilogging import cfg_multilogging
        
    cfg_multilogging('DEBUG', 'adbtest.LOG')    
    logger=logging.getLogger('Android_Modem')
    
    devicetag=adb_device_tag()
    adb_modem_reboot()
    
    modeminfo=adb_modem_info()
    adb_modem_config(rat='LTE', rfband=1, usimemu=0)
    adb_modem_on()

    adb_airplanemode_on()
    raw_input("Press [ENTER]")
    adb_airplanemode_off()
    
    adb_modem_off()
    
    

    logger.info("END")
    
