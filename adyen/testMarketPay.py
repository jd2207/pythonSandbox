import marketPay
import unittest, testUtils

class TestEndPoints(unittest.TestCase):

  def setUp(self):
    credentials = ('ws_635247@MarketPlace.JohnDick', 'N)G^xjE#&<6Jc6r!~/mQMHM8F')
    self.endPoint = marketPay.CreateAccountHolder(credentials)

  def testBasicAccountCreation(self):
    merchantRef = testUtils.timestampMerchantRef()
    
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



    paymentReq = testUtils.CardPayment (amount, merchantRef, self.testMerchantAccount, self.testCard).payment
    r = self.endPoint.sendRequest(paymentReq)
    self.assertEqual(r, 200)  #     'Is HTTP response code = 200')
    paymentResp = self.endPoint.getResponse()
    self.assertEqual(paymentResp["resultCode"], 'Authorised')  #  "Is payment authorized?"


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestEndPoints)
  unittest.TextTestRunner(verbosity=3).run(suite)
