
import datetime


TEST_EUR_AMOUNT = {"value": 1500, "currency" : "EUR"}
 
TEST_CARD_VISA = \
      {                                      
      "number": "4111111111111111",                 
      "expiryMonth": "8",                           
      "expiryYear": "2018",                         
      "cvc": "737",                                 
      "holderName": "John Smith"                    
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