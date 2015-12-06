import logging, rcb, dataStall


def sshRecovery():
    print 'Try to establish a new connection'
    new_cb = rcb.asif()
    logging.info(cb.sendCommand('ip route add 204.2.137.173 dev wwan0'))
    return new_cb

logging.basicConfig(format='%(asctime)s  %(levelname)s: %(message)s',level=logging.INFO)

cb = rcb.asif()

# Start logging
logging.info(cb.sendCommand('nv-start-logging.sh -f'))

# Ensure FTP traffic goes through the modem  
logging.info(cb.sendCommand('ip route add 204.2.137.173 dev wwan0'))

# Loop until dataStall (or cannot recover from ssh timeout)
sshErrors = 0
while True:
    try:
        while not dataStall.dataStall(cb, 30):    # wait for a stall for period of 60 secs 
            logging.info('Performing a download...')
            cb.sendCommand('/usr/local/data/temp/ftp-download.sh',1)
            logging.info('Performing an upload...')
            cb.sendCommand('/usr/local/data/temp/ftp-upload.sh',1)
        else:
            logging.info ('Stopping logging')
            print cb.sendCommand('nv-stop-logging.sh')

    except rcb.sshTimeout:
        sshErrors += 1
        logging.warning('SSH timeout #'+str(sshErrors))
        cb = sshRecovery()




