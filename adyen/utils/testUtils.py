import datetime, time, json, copy

# TEST credentials ======================================================================

# Credentials for TEST marketpay account JohnDick 
TEST_CRED_MP_JOHNDICK = ('ws_635247@MarketPlace.JohnDick', 'N)G^xjE#&<6Jc6r!~/mQMHM8F')

# Credentials for TEST marketpay account GoFundMe 
TEST_CRED_MP_GOFUNDME = ('ws_087431@MarketPlace.GoFundMe', 'SRKPeM9Pt#[mNkLxvRCIm7wKx')

# Credentials for making a payment on TEST 
TEST_CRED_PAYMENT = ('ws_586199@Company.AdyenTechSupport', 'Q*-h6a?8Ut!qU<Q(F2y1br{MM')

  
# LIVE credentials ======================================================================

# Credentials for live account TestMarketPlace
TEST_CRED_LIVE = ('ws_032172@MarketPlace.TestMarketPlace', 'C>)^6p=DyJe[J&X9sqJj=L]4N')

# Credentials for making a payment on LIVE 
TEST_CRED_LIVE_PAYMENT = ('ws_074722@Company.TestMarketPlaceCompany', 'd9Bc{g2L>L/#+u8Y<^5SHvD3Q')

# Credentials for live GoFundMe 
TEST_CRED_LIVE_GFM = ('ws_100468@MarketPlace.GoFundMe', '%H9s62gJsZYvEkU6D(+(?\cW/') 

# Amounts 
TEST_1_EUR_AMOUNT = {"value": 100, "currency" : "EUR"}


TEST_HOLDER = "John Smith"
 
TEST_CHARGEBACK_HOLDER = "CHARGEBACK" 


# Test cards ============================================================================

TEST_CARD_VISA =  { "number": "4111111111111111",                 
                    "expiryMonth": "8",                           
                    "expiryYear": "2018",                         
                    "cvc": "737",                                 
                    "holderName": TEST_HOLDER                    
                  }   

JOHN_VISA = {
    "number": "4003449102489836",                 
    "expiryMonth": "4",                           
    "expiryYear": "2020",                         
    "cvc": "243",                                 
    "holderName": "John Dick"                    
  }


MP_TEST_PERSON = {
  "email":"test@adyen.com",
  "individualDetails": {
    "name": {
      "firstName":"FirstName",
      "gender":"MALE",
      "lastName":"SecondName"
      }
   } 
}






MP_TEST_ADDRESS = {
  "city":"Amsterdam",
  "country":"US",
  "postalCode":"12345",
  "stateOrProvince":"NH",
  "street":"Teststreet 1"
  }


MP_TEST_ADDRESS_LIMITEDPAYOUTCITY = {
  "city":"LIMITEDPAYOUTCITY",
  "country":"US",
  "postalCode":"12345",
  "stateOrProvince":"NH",
  "street":"Teststreet 1"
  }


MP_FRAUD_ADDRESS = {
  "city":"FRAUDCITY",
  "country":"US",
  "postalCode":"12345",
  "stateOrProvince":"NH",
  "street":"Teststreet 1"
  }


MP_TEST_PHONE_NUMBER = {
  "phoneCountryCode":"NL",
  "phoneNumber":"0612345678",
  "phoneType":"Mobile"
  }


MP_TEST_BANK_ACCOUNT_DETAIL_NO_IBAN = {
   "accountNumber":"12345678",
   "bankAccountName":"baName",
   "bankBicSwift":"BicSUSft",
   "bankCity":"city",
   "bankName":"bankName",
   "branchCode":"122105155",
   "countryCode":"US",
   "currencyCode":"EUR",
   "ownerCity":"ownerCity",
   "ownerCountryCode":"BE",
   "ownerDateOfBirth":"1980-01-01",
   "ownerHouseNumberOrName":"houseNumberOrName",
   "ownerName":"ownerName",
   "ownerNationality":"AD",
   "ownerPostalCode":"ownerPostalCode",
   "ownerState":"ownerState",
   "ownerStreet":"ownerStreet",
   "primaryAccount":"true",
   "taxId":"bankTaxId"
}


MP_TEST_DOC_PASSPORT = {
  "content": "dGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxbdGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxb" +  
                     "dGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxbdGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxb" +
                     "dGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxbdGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxb" + 
                     "dGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxbdGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxb" + 
                     "dGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxbdGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxb" + 
                     "dGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxbdGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxb" + 
                     "dGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxbdGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxb" + 
                     "dGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxbdGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxb" + 
                     "dGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxbdGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxb" + 
                     "dGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxbdGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxb" + 
                     "dGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxbdGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxb" + 
                     "dGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxbdGVzdCBkb2N1bWVudCBjb250ZW50xbxbxbxbxbxbxbxbxbxbxbxbxbxbxb",
  "detail": {
    "description": "PENDINGREVIEW",
    "documentType": "PASSPORT",
    "filename" : "fileName1.jpg"
  }
}



DEFAULT_MERCHANT_CATEGORY_CODE = '7999'

MP_TEST_ACCOUNT_HOLDER_DETAILS = MP_TEST_PERSON
MP_TEST_ACCOUNT_HOLDER_DETAILS["bankAccountDetails"] = []
MP_TEST_ACCOUNT_HOLDER_DETAILS["merchantCategoryCode"] = DEFAULT_MERCHANT_CATEGORY_CODE  

MP_TEST_DEFAULT_LIMITEDPROCESSING = { 
                    "allowPayout": "false", 
                    "allowProcessing": "true", 
                    "stateLimit": {
                      "amount": 1000000, 
                      "currency": "EUR"
                    }, 
                    "stateType": "LimitedProcessing"
  }


MP_TEST_DEFAULT_LIMITEDPAYOUT = {
                    "allowPayout": "true", 
                    "allowProcessing": "false", 
                    "stateType": "LimitedPayout"
  }

MP_TEST_DEFAULT_LIMITLESSPROCESSING = {
                "allowPayout": "false", 
                "allowProcessing": "true", 
                "stateType": "LimitlessProcessing"
                }

MP_TEST_DEFAULT_LIMITLESSPAYOUT = {
                "allowPayout": "true", 
                "allowProcessing": "false", 
                "stateType": "LimitlessPayout"
                }

MP_TEST_FIRST_STATE = { "states": [  MP_TEST_DEFAULT_LIMITEDPROCESSING  ], 
                        "status": "Active"
                      }


MP_TEST_DEFAULT_LIMITEDPROCESSING_DERIVED = copy.copy(MP_TEST_DEFAULT_LIMITEDPROCESSING)
MP_TEST_DEFAULT_LIMITEDPROCESSING_DERIVED["derived"] = "true"

MP_TEST_DEFAULT_LIMITEDPAYOUT_DERIVED = copy.copy(MP_TEST_DEFAULT_LIMITEDPAYOUT)
MP_TEST_DEFAULT_LIMITEDPAYOUT_DERIVED["derived"] = "true"

MP_TEST_DEFAULT_LIMITLESSPROCESSING_DERIVED = copy.copy(MP_TEST_DEFAULT_LIMITLESSPROCESSING)
MP_TEST_DEFAULT_LIMITLESSPROCESSING_DERIVED["derived"] = "true"

MP_TEST_DEFAULT_LIMITLESSPAYOUT_DERIVED = copy.copy(MP_TEST_DEFAULT_LIMITLESSPAYOUT)
MP_TEST_DEFAULT_LIMITLESSPAYOUT_DERIVED["derived"] = "true"

MP_TEST_DEFAULT_STATE_CONFIG = [ { "AccountStateConfiguration" : MP_TEST_DEFAULT_LIMITLESSPROCESSING_DERIVED  }, 
                                 { "AccountStateConfiguration" : MP_TEST_DEFAULT_LIMITLESSPAYOUT_DERIVED }, 
                                 { "AccountStateConfiguration" : MP_TEST_DEFAULT_LIMITEDPAYOUT_DERIVED }, 
                                 { "AccountStateConfiguration" : MP_TEST_DEFAULT_LIMITEDPROCESSING_DERIVED }
                               ]


class CardPayment(object):
  
  def __init__(self, merchantAccount, amount, creditCard, merchantReference=None ):

    self.paymentReq = \
      { "card" : creditCard,
        "amount" : amount,  
        "reference": merchantReference if merchantReference!=None else timestampMerchantRef(),                 
        "merchantAccount": merchantAccount
      } 


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

