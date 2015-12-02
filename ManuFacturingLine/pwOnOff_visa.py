#! /usr/bin/python
# PSU power on and off control
#version: v1.0
#Date: 11 Sep 2014
import os, sys
import xml.etree.ElementTree as ET
# ********************************************************************
# DEFINE USER'S PATHS
# ********************************************************************
from modules.instr.psu_bench_visa import *

XML_CFG_FILE = os.path.join(os.path.dirname(__file__),"config","PSUSetting.xml")
XML_PSU_TAG = "PSUNormalOp"
XML_PSU_ICAL_TAG = "PSUIcalOp"
XML_PSU_TAG_VMAX = "Vmax_V"
XML_PSU_TAG_VIMAX = "Imax_A"
XML_PSU_CFG_TAG = "PSUConfig"
XML_PSU_CFG_TAG_VISADDR = "VisaAddr"
#=====================================================================
class FactoryPower(VisaPsuBenchControl):
    """Controls the Power on or off to support factory automation"""
    def __init__(self):
        self.__logoutput__="PSU has not been switched ON\n"
        tree = ET.parse(XML_CFG_FILE)
        root = tree.getroot()
        #get Normal Op limits
        nlimits = root.find(XML_PSU_TAG)
        self.nVmax_V=float(nlimits.find(XML_PSU_TAG_VMAX).text)
        self.nImax_A=float(nlimits.find(XML_PSU_TAG_VIMAX).text)

        #get iCal Op limits
        ilimits = root.find(XML_PSU_ICAL_TAG)
        self.iVmax_V=float(ilimits.find(XML_PSU_TAG_VMAX).text)
        self.iImax_A=float(ilimits.find(XML_PSU_TAG_VIMAX).text)

        #get PSU config
        psuCfg = root.find(XML_PSU_CFG_TAG)
        self.visaAddr= psuCfg.find(XML_PSU_CFG_TAG_VISADDR).text

        #init base-class
        super(FactoryPower, self).__init__(self.visaAddr)
        self.__logoutput__+=VisaPsuBenchControl.__str__(self)+'\n'

    def PSUOn_P6V(self):
        #self.state = VisaPsuBenchControl.WasOn(self)
        if self.State():
            VisaPsuBenchControl.off(self)

        VisaPsuBenchControl.set(self,'P6V', self.nVmax_V, self.nImax_A)
        VisaPsuBenchControl.on(self)
        # This may take up to 0.5 sec!!!
        # t0_msec=int(round(time.time() * 1000))
        reading=VisaPsuBenchControl.read(self,'P6V')
        self.__logoutput__+="PSU is On \nPSU bench configuration: Vmax[V]=%s, Imax[A]=%s :: read back Voltage[V]=%s, Current[mA])=%s\n" % (self.nVmax_V, self.nImax_A, reading[0][0], reading[0][1])
        #t1_msec=int(round(time.time() * 1000))

    def PSUOn_P6V_iCal(self):
        #self.state = VisaPsuBenchControl.WasOn(self)
        if self.State():
            VisaPsuBenchControl.off(self)

        VisaPsuBenchControl.set(self,'P6V', self.iVmax_V, self.iImax_A)
        VisaPsuBenchControl.on(self)
        # This may take up to 0.5 sec!!!
        # t0_msec=int(round(time.time() * 1000))
        reading=VisaPsuBenchControl.read(self,'P6V')
        self.__logoutput__+="PSU is On \nPSU bench configuration: Vmax[V]=%s, Imax[A]=%s :: read back Voltage[V]=%s, Current[mA])=%s\n" % (self.iVmax_V, self.iImax_A, reading[0][0], reading[0][1])
        #t1_msec=int(round(time.time() * 1000))


    def PSUOff(self):
        self.__logoutput__ +="PSU is Off\n"
        VisaPsuBenchControl.off(self)

    def getLog(self):
        logOutput = self.__logoutput__
        self.__logoutput__=""
        return logOutput

    def __del__(self):
        VisaPsuBenchControl.close(self)

#=====================================================================
if __name__ == '__main__':
    myTest = FactoryPower()
   # myTest.State()
    myTest.PSUOn_P6V()
    raw_input("Check the setting and press [ENTER] to turn off")

    myTest.PSUOn_P6V_iCal()
    raw_input("Check the setting and press [ENTER] to turn off")

    myTest.PSUOn_P6V()
    raw_input("Check the setting and press [ENTER] to turn off")

    myTest.PSUOff()
    myTest.close()
    #myTest.State()
    print myTest.getLog()
