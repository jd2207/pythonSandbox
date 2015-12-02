#! /usr/bin/python
# PSU power on and off control
#version: v1.0
#Date: 11 Sep 2014
import os, sys
import xml.etree.ElementTree as ET
# ********************************************************************
# DEFINE USER'S PATHS
# ********************************************************************
from modules.instr.psu_bench import *

XML_CFG_FILE = os.path.join(os.path.dirname(__file__),"config","PSUSetting.xml")
XML_PSU_TAG = "PSUNormalOp"
XML_PSU_TAG_VMAX = "Vmax_V"
XML_PSU_TAG_VIMAX = "Imax_A"
XML_PSU_CFG_TAG = "PSUConfig"
XML_PSU_CFG_TAG_NAME = "Name"
XML_PSU_CFG_TAG_IP = "IPAddr"
XML_PSU_CFG_TAG_GPIB = "GPIB"
#=====================================================================
class FactoryPower(PsuBenchControl):
    """Controls the Power on or off to support factory automation"""
    def __init__(self):
        self.__logoutput__="PSU has not been switched ON\n"
        tree = ET.parse(XML_CFG_FILE)
        root = tree.getroot()
        #get limits
        limits = root.find(XML_PSU_TAG)
        self.Vmax_V=float(limits.find(XML_PSU_TAG_VMAX).text)
        self.Imax_A=float(limits.find(XML_PSU_TAG_VIMAX).text)

        #get PSU config
        psuCfg = root.find(XML_PSU_CFG_TAG)
        self.psuname= psuCfg.find(XML_PSU_CFG_TAG_NAME).text
        self.psugwip= psuCfg.find(XML_PSU_CFG_TAG_IP).text
        self.psugpib= psuCfg.find(XML_PSU_CFG_TAG_GPIB).text

        #init base-class
        super(FactoryPower, self).__init__(self.psugwip, self.psugpib,self.psuname)
        self.__logoutput__+=PsuBenchControl.__str__(self)+'\n'

    def PSUOn(self):
        PsuBenchControl.on(self)
        PsuBenchControl.set(self,'P6V', self.Vmax_V, self.Imax_A)
        # This may take up to 0.5 sec!!!
        t0_msec=int(round(time.time() * 1000))
        reading=PsuBenchControl.read(self,'P6V')
        self.__logoutput__+="PSU is On \nPSU bench configuration: Vmax[V]=%s, Imax[A]=%s :: read back Voltage[V]=%s, Current[mA])=%s\n" % (self.Vmax_V, self.Imax_A, reading[0][0], reading[0][1])
        t1_msec=int(round(time.time() * 1000))

    def PSUOff(self):
        self.__logoutput__ +="PSU is Off\n"
        PsuBenchControl.off(self)

    def getLog(self):
        logOutput = self.__logoutput__
        self.__logoutput__=""
        return logOutput

    def __del__(self):
        PsuBenchControl.close(self)
                
#=====================================================================
if __name__ == '__main__':
    myTest = FactoryPower()
    myTest.PSUOn()
    raw_input("Check the setting and press [ENTER] to turn off")
    myTest.PSUOff()
    print myTest.getLog()
