'''
Name - Chris Pinnegar
email - chris.pinnegar@adyen.com
DOB - 07/02/1978
Nationality - British
Phone number - 07973462067
Adress - Marwell, Basingstoke Road, Three Mile Cross, Berkshire, RG7 1AX
Number of national ID / NHS number - JP582757B
Bank account number / IBAN - 71510703
Bank account holder name (if different from name) - GB54MIDL40190371510703
'''

TEST_EMAIL = "chris.pinnegar@adyen.com"

TEST_INDIVIDUAL_DETAILS = {
    "name": {
      "firstName":"Chris",
      "gender":"MALE",
      "lastName":"Pinnegar"
      }, 
    "personalData" : {
      "dateOfBirth":"1978-02-07",
      "idNumber":"JP582757B",
      "nationality":"GB"
      }
  }
 

TEST_ADDRESS = {
  "city":"Three Mile Cross",
  "country":"GB",
  "postalCode":"RG7 1AX",
  "houseNumberOrName" : "Marwell",
  "stateOrProvince":"",
  "street":"Basingstoke Road"
  }

TEST_PHONE = {
  "phoneCountryCode":"GB",
  "phoneNumber":"07973462067",
  "phoneType":"Mobile"
  }

TEST_BANK_ACCOUNT_DETAILS = [
            {
                "BankAccountDetail":{
                   "iban" : "GB54MIDL40190371510703",
                   "countryCode" : "GB",
                   "currencyCode" : "GBP",
                   "ownerCity":"Three Mile Cross",
                   "ownerHouseNumberOrName":"Marwell",
                   "ownerName":"Chris Pinnegar",
                   "ownerPostalCode":"RG7 1AX"
                }
            }]
