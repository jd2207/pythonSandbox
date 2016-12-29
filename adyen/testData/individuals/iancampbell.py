'''
Ian Campbell  
ian.campbell@adyen.com
13/9/1977
British
07818037750
21 Merlin Way, Bicester, OX26 6YG
Acc number - 00348181
Sort code – 090131

'''

TEST_EMAIL = "ian.campbell@adyen.com"

TEST_INDIVIDUAL_DETAILS = {
    "name": {
      "firstName":"Ian",
      "gender":"MALE",
      "lastName":"Campbell"
      }, 
    "personalData" : {
      "dateOfBirth":"1977-09-13",
      "idNumber":"??????",
      "nationality":"GB"
      }
  }
 

TEST_ADDRESS = {
  "city":"Bicester",
  "country":"GB",
  "postalCode":"OX26 6YG",
  "houseNumberOrName" : "21",
  "stateOrProvince":"",
  "street":"Merlin Way"
  }

TEST_PHONE = {
  "phoneCountryCode":"GB",
  "phoneNumber":"07818037750",
  "phoneType":"Mobile"
  }

TEST_BANK_ACCOUNT_DETAILS = [
            {
                "BankAccountDetail":{
                   "iban" : "",
                   "countryCode" : "GB",
                   "currencyCode" : "GBP",
                   "ownerCity":"LONDON",
                   "ownerHouseNumberOrName":"21",
                   "ownerName":"Fred Potter",
                   "ownerPostalCode":"SW9 0NG"
                }
            }]
