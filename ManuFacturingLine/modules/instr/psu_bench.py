#! /usr/bin/env python

#######################################################################################################################
#
# $Id: //swtools/main.br/manufacturing/tools/SmokeTest/modules/instr/psu_bench.py#3 $
# $Author: rapfeldorfer $
# $Revision: #3 $
# $DateTime: 2014/10/16 12:09:56 $
#
#######################################################################################################################

import os, time, re, sys, logging

sys.path.append(os.sep.join(os.path.abspath('..').split(os.sep)[:]+['common', 'config']))

from vxi_11 import vxi_11_connection



class Agilent_E3631A(vxi_11_connection):
    default_lock_timeout=5000
    #idn_head="HEWLETT-PACKARD,E3631A,0,2.1-5.0-1.0"



def switch_off_psu(psu_gwip, psu_gpib, psu_name='E3631A_0'):
    psu_bench=PsuBenchControl(psu_name=psu_name, psu_gwip=psu_gwip, psu_gpib=psu_gpib)
    psu_bench.off()
    psu_bench.close()

def switch_off_on_psu(psu_gwip, psu_gpib, psu_name='E3631A_0', Vmax_V=3.8, Imax_A=5, time_secs=30):
    psu_bench=PsuBenchControl(psu_name=psu_name, psu_gwip=psu_gwip, psu_gpib=psu_gpib)
    psu_bench.off()
    time.sleep(2)
    psu_bench.on()
    psu_bench.set('P6V', Vmax_V, Imax_A)
    psu_bench.close()
    time.sleep(time_secs)


class PsuBenchControl(object):
    PSU_NAME_L         = ['E3631A_0', 'E3631A_1']
    PSU_MEAS_CHANNEL_L = ['P6V', 'P25V', 'N25V']

    def __init__(self, psu_gwip, psu_gpib, psu_name='E3631A_0', buffsize=10):

        #if not psu_name in self.PSU_NAME_L:
        #    raise Exception('must use -p [ %s ]' % ' | '.join(sorted(self.PSU_NAME_L)))

        self.psu={ psu_name: {'IP': r'%s' % psu_gwip, 'GPIB_PORT' : r'gpib0,%s' % psu_gpib}}
        self.open(psu_name)
        self.buffsize=buffsize
        self.voltage_buff=[]
        self.current_buff=[]
        self.curr_min=0
        self.curr_avrg=0
        self.curr_max=0
        self.curr_dev=0

    def open(self, psu_name):
        self.name = psu_name
        self.gwip = self.psu[psu_name]['IP']
        self.gpib_addr = self.psu[psu_name]['GPIB_PORT']
        self.dev = Agilent_E3631A(host=self.gwip, device=self.gpib_addr, timeout=2, device_name=self.name, raise_on_err=1)
        logging.info("Connected to PSU: name=%s, gwip=%s, port=%s" % (self.name, self.gwip, self.gpib_addr))
        self.reset()
        logging.debug("Reset completed")

    def reset(self):
        self.dev.write("*rst")                  # this sets all output voltages to zero
        self.dev.write("*cls")

    def read(self, channel):
        meas = []
        logging.debug("Selected channel for measurement: %s" % channel)
        if not channel in self.PSU_MEAS_CHANNEL_L:
            logging.error('PsuBenchControl.read(): Invalid measurement channel %s. Skipping measurements' % (channel))
            return meas

        # Read voltage
        #self.dev.write("INST %s" % channel)
        #self.dev.write("MEAS:VOLT:DC?")
        self.dev.write("MEAS:VOLT:DC? %s" % channel)
        reading = self.dev.read()
        voltage = float(reading[2])

        # Read current
        #self.dev.write("MEAS:CURR:DC?")
        self.dev.write("MEAS:CURR:DC? %s" % channel)
        reading = self.dev.read()
        current = int(float(reading[2]) * 1000)
        logging.info("%s channel %s : voltage=%05.3fV, current=%.0fmA" % (self.name, channel, voltage, current))
        self.curr_min=current
        self.curr_max=current
        self.curr_avrg=current
        self.curr_dev=0
        meas.append((voltage, current))
        return meas

    def set(self, channel, voltage, current):
        if channel in self.PSU_MEAS_CHANNEL_L:
            logging.info("%s channel %s : setting voltage=%05.3fV, current=%05.3fmA" % (self.name, channel, float(voltage), float(current)))
            self.dev.write("INST %s" % channel)
            self.dev.write("CURR %s A" % current)
            self.dev.write("VOLT %s V" % voltage)
        else:
            logging.error('PsuBenchControl.set(): Invalid channel %s. Skipping configuration ' % (channel))

    def on(self):
        logging.info("Setting outputs of psu_voltmeter \"%s\" to ON" % (self.name))
        self.dev.write("OUTP ON")

    def off(self):
        logging.info("Setting outputs of psu_voltmeter \"%s\" to OFF" % (self.name))
        self.dev.write("OUTP OFF")

    def close(self):
        logging.info("Closing PSU connection name = %s" % (self.name))
        self.dev.disconnect

    def __str__(self):
        return "PSU name   : {0}\nGateway IP : {1}\nGPIB Addr  : {2}".format(self.name, self.gwip, self.gpib_addr)

#######################################################################################################################

if __name__ == '__main__':

    import sys, os
    #sys.path.append(os.sep.join(os.path.abspath('..').split(os.sep)[:]+['config']))
    #from threading import Thread

    from cfg_multilogging import cfg_logger_root

    logger_00 = cfg_logger_root('DEBUG', 'psu_bench_fs.LOG')
    logger_00.debug('START')
    Vmax_V=3.8
    Imax_A=5
    psuname='E3631A_0'
    psugwip=r'10.21.141.145'
    psugpib=5
    psu_bench=PsuBenchControl(psu_name=psuname, psu_gwip=psugwip, psu_gpib=psugpib)
    print psu_bench

    psu_bench.on()
    psu_bench.set('P6V', Vmax_V, Imax_A)
    raw_input("Check che setting and press [ENTER]")

    # This may take up to 0.5 sec!!!
    t0_msec=int(round(time.time() * 1000))
    reading=psu_bench.read('P6V')
    logging.info("PSU bench configuration: Vmax[V]=%s, Imax[A]=%s :: read back Voltage[V]=%s, Current[mA])=%s" % (Vmax_V, Imax_A, reading[0][0], reading[0][1]))

    t1_msec=int(round(time.time() * 1000))
    logging.info("Elapsed time %s [msec]" % (t1_msec-t0_msec))

    psu_bench.off()
    psu_bench.close()


    logger_00.debug('END')


