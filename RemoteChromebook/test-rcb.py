import rcb

cb = rcb.rcb('192.168.1.210','root')       # password-less
cb.fw_update('/xxx/yyy')


'''
cb2 = rcb.rcb('10.20.221.13','root')  		 # will ask for a password
print ('cb2 done')

print 'try a wrong password'
cb3 = rcb.rcb('10.20.221.13','chrometest')   # will ask for a password, get it wrong
print 'should not get here'

print cb.sendCommand('ls -l')
print 'xxx'
print cb.sendCommand('ls -l',1)

print cb.versions()
#cb.reboot() 

print 'Enumeration is:', cb.modemEnumeration()

print 'Last time connected is:', cb.lastTimeModemConnected()
print 'System time now is:',cb.systime()
print 'Difference is',cb.systime() - cb.lastTimeModemConnected()

fn = '/dev/mdm0_at'
print fn + ('exists' if  cb.fileExists(fn) else 'does not exist')

fn = '/dev/mdm0_atxx'
print fn + ('exists' if  cb.fileExists(fn) else 'does not exist')
'''