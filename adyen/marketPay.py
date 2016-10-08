from endPoint import endPoint

class CreateAccountHolder(endPoint.AbstractEndPoint):
  def setURL(self):
    self.url = 'https://cal-test.adyen.com/cal/services/Account/v1/createAccountHolder'


if __name__ == "__main__":

# Basic marketpay test   
  credentials = ('ws_635247@MarketPlace.JohnDick', 'N)G^xjE#&<6Jc6r!~/mQMHM8F')
  ep = CreateAccountHolder(credentials)
  accountHolder = 'ah6'
  
  newAccountReq = \
      {
         "accountHolderCode" : accountHolder,
         "accountHolderDetails" :
          {
          "email":"test@adyen.com",
           "individualDetails":
            {
             "name":
              {
              "firstName":"First name",
               "gender":"MALE",
              "lastName":"TestData"
              }
            } 
          },
        "legalEntity":"Individual"
      }
      
  resp = ep.sendRequest(newAccountReq)
  print ' >>> '
  print ep.dumpRequest()
  print '<<<  '
  print 'Response status: %i' % resp
  print ep.dumpResponse()
  