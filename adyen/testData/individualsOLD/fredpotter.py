'''
Name Fred Potter
email fred.potter@adyen.com
DOB 26/05/1992
Nationality British
Phone number +447906851669
Adress 21 hillyard street, sw9 0ng
Number of national ID / NHS number 522675290
Bank account number / IBAN GB55NWBK60023667650856
Bank account holder name (if different from name)
'''

TEST_EMAIL = "fred.potter@adyen.com"

TEST_INDIVIDUAL_DETAILS = {
    "name": {
      "firstName":"Fred",
      "gender":"MALE",
      "lastName":"Potter"
      }, 
    "personalData" : {
      "dateOfBirth":"1992-05-26",
      "idNumber":"522675290",
      "nationality":"GB"
      }
  }
 

TEST_ADDRESS = {
  "city":"London",
  "country":"GB",
  "postalCode":"SW9 0NG",
  "houseNumberOrName" : "21",
  "stateOrProvince":"",
  "street":"Hillyard Street"
  }

TEST_PHONE = {
  "phoneCountryCode":"GB",
  "phoneNumber":"+447906851669",
  "phoneType":"Mobile"
  }

TEST_BANK_ACCOUNT_DETAILS = [
            {
                "BankAccountDetail":{
                   "iban" : "GB55NWBK60023667650856",
                   "countryCode" : "GB",
                   "currencyCode" : "GBP",
                   "ownerName":"Fred Potter",
                   "ownerPostalCode":"SW9 0NG"
                }
            }]
