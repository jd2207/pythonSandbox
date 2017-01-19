import testData.misc
import sys, logging

def getDetailsFromHandle(handle):
  
  if handle == None:
    return MINIMAL_PERSON
  elif handle == 'TestPerson':
    return TEST_PERSON
  elif handle == 'AnnPerry':
    return ANN_PERRY
  else:
    logging.error('Unknown handle %s' % handle)
    sys.exit()


MINIMAL_PERSON = {
  "email": testData.misc.MP_TEST_EMAIL,
  "individualDetails": {
    "name" : testData.misc.MP_TEST_NAME
    }
  } 


TEST_PERSON = {
  'address' : testData.misc.MP_TEST_ADDRESS,
  'bankAccountDetails' : [{ 'BankAccountDetail' : testData.misc.MP_TEST_BANK_ACCOUNT_DETAIL_NO_IBAN }],
  'email' : testData.misc.MP_TEST_EMAIL,
  'individualDetails' : { "personalData" : testData.misc.MP_TEST_PERSONAL_DATA,
                          "name" : testData.misc.MP_TEST_NAME
                        },
  'phoneNumber' : testData.misc.MP_TEST_PHONE_NUMBER
  }


ANN_PERRY = {
  "address" : {
    "city":"March",
    "country":"GB",
    "postalCode":"PE15 9PN",
    "houseNumberOrName" : "11",
    "stateOrProvince":"",
    "street":"Monument View"
  },
  "bankAccountDetails" : [{            
    "BankAccountDetail": {
      "accountNumber":"91104381",
      "bankCode" : "MIDL",
      "branchCode":"403922",
      "countryCode" : "GB",
      "currencyCode" : "GBP",
      "ownerCity":"MARCH",
      "ownerDateOfBirth":"1974-02-16",
      "ownerHouseNumberOrName":"11",
      "ownerName":"Ann Perry",
      "ownerPostalCode":"PE15 9PN"
    }
  }],
  "email" : "ap1602@yahoo.co.uk",
  "individualDetails" : {
    "name": {
      "firstName":"Ann",
      "gender":"FEMALE",
      "lastName":"Perry"
    }, 
    "personalData" : {
    "dateOfBirth":"1974-02-16",
    "idNumber":"JA029676A",
    "nationality":"GB"
    }
  },
  "phoneNumber" : {
    "phoneCountryCode":"GB",
    "phoneNumber":"+447879593430",
    "phoneType":"Mobile"
  }
}





