'''
Name: Mr Luke Strudwick
email: luke.strudwick@adyen.com
DOB: 25/02/1987
Nationality: British
Phone number: 07920032684
Adress: 18 Claycorn Court, Station Way, Claygate, KT10 0QR
Number of national ID / NHS number: JN212078C
Bank account number / IBAN: GB88LOYD30937407328749
Bank account holder name (if different from name)
'''

TEST_EMAIL = "luke.strudwick@adyen.com"

TEST_INDIVIDUAL_DETAILS = {
    "name": {
      "firstName":"Luke",
      "gender":"MALE",
      "lastName":"Strudwick"
      }, 
    "personalData" : {
      "dateOfBirth":"1987-02-25",
      "idNumber":"JN212078C",
      "nationality":"GB"
      }
  }
 

TEST_ADDRESS = {
  "city":"Claygate",
  "country":"GB",
  "postalCode":"KT10 0QR",
  "houseNumberOrName" : '18',
  "stateOrProvince":"",
  "street":"Claycorn Court"
  }

TEST_PHONE = {
  "phoneCountryCode":"GB",
  "phoneNumber":"07920032684",
  "phoneType":"Landline"
  }

TEST_BANK_ACCOUNT_DETAILS = [
            {
                "BankAccountDetail":{
                   "iban" : "GB88LOYD30937407328749",
                   "countryCode" : "GB",
                   "currencyCode" : "GBP",
                   "ownerCity":"Claygate",
                   "ownerHouseNumberOrName":"18",
                   "ownerStreet" : "Claycorn Court",
                   "ownerName":"Luke Strudwick",
                   "ownerPostalCode":"KT10 0QR"
                }
            }]
  
