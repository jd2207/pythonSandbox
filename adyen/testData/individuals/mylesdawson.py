'''
  Name – Myles Dawson
  email – myles.dawson@adyen.com
  DOB - 08/11/2016
  Nationality - British
  Phone number - 00447957804192
  Adress – Viners, Mire Lane, Waltham St Lawrence, Berkshire, RG10 0NJ
  Number of national ID / NHS number – NZ 262276C
  IBAN: GB84HLFX11066510509668 
'''

TEST_EMAIL = "myles.dawson@adyen.com"

TEST_INDIVIDUAL_DETAILS = {
    "name": {
      "firstName":"Myles",
      "gender":"MALE",
      "lastName":"Dawson"
      }, 
    "personalData" : {
      "dateOfBirth":"??????",
      "idNumber":"NZ 262276C",
      "nationality":"GB"
      }
  }
 

TEST_ADDRESS = {
  "city":"Lawrence",
  "country":"GB",
  "postalCode":"RG10 0NJ",
  "houseNumberOrName" : "Viners",
  "stateOrProvince":"",
  "street":"Mire Lane"
  }

TEST_PHONE = {
  "phoneCountryCode":"GB",
  "phoneNumber":"07957804192",
  "phoneType":"Mobile"
  }

TEST_BANK_ACCOUNT_DETAILS = [
            {
                "BankAccountDetail":{
                   "iban" : "GB84HLFX11066510509668",
                   "countryCode" : "GB",
                   "currencyCode" : "GBP",
                   "ownerCity":"Lawrence",
                   "ownerHouseNumberOrName":"Viners",
                   "ownerName":"Myles Dawson",
                   "ownerPostalCode":"RG10 0NJ"
                }
            }]

