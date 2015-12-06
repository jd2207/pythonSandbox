'''
Script which will update the modem on a remote chromebook

Assumes that the remote chromebook is ssh-able 

Usage:  remoteUpdate user, host, local_fw_update_dir

'''

import rcb, sys, time

# Arguments    
host = sys.argv[1]

user = sys.argv[2] if len(sys.argv) > 2 else 'root'
local_fw_update_dir = sys.argv[3] if len(sys.argv) > 3 else '.' 


# Establish ssh connection to remote chromebook (or quit)
rcb = rcb.rcb(host,user)
quit() if not rcb.ssh else None

# Copy the firmware update to the remote chromebook
remoteDir= '/var/log/icera/fw_update/binaries_nvidia-e1729-mbim'

rcb.sendCommand('mkdir '+ remoteDir) if not rcb.fileExists(remoteDir) else None
print 'Copying new modem firmware from local:',local_fw_update_dir,'to remote Chromebook:',remoteDir

rcb.copyTo(local_fw_update_dir, remoteDir)


# Do the upgrade
rcb.fwUpdate(remoteDir)
print 'Waiting 20 seconds for modem to re-enumerate...'
time.sleep(20)
print 'Modem version now is ...',rcb.modemVersion()

        