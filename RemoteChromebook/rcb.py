"""
Module to represent a remotely ssh-able chromebook
"""

import getpass, re, pxssh
from dateutil.parser import parse
from pexpect import EOF
import subprocess, logging

TIMEOUT = 60
noChromeDevTools = 'Check if chromedevtools are correctly installed'


class sshTimeout(Exception):
	pass
	
class rcb(object):

	def __init__(self,host,user):			# create the SSH connection or die
		self.ssh = None
		self.timeout = TIMEOUT 				# default ssh timeout 
		try:
			s=pxssh.pxssh()
			s.login (host, user)			# try password-less first
				
		except pxssh.ExceptionPxssh as e1:
			if str(e1) == 'password refused':
				try: 
					password = getpass.getpass('password: ')
					s=pxssh.pxssh()
					s.login (host,user,password)
				except pxssh.ExceptionPxssh as e2:
					self.ssh_fail(e2,user,host)
				else:
					self.ssh_ok(s,user,host)
			else:
				self.ssh_fail(e1,user,host)
		except EOF as e3:
				self.ssh_fail(e3,user,host)
		else:
			self.ssh_ok(s,user,host)
		

	def ssh_ok(self,s,user,host):
		self.ssh = s
		self.user = user
		self.host = host
		logging.info('Successful connection to '+str(self.user+'@'+self.host)) 

	def ssh_fail(self,e,user,host):
		logging.error('SSH session to ' + str(user+'@'+host) + ' failed on login.')

	def sendCommand(self,cmd,flag=0):

		self.ssh.sendline(cmd)
		if self.ssh.prompt(self.timeout):		# wait for the prompt
			output = self.ssh.before
			return output.replace(cmd,'') if flag else output		# return the output (minus original command if flag is set)
		else:
			raise sshTimeout ('Timeout during ssh command: '+str(cmd))
		
			
	def version(self):
		output = self.sendCommand('cat /etc/lsb-release')
		return re.search('CHROMEOS_RELEASE_DESCRIPTION=(.*)',output).group(1)
		
	def reboot(self):
		self.sendCommand('reboot')
				
	def modemEnumeration(self):			# returns 0 = not enumerated; 1 = normal MBIM profile; 2 = loader mode; 3 = 5AN profile
		patterns = {'1983:1003':1, '1983:1000':2, '1983:1007':3 }
		lsusb = self.sendCommand('lsusb')
					
		for p in patterns:
			if re.search(p,lsusb):
				return patterns.get(p)
		return 0
	
	def lastTimeModemConnected(self):
		output = self.sendCommand("cat /var/log/net.log | grep 'state changed (connecting -> connected)' | tail -1")
		return parse(re.search('(.*) localhost',output).group(1)) if output else None

	def systime(self):
		dt = self.sendCommand('date --iso-8601=seconds',1)
		return parse(dt)
	
	def fileExists(self,fn):
		cmd = 'if [ -e '+fn+' ]; then echo 1; fi'
		return 1 if (self.sendCommand(cmd,1)) else 0
			
	def sendATCommand(self,atcmd):
		modem = '/dev/mdm0_at'
		if not (self.fileExists(modem)):
			if not self.fileExists('/usr/local/bin/nv-soc-local.sh'):
				quit('nv-soc-local.sh not on path '+noChromeDevTools)
			else:
				self.sendCommand('echo 1 | nv-soc-local.sh')
				self.sendCommand('nv-start-logging.sh')			   # re-start logging
		return  self.sendCommand('atcmd-itf '+modem+' '+atcmd,1)

	def forceRATMode(self,mode):
		resp = self.sendATCommand('AT%INWMODE=0,'+mode+',1')
		return 1 if re.search('OK',resp) else 0

	def networkOper(self):
		resp = self.sendATCommand('AT+COPS?')
		return re.search('\+COPS:.*"(.*)"',resp).group(1)
	
	def copyTo(self,local,remote):
		subprocess.call(['scp','-r',local,self.user+'@'+self.host+':'+remote])
		
	def fwUpdate(self, fwDir):
		if self.fileExists('/usr/local/bin/nv-fw-update.sh'):
			self.timeout = 60							# fw updates needs bigger timeout
			print self.sendCommand('echo 1 | nv-fw-update.sh '+fwDir)
			self.timeout = TIMEOUT						# return to default
		else:
			quit('Cannot find nv-fw-update.sh '+noChromeDevTools)
		
	def modemVersion(self):
		self.sendATCommand('AT+GMR')
	
	def ping(self,host='8.8.8.8'):
		try: 
			logging.debug('attempting to ping '+host)
			logging.debug(self.sendCommand('ip route add '+host+' dev wwan0'))
			output = self.sendCommand('ping -c 1 -W 5 ' + host,1)			# 5 second ping timeout
			return True if re.search('1 received',output) else False
		except sshTimeout:
			logging.warning('Ping failure due to SSH timeout')
			return False
			
			
			
# --------------------------------------------------------------
# Subclasses for specific chromebooks with fixed IP addresses		
# --------------------------------------------------------------
		
class asif(rcb):
	def __init__(self):
		super(asif,self).__init__('172.17.164.120','root')		
