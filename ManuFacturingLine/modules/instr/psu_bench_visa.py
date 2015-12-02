#! /usr/bin/env python

#######################################################################################################################
#
# $Id: //swtools/main.br/manufacturing/tools/SmokeTest/modules/instr/psu_bench_visa.py#2 $
# $Author: yongz $
# $Revision: #2 $
# $DateTime: 2015/01/22 14:54:28 $
#
#######################################################################################################################

import os, time, re, sys, logging, visa


def Resource():
       rm = visa.ResourceManager()
       print rm.list_resources()

class VisaPsuBenchControl(object):
    PSU_NAME_L         = ['E3631A_0', 'E3631A_1']
    PSU_MEAS_CHANNEL_L = ['P6V', 'P25V', 'N25V']
    "Visa PSU clase"
    def __init__(self, VisaAddres):
        self.rm = visa.ResourceManager()
        self.addr = VisaAddres
        self.inst = self.rm.open_resource(self.addr)
        self.ison = False
        self.State()

    def State(self):
       self.name = self.inst.query("OUTPut:STATe?")
       if int(self.name) == 0:
            print "OFF"
            self.ison= False
       else:
            print "ON"
            self.ison = True
       return self.ison

    def WasOn(self):
        return self.ison

    def close(self):
        self.rm.close

    def reset(self):
        self.inst.write("*rst")                  # this sets all output voltages to zero
        self.inst.write("*cls")

    def read(self, channel):
        meas = []
        logging.debug("Selected channel for measurement: %s" % channel)
        if not channel in self.PSU_MEAS_CHANNEL_L:
            return meas
        # Read voltage
        voltage = self.inst.query_ascii_values("MEAS:VOLT:DC? %s" % channel)[0]

        # Read current
        current=self.inst.query_ascii_values("MEAS:CURR:DC? %s" % channel)[0]*1000
        self.curr_min=current
        self.curr_max=current
        self.curr_avrg=current
        self.curr_dev=0
        meas.append((voltage, current))
        return meas

    def set(self, channel, voltage, current):
        if channel in self.PSU_MEAS_CHANNEL_L:
            self.inst.write("INST %s" % channel)
            self.inst.write("CURR %s A" % current)
            self.inst.write("VOLT %s V" % voltage)

    def on(self):
         self.inst.write("OUTP ON")
         self.State()

    def off(self):
        self.inst.write("OUTP OFF")
        self.State()

    def __str__(self):
       return self.inst.query("*IDN?")


def test():
    print Resource()
    mypsu = VisaPsuBenchControl('GPIB1::5::INSTR')
    #mypsu.open()
    mypsu.set('P6V',3.8,5)
    mypsu.State()
    mypsu.on()
    reading=mypsu.read('P6V')
    print reading
    mypsu.State()
    mypsu.off()
    mypsu.State()
    mypsu.close()


#######################################################################################################################

if __name__ == '__main__':
    test()

