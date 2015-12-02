'''
Created on 4 Aug 2013

@author: fsaracino
'''

def cfg_multilogging(log_level, log_file):
    import sys 
    import logging
    
    # Define the message format 
    frmt_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Check if the input parameters log_level is valid
    numeric_level=getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid logging level: %s' % (log_level))
        
    # Set up DEBUG logging to file
    logging.basicConfig(level=logging.DEBUG, 
                        format=frmt_str,
                        filename=log_file,
                        filemode='w')
    
    # Define console handler for  messages 
    hc = logging.StreamHandler(sys.stdout)
    hc.setLevel(numeric_level)

    # Set a format for console messages
    hc_frmt=logging.Formatter(frmt_str)
    hc.setFormatter(hc_frmt)
    
    # Add handler to the root logger    
    logging.getLogger('').addHandler(hc)
    
    return logging.getLogger('')
    

if __name__ == "__main__":
    import os
    import logging
    
    def main():
        logger=logging.getLogger('main')

        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warning message')
        logger.error('error message')
        logger.critical('critical message')
            
    def test():
        logger=logging.getLogger('test')
        logger.info("function ok")
        
    
    (cmdpath, cmdname)=os.path.split(os.path.abspath(__file__))
    logger=cfg_multilogging('DEBUG', os.path.splitext(cmdname)[0]+'.LOG')

    logger.info("START")
    main()
    test()
    logger.info("END")
    
    
    
