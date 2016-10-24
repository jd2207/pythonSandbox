
import datetime, time, json


TEST_EUR_AMOUNT = {"value": 1500, "currency" : "EUR"}
 
TEST_CARD_VISA = {                                      
    "number": "4111111111111111",                 
    "expiryMonth": "8",                           
    "expiryYear": "2018",                         
    "cvc": "737",                                 
    "holderName": "John Smith"                    
  }


MP_TEST_PERSON = {
  "email":"test@adyen.com",
  "individualDetails": {
    "name": {
      "firstName":"First name",
      "gender":"MALE",
      "lastName":"TestData"
      }
    } 
  }


class CardPayment(object):
  
  def __init__(self, amount, merchantReference, merchantAccount, card):
    self.payment = \
      { "card" : card,
        "amount" : amount,  
        "reference": merchantReference,                 
        "merchantAccount": merchantAccount
      } 

def timestampMerchantRef():
  return "Test @ " + str(datetime.datetime.now())

def uniquenameFromTimestamp():
  return int( time.mktime(datetime.datetime.now().timetuple()) ).__str__()
  
def jsonFromFile(jsonFileName):
  with open(jsonFileName) as jsonFile:    
    data = json.load(jsonFile)

  return data