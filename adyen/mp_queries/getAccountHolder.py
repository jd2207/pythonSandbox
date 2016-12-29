#! /usr/bin/python

# --------------------------------------------------------------------------------------------------------------
#
#  Utility to query AccountHolder state via command line
#
#  See getAccountHolder.py --help for command line options
#
# --------------------------------------------------------------------------------------------------------------


import accountHolder.accountHolder, testData.merchants.MarketPlaceMerchants
import argparse, sys
import utils.testUtils

def parseArgs( ):
  desc = "Simple utility for querying a marketpay accountHolder"
  parser = argparse.ArgumentParser(description=desc)
 
  #Mandatory arguments
  parser.add_argument( 'merchantAccount', help='merchant account')
  parser.add_argument( 'accountHolder', help='marketpay accountHolder')
 
  #Optional/keyword arguments
  parser.add_argument( '--live', action='store_true', help='flag to specify the LIVE system, otherwise TEST system is assumed')
  parser.add_argument( '--debug', action='store_true', help='debug flag, default = OFF')
  
  args = parser.parse_args()    
  return args


if __name__ == '__main__':

  args = parseArgs()  # Parse command line arguments
  
  # Read the credentials from testData 
  if (args.merchantAccount == 'JohnDickMarketPlace'):
    credentials = testData.merchants.MarketPlaceMerchants.JohnDickMarketPlace.TEST_MP_CRED
  elif (args.merchantAccount == 'TestMarketPlaceMerchant'):
    credentials = testData.merchants.MarketPlaceMerchants.TestMarketPlace.TEST_MP_CRED
  elif (args.merchantAccount == 'GoFundMeIE'):
    credentials = testData.merchants.MarketPlaceMerchants.GoFundMeIE.TEST_MP_CRED
  else:
    sys.exit('ERROR: No credential data setup for merchant %s' % args.merchantAccount)

  if args.debug:
    print 'Merchant account: %s' % args.merchantAccount
    print 'Account Holder: %s' % args.accountHolder
    print 'Live flag: %s' % args.live
    print 'Debug is ON' 
  else:
    print 'Debug is OFF'

'''
# TEST JohnDick marketpay account 
live=False
credentials = testUtils.TEST_CRED_MP_JOHNDICK
ahName= "1481325809"
'''

'''
# LIVE Go FundMe marketpay account 
credentials = utils.testUtils.TEST_CRED_LIVE_GFM
live = True
#ahName = 'UID-15894774'    #  ---> just set up ' "awaiting data" - Grandad is 70
#ahName = 'UID-15894710'   #  --- Jason test
ahName = 'UID-15894276'  #   FIRST TRANSACTION!!! email, first second name only - Borneo trip
#ahName = 'UID-15894614'   # --- Jason test
#ahName = 'UID-15899606'  # just set up - "awaiting data"
#ahName = 'UID-15892398'  # - identity verification is PASSED    *    created before Thursday's patch
#ahName = 'UID-15913146'  # awaiting data    *
#ahName = 'UID-15914392' # awaiting data    *
#ahName = 'UID-15911480'  # awaiting data
#ahName = 'UID-15913146'  # awaiting data
#ahName = 'UID-15913532' # awaiting data
#ahName = 'UID-15914514' # awaiting data
#ahName = 'UID-15917852'
ahName = 'UID-15919182'   # Islamic guidance
'''

'''
# LIVE TestMarketPlace 
live=True
credentials = utils.testUtils.TEST_CRED_LIVE
#ahName = 'JohnDTestAH'
# ahName = 'JamieCollins'
#ahName = 'RobFreedman'
#ahName = 'BrianMapley'
#ahName = 'FredPotter'
#ahName = '1481761179'
#ahName = '1482261949'
#ahName='1481843694'
ahName='1482259383'
'''

# --------------------------------------------------------------------------------------------------------------
#  Read the accountHolder  
# --------------------------------------------------------------------------------------------------------------

ah = accountHolder.accountHolder.getAccountHolder(args.accountHolder, credentials, live=args.live, debug=args.debug)

#ah = accountHolder.accountHolder.getAccountHolder(ahName, credentials, live=live, debug=True)

ah.getBalance()
ah.getTransactionList()
