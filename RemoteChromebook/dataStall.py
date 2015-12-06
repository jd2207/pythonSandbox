'''
Script which will check continuously (for a given time period) for data stall by performing periodic pings  

Usage:  dataStall(rcb,timer) 
where   rcb is a remoteChromebook instance
        timer is duration of the test
'''

import time, logging

SLEEP_TIME = 10    # seconds between ping attempts 

def dataStall(cb,timer=3600):     # test for 1 hour by default

    dataStall = False
    elapsedTime = 0.0
    timeout = False
    
    while not dataStall and not timeout:
    
# simple ping, once per minute until single ping fail or timeout  
        while cb.ping():
            time.sleep(SLEEP_TIME) 
            elapsedTime += SLEEP_TIME 
            logging.debug('No data stall after '+ str(elapsedTime) + ' seconds')
            if elapsedTime >= timer:
                timeout = True
                break
                
# Attempt recovery if one ping fails, 5 times over a short period
        else:
            logging.warning('Ping failure, possible stall ... ')
            i = 5
            while i > 0:
                logging.warning( str(i) + ' attempts left to recover')
                if cb.ping():
                    logging.warning('Recovery')
                    break
                else:
                    time.sleep(5.0) 
                    i -= 1
            else:                   # data stall declared if None of the 5 attempts are successful
                dataStall = True

    logging.error('Stall declared!') if dataStall else logging.info('No stall after a total of '+str(timer) +' seconds')
    return dataStall


    