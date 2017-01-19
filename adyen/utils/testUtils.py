import datetime, time, json, sys

import testData.merchants.marketPlaceMerchants
from testData.merchants.marketPlaceMerchants import JOHNDICKMARKETPLACE, TESTMARKETPLACE, GOFUNDME, GOFUNDME_TEST, BAD_AUTH_MERCHANT, JOHNDICKMARKETPLACE_BADPASSWORDS

'''
def getCredentials(merchantAccount, platform='psp'):

# Read the credentials from testData 
  if (merchantAccount == 'JohnDickMarketPlace'):
    merchant = testData.merchants.marketPlaceMerchants.Merchant(JOHNDICKMARKETPLACE)
  elif (merchantAccount == 'TestMarketPlaceMerchant'):
    merchant = testData.merchants.marketPlaceMerchants.Merchant(TESTMARKETPLACE)
  elif (merchantAccount == 'GoFundMeIE'):
    merchant = testData.merchants.marketPlaceMerchants.Merchant(GOFUNDME)
  elif (merchantAccount == 'GoFundMeCOM'):
    merchant = testData.merchants.marketPlaceMerchants.Merchant(GOFUNDME_TEST)
  elif (merchantAccount == 'BadAuthMerchant'):
    merchant = testData.merchants.marketPlaceMerchants.Merchant(BAD_AUTH_MERCHANT)
  elif (merchantAccount == 'BadPasswordMerchant'):
    merchant = testData.merchants.marketPlaceMerchants.Merchant(JOHNDICKMARKETPLACE_BADPASSWORDS)
  else:
    sys.exit('ERROR: No credential data setup for merchant %s' % merchantAccount)

  if platform == 'psp':
    return merchant.psp_credentials
  elif platform == 'mp':
    return merchant.mp_credentials
  else:
    sys.exit('ERROR: No platform specified for credentials for merchant %s' % merchantAccount)
'''


def timestampMerchantRef():
  return "Test @ " + str(datetime.datetime.now())


def uniquenameFromTimestamp():
  return int( time.mktime(datetime.datetime.now().timetuple()) ).__str__()

  
def jsonFromFile(jsonFileName):
  with open(jsonFileName) as jsonFile:    
    data = json.load(jsonFile)
  return data


def jsonDump( r ):
  return json.dumps( r, sort_keys=True, indent=4)


def jsonPrint( r ):
  print jsonDump( r )




