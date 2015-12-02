#!/usr/bin/env python
# -*- coding: cp936 -*-
#################################################################################################
#  NVIDIA, Corporation
#  Copyright (c) 2014
#  All rights reserved
#################################################################################################
'''
smokeTst.py {0}: smoke test PSU control

Usage:
      python smokeTst.py
'''
version = "v1.2"
__doc__=__doc__.format(version)

#################################################################################################
import os, sys
import xml.etree.ElementTree as ET

# ********************************************************************
# DEFINE USER'S PATHS
# ********************************************************************
from modules.instr.psu_bench import *

XML_CFG_FILE = os.path.join(os.path.dirname(__file__),"config","PSUSetting.xml")
XML_PSU_TAG = "SmokeTest"
XML_PSU_TAG_VMAX = "Vmax_V"
XML_PSU_TAG_IMAX = "Imax_A"
XML_PSU_TAG_STEPS = "NoOfStep"
XML_PSU_TAG_PASS_FAIL = "Pass_Fail_Limit_mA"
XML_PSU_TAG_OPEN_CIR = "Open_circuit_limit_mA"
XML_PSU_CFG_TAG = "PSUConfig"
XML_PSU_CFG_TAG_NAME = "Name"
XML_PSU_CFG_TAG_IP = "IPAddr"
XML_PSU_CFG_TAG_GPIB = "GPIB"
XML_PSU_CFG_TAG_DELAY = "MinDelay_mS"
#=====================================================================
CurrentDelta_mA = 5 #hysteresis margin as the metre will alwasys limit the current output bellow the Imax setting
#this function returns a tuple (0/1,"String here")
def smoketest():
    tree = ET.parse(XML_CFG_FILE)
    root = tree.getroot()
    #get the limits
    limits = root.find(XML_PSU_TAG)
    Vmax_V=float(limits.find(XML_PSU_TAG_VMAX).text)
    Imax_A=float(limits.find(XML_PSU_TAG_IMAX).text)
    NoOfStep = int(limits.find(XML_PSU_TAG_STEPS).text)
    Pass_Fail_limits_mA =float(limits.find(XML_PSU_TAG_PASS_FAIL).text)
    Open_Circuit_limits_mA =float(limits.find(XML_PSU_TAG_OPEN_CIR).text)

    #get PSU config
    psuCfg = root.find(XML_PSU_CFG_TAG)
    psuname= psuCfg.find(XML_PSU_CFG_TAG_NAME).text
    psugwip= psuCfg.find(XML_PSU_CFG_TAG_IP).text
    psugpib= psuCfg.find(XML_PSU_CFG_TAG_GPIB).text
    psuDelay_mS = int(psuCfg.find(XML_PSU_CFG_TAG_DELAY).text)

    psu_bench=PsuBenchControl(psu_name=psuname, psu_gwip=psugwip, psu_gpib=psugpib)
    #print psu_bench
    logoutput = str(psu_bench)
    psu_bench.on()
    #ramping up the voltage and check the currnt reading
    Vstep = Vmax_V / NoOfStep
    for i in range(0, NoOfStep):
        StepCnt = i+1
        Vout = StepCnt*Vstep
        psu_bench.set('P6V', Vout, Imax_A)
        # This may take up to 0.5 sec!!!
        t0_msec=int(round(time.time() * 1000))
        reading=psu_bench.read('P6V')
        if abs(reading[0][1] - Imax_A*1000) < CurrentDelta_mA:
            break #current exceed Max Limit
        logoutput += ("Vmax=%sV, Imax=%sA :: Readings Voltage=%s V, Current=%s mA\n" % (Vout, Imax_A, reading[0][0], reading[0][1]))
        print('.'),
        t1_msec=int(round(time.time() * 1000))
        t_delta = t1_msec - t0_msec
        logoutput += "PSU delay %s mS\n" % t_delta
        if t_delta < psuDelay_mS:
            delay_S = float(psuDelay_mS - t_delta)/1000
            time.sleep(delay_S)
            logoutput += ("Extra PSU delay %s mS \n" % (psuDelay_mS - t_delta))

    print('\n')
    logoutput +="\n"
    CurrentReading_mA = reading[0][1]
    if not(StepCnt >= NoOfStep and CurrentReading_mA <= Pass_Fail_limits_mA and CurrentReading_mA >= Open_Circuit_limits_mA):
        if StepCnt < NoOfStep:
            retVal = (0,"FAIL - Reason: Excessive current")
        else:
            if CurrentReading_mA <= Pass_Fail_limits_mA and CurrentReading_mA >= Open_Circuit_limits_mA:
                retVal = (0,"FAIL - Reason: Exceed Pass/Fail current limit")
            else:
                retVal = (0,"FAIL - Reason: Open circuit")
    else:
        retVal = (1, "PASS")
    psu_bench.off()
    psu_bench.close()
    #add the log strings
    rtV=list(retVal)
    rtV.append(logoutput)
    retVal = tuple(rtV)
    return retVal

#=====================================================================
if __name__ == '__main__':
     results = smoketest()
     print results[2], results[1]
     raw_input("Press Enter to exit")



