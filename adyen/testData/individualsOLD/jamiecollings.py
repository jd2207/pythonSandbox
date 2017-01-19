'''
# ===========================================================================
Jamie Alexander Collings
jamie.collings@adyen.com
17.11.1987
British
+44 7479 844 616
Flat 5 Lourdes Apartments, West Kensington, LONDON, W14 9NU
National Insurance: JK 69 84 57 B
IBAN: GB03LOYD30953617696060
Jamie A Collings
'''


TEST_EMAIL = "jamie.collings@adyen.com"

TEST_INDIVIDUAL_DETAILS = {
    "name": {
      "firstName":"Jamie",
      "gender":"MALE",
      "lastName":"Collings"
      }, 
    "personalData" : {
      "dateOfBirth":"1987-11-17",
      "idNumber":"JK 69 84 57 B",
      "nationality":"GB"
      }
  }
 

TEST_ADDRESS = {
  "city":"London",
  "country":"GB",
  "houseNumberOrName" : '5',
  "postalCode":"W14 9NU",
  "stateOrProvince":"",
  "street":"Lourdes Apartments"
  }

TEST_PHONE = {
  "phoneCountryCode":"GB",
  "phoneNumber":"+44 7479 844 616",
  "phoneType":"Mobile"
  }

TEST_BANK_ACCOUNT_DETAILS = [
            {
                "BankAccountDetail":{
                   "iban" : "GB03LOYD30953617696060",
                   "countryCode" : "GB",
                   "currencyCode" : "GBP",
                   "ownerCity":"London",
                   "ownerHouseNumberOrName":"5",
                   "ownerName":"Jamie Collings",
                   "ownerPostalCode":"W14 9NU"
                }
            }]
