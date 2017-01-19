import sys


def getMerchantFromAlias(alias):
  
  if alias == 'JohnDickMarketPlace':
    return Merchant(JOHNDICKMARKETPLACE)
  elif alias == 'TestMarketPlaceMerchant':
    return Merchant(TESTMARKETPLACE)
  elif alias == 'GoFundMeIE':
    return Merchant(GOFUNDME)
  else:
    print 'ERROR: Merchant alias %s not recognized'
    sys.exit()



class Merchant(object):
  def __init__(self, merchantData):
    self.merchantName = merchantData['merchantName']
    self.companyName = merchantData['companyName']
    self.marketPlaceName = merchantData['marketPlaceName'] if 'marketPlaceName' in merchantData.keys() else None
    self.mp_credentials = fullCreds(merchantData['mp_cred'], 'mp', self.marketPlaceName) if 'mp_cred' in merchantData.keys() else None
    self.psp_credentials = fullCreds(merchantData['psp_cred']  , 'psp', self.companyName) if 'psp_cred' in merchantData.keys() else None
    self.mp_testVirtualAccount = merchantData['mp_test_virtual_account'] if 'mp_test_virtual_account' in merchantData.keys() else None


JOHNDICKMARKETPLACE = {
    'merchantName' : 'JohnDickMarketPlace',
    'companyName' : 'AdyenTechSupport', 
    'marketPlaceName' : 'JohnDick',
    'mp_cred' : ('ws_635247', 'N)G^xjE#&<6Jc6r!~/mQMHM8F'),
    'psp_cred' : ('ws_586199', 'Q*-h6a?8Ut!qU<Q(F2y1br{MM'),
    'mp_test_virtual_account' : '170523285'
    }

JOHNDICKMARKETPLACE_BADPASSWORDS = {
    'merchantName' : 'JohnDickMarketPlace',
    'companyName' : 'AdyenTechSupport', 
    'marketPlaceName' : 'JohnDick',
    'mp_cred' : ('ws_635247', 'password'),
    'psp_cred' : ('ws_586199', 'password')
    }


TESTMARKETPLACE = {
    'merchantName' : 'TestMarketPlaceMerchant',
    'companyName' : 'TestMarketPlaceCompany', 
    'marketPlaceName' : 'TestMarketPlace',
    'mp_cred' :  ('ws_032172', 'C>)^6p=DyJe[J&X9sqJj=L]4N'),
    'psp_cred' : ('ws_074722', 'd9Bc{g2L>L/#+u8Y<^5SHvD3Q')
    }

GOFUNDME = {
    'merchantName' : 'GoFundMeIE',
    'companyName' : 'GoFundMe', 
    'marketPlaceName' : 'GoFundMe',
    'mp_cred' :  ('ws_100468', '%H9s62gJsZYvEkU6D(+(?\cW/'),
  }

GOFUNDME_TEST = {
    'merchantName' : 'GoFundMeCOM',
    'companyName' : 'GoFundMe', 
    'marketPlaceName' : 'GoFundMe',
    'mp_cred' :  ('ws_087431', 'SRKPeM9Pt#[mNkLxvRCIm7wKx'),
  }

BAD_AUTH_MERCHANT = {
    'merchantName' : 'BadAuthMerchant',
    'companyName' : 'BadAuthMerchant', 
    'marketPlaceName' : 'BadAuthMerchant',
    'psp_cred' : ('user', 'password'),
    'mp_cred' :  ('user', 'password')
  }



def fullCreds( cred, platform, company_or_marketplace):
  if cred:
    if platform in ('psp','mp'):
      prefix = 'MarketPlace' if platform=='mp' else 'Company'
    else:
      print "ERROR: Bad value for parameter 'platform'"
      sys.exit()  
    return (cred[0] + '@' + prefix + '.' + company_or_marketplace, cred[1])
  else:
    return None



