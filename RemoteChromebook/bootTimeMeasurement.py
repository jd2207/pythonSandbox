'''
Script which will perform multiple reboots of a remote chromebook, and also measure the time to fully connect to the network

Assumes that the remote chromebook is ssh-able 

Usage:  bootTimeMeasurement user host iterations (default=1), ratString (default='EUG')

The test will fail if either:
  - the average time from boot to connected is greater than THRESHOLD1 seconds
  - any single measurement of boot to connected is greater than THRESHOLD2 seconds

'''

from rcb import rcb
from time import sleep

THRESHOLD1 = 30              # time limit in seconds for PASS of boot up till connect time (average of all test runs)
THRESHOLD2 = 60              # Max time limit in seconds maximum time allowed to achieve connection after a reboot - abort test 

# Arguments    
import sys
user = sys.argv[1]
host = sys.argv[2]
iterations = int(sys.argv[3]) if len(sys.argv) > 3 else 1
rats = sys.argv[4] if len(sys.argv) > 4 else 'EUG'

# Make the ssh connection (will quit if this fails)    
cb = rcb(host,user)

print 'Performing {0} reboot test(s) and measurement(s) on {1}@{2} for RATS = {3}'.format(iterations,user,host,rats)
print 'Network is:',cb.networkOper()

# Big loop for dual-mode, umts-only and lte-only
for rat in rats:
    print "Tests for rat =",rat
    if cb.forceRATMode(rat):
        print '{0:>5}{1:>20}{2:>20}{3:>15}'.format("Loop","Rebooted @","Re-Connected @","Diff (secs)")
        
        totalTime = 0;
        for i in range(1,iterations + 1):
            rebootTime = cb.systime()        # record time of the reboot
            cb.reboot()                                                    
            sleep(THRESHOLD2)                # wait for remote host to come back up, and for connection to be made 
            cb = rcb(host,user)
            if (cb.modemEnumeration() != 1):
                quit ('FAIL: The modem failed to enumerate in normal mode after a reboot')
            else:
                lastConnectTime = cb.lastTimeModemConnected();
                if (lastConnectTime < rebootTime):
                    quit ('FAIL: Modem unable to (re-)connect to the network')
                else:    
                    deltaT = (lastConnectTime - rebootTime).seconds 
                    totalTime += deltaT
                    print  '{0:>5}{1:            %H:%M:%S}{2:            %H:%M:%S}{3:15.2f}'.format(i,rebootTime,lastConnectTime,deltaT)
    else: 
        quit("Could not force modem to LTE only mode") 

    meanBootTime = totalTime / iterations
    print 'Time to connect average = {0:.2f} seconds: {1}'.format(meanBootTime,'PASS' if meanBootTime <= THRESHOLD1 else 'FAIL')
    