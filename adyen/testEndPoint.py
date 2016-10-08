from endPoint import endPoint
import unittest, testUtils

class TestEndPoint(unittest.TestCase):

  def setUp(self):
    credentials = ('ws_586199@Company.AdyenTechSupport', 'Q*-h6a?8Ut!qU<Q(F2y1br{MM')
    self.endPoint = endPoint.AuthorizePaymentEndPoint(credentials)
    self.testCard = testUtils.TEST_CARD_VISA
    self.testMerchantAccount = "JohnDick"

  def testRequest(self):
    self.request = self.createRequest()
    self.sendRequest(self.request)
    self.validateHttpResponse()
    self.validateJsonResponse()
    
  def sendRequest(self):
    self.responsecode = self.endPoint.sendRequest(self.request)
   
  def validateHttpResp(self):
    
       
    merchantRef = testUtils.timestampMerchantRef()
    amount = testUtils.TEST_EUR_AMOUNT
    paymentReq = testUtils.CardPayment (amount, merchantRef, self.testMerchantAccount, self.testCard).payment

    # send the request
    r = self.endPoint.sendRequest(paymentReq)
  
    # test the HTTP response
    self.assertEqual(r, 200)  #     'Is HTTP response code = 200')
    
    # validate the response
    paymentResp = self.endPoint.getResponse()
    self.assertEqual(paymentResp["resultCode"], 'Authorised')  #  "Is payment authorized?"
'''
'''
    
class TestBasicAuthorization(TestEndPoint):
    
    def createRequest():
      merchantRef = testUtils.timestampMerchantRef()
      amount = testUtils.TEST_EUR_AMOUNT
      paymentReq = testUtils.CardPayment (amount, merchantRef, self.testMerchantAccount, self.testCard).payment
      
    def sendRequest(self):
      self.responsecode = self.endPoint.sendRequest(paymentReq)
      
  
    # test the HTTP response
    self.assertEqual(r, 200)  #     'Is HTTP response code = 200')
    
    # validate the response
    paymentResp = self.endPoint.getResponse()
    self.assertEqual(paymentResp["resultCode"], 'Authorised')  #  "Is payment authorized?"
    
    
'''

class TestAuthorization(TestEndPoint):
  

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestEndPoints)
  unittest.TextTestRunner(verbosity=3).run(suite)
