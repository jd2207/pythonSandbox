import endPoint
import unittest, utils.testUtils

class TestEndPoint(unittest.TestCase):

  def setUp(self):
    self.setCredentials()
    self.setEndPoint(self.credentials)
 
  def setCredentials(self):
    ''' To be overridden by child classes '''

  def setEndPoint(self, credentials):
    ''' To be overridden by child classes '''

  def createRequest(self):
    ''' To be overridden by child classes '''
         
  def sendRequest(self):
    self.endPoint.sendRequest(self.request)
      
  def validateHttpResponse(self):
    self.assertEqual(self.endPoint.httpResp, 200)  #     'Is HTTP response code = 200'

  def validateJsonResponse(self): 
    ''' To be overridden by child classes '''
  
  def test_Request(self):
    self.createRequest()
    self.sendRequest()
    self.validateHttpResponse()
    self.validateJsonResponse() 

    
class TestBasicAuthorization(TestEndPoint):
 
    def setCredentials(self):
      self.credentials = utils.testUtils.TEST_CRED_PAYMENT
    
    def setEndPoint(self, credentials):
      self.endPoint = endPoint.AuthorizePaymentEndPoint(credentials)
    
    def createRequest(self):
      testMerchantAccount = "JohnDick"
      testCard = utils.testUtils.TEST_CARD_VISA
      merchantRef = utils.testUtils.timestampMerchantRef()
      amount = utils.testUtils.TEST_1_EUR_AMOUNT
      self.request = utils.testUtils.CardPayment (testMerchantAccount, amount, testCard, merchantRef).paymentReq
    
    def validateJsonResponse(self):
      resp = self.endPoint.getResponse()
      self.assertEqual(resp["resultCode"], 'Authorised')  #  "Is payment authorized?"

  

if __name__ == '__main__':
    
  suite = unittest.TestLoader().loadTestsFromTestCase(TestBasicAuthorization)
  unittest.TextTestRunner(verbosity=3).run(suite)
