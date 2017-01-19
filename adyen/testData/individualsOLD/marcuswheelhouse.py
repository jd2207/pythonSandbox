'''
Name - Marcus Wheelhouse
email - marcus.wheelhouse@adyen.com
DOB - 09/10/1992
Nationality - British
Phone number - 00447794963194
Adress - Erin, Kinburn Drive, Egham Hill, Egham, Surrey, TW20 0BD
Number of national ID / NHS number - JW 74 97 32 A
Bank account number / IBAN - GB52NWBK60073347702761
'''

TEST_EMAIL = "marcus.wheelhouse@adyen.com"

TEST_INDIVIDUAL_DETAILS = {
    "name": {
      "firstName":"Marcus",
      "gender":"MALE",
      "lastName":"Wheelhouse"
      }, 
    "personalData" : {
      "dateOfBirth":"1992-10-09",
      "idNumber":"JW 74 97 32 A",
      "nationality":"GB"
      }
  }
 

TEST_ADDRESS = {
  "city":"Egham",
  "country":"GB",
  "postalCode":"TW20 0BD",
  "houseNumberOrName" : "Erin",
  "stateOrProvince":"",
  "street":"Kinburn Drive"
  }

TEST_PHONE = {
  "phoneCountryCode":"GB",
  "phoneNumber":"+4407794963194",
  "phoneType":"Mobile"
  }

TEST_BANK_ACCOUNT_DETAILS = [
            {
                "BankAccountDetail":{
                   "iban" : "GB52NWBK60073347702761",
                   "countryCode" : "GB",
                   "currencyCode" : "GBP",
                   "ownerCity":"Egham",
                   "ownerHouseNumberOrName":"Erin",
                   "ownerName":"Marcus Wheelhouse",
                   "ownerPostalCode":"TW20 0BD"
                }
            }]
