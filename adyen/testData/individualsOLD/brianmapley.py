'''
# ===========================================================================
Name  :  Brian Mapley
email  :  Brian.mapley@adyen.com
DOB   25th/4/1973
Nationality :  English
Phone number:  07721 559214 / 01933 403217
Address:  20 Oakview, Redhill Grange, Wellingborough, Northants, NN9 5YU
Number of national ID / NHS number :  NZ233877D
Bank account number / IBAN :  GB16YORK05097244801519
Bank account holder name (if different from name) MR B R MAPLEY
'''

TEST_EMAIL = "Brian.mapley@adyen.com"

TEST_INDIVIDUAL_DETAILS = {
    "name": {
      "firstName":"Brian",
      "gender":"MALE",
      "lastName":"Mapley"
      }, 
    "personalData" : {
      "dateOfBirth":"1973-04-25",
      "idNumber":"NZ233877D",
      "nationality":"GB"
      }
  }
 

TEST_ADDRESS = {
  "city":"Wellingborough",
  "country":"GB",
  "postalCode":"NN9 5YU",
  "houseNumberOrName":"20",
  "stateOrProvince":"",
  "street":"Oak View"
  }

TEST_PHONE = {
  "phoneCountryCode":"GB",
  "phoneNumber":"01933403217",
  "phoneType":"Landline"
  }

TEST_BANK_ACCOUNT_DETAILS = [
            {
                "BankAccountDetail":{
                   "iban" : "GB16YORK05097244801519",
                   "countryCode" : "GB",
                   "currencyCode" : "GBP",
                   "ownerCity":"Wellingborough",
                   "ownerHouseNumberOrName":"20",
                   "ownerName":"MR B R MAPLEY",
                   "ownerPostalCode":"NN9 5YU"
                }
            }]
