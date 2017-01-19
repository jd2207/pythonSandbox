'''
Rob Freedman
rob.freedman@adyen.com (or rob.freedman@sky.com if you want personal email)
01/05/1986
UK
07496377269
First Floor Flat
46 Mayflower Road
London
SW9 9LA
JX484091D
GB40NAIA07011629259176
'''

TEST_EMAIL = "rob.freedman@sky.com"

TEST_INDIVIDUAL_DETAILS = {
    "name": {
      "firstName":"Rob",
      "gender":"MALE",
      "lastName":"Freedman"
      }, 
    "personalData" : {
      "dateOfBirth":"1986-05-01",
      "idNumber":"JX484091D",
      "nationality":"GB"
      }
  }
 

TEST_ADDRESS = {
  "city":"London",
  "country":"GB",
  "postalCode":"SW9 9LA",
  "houseNumberOrName":"46",
  "stateOrProvince":"",
  "street":"Mayflower Road"
  }

TEST_PHONE = {
  "phoneCountryCode":"GB",
  "phoneNumber":"07496377269",
  "phoneType":"Mobile"
  }

TEST_BANK_ACCOUNT_DETAILS = [
            {
                "BankAccountDetail":{
                   "iban" : "GB40NAIA07011629259176",
                   "countryCode" : "GB",
                   "currencyCode" : "GBP",
                   "ownerCity":"LONDON",
                   "ownerHouseNumberOrName":"46",
                   "ownerStreet":"Mayflower Road",
                   "ownerName":"Rob Freedman",
                   "ownerPostalCode":"SW9 9LA"
                }
            }]
