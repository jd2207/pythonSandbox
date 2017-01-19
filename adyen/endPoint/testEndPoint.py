# ---------------------------------------------------------------------------------------
# Unit testing of endPoint module
# ---------------------------------------------------------------------------------------

import endPoint
import testData.merchants.marketPlaceMerchants
import unittest


# ---------------------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------------------

TEST_MERCHANT_ALIAS = 'JohnDickMarketPlace'
DEBUG = False


# ---------------------------------------------------------------------------------------
# Unit tests for Authorization endPoint
# ---------------------------------------------------------------------------------------
   
class TestAuthorizationEndPoint(unittest.TestCase):
 
  def setUp(self):
    ''' Setup a merchant and a payment request using the authorization endpoint'''
    self.testMerchant = testData.merchants.marketPlaceMerchants.getMerchantFromAlias(TEST_MERCHANT_ALIAS) 
    self.ep = endPoint.AuthorizePaymentEndPoint(self.testMerchant.psp_credentials, debug=DEBUG)
    self.request = {
      "amount": {
        "currency": "EUR", 
        "value": 100
      }, 
      "card": {
        "cvc": "737", 
        "expiryMonth": "8", 
        "expiryYear": "2018", 
        "holderName": "John Smith", 
        "number": "4111111111111111"
      }, 
      "merchantAccount": self.testMerchant.merchantName, 
      "reference": "ref"
    }
    
  def test_BasicAuthorization(self):
    ''' Happy case. Authorization is successful '''
    resp = self.ep.sendRequest(self.request)
    self.assertEqual(resp,0,'Response is %i not zero' % resp)
    self.assertEqual(self.ep.httpResp,200,'HTTP response is not zero: %s' % self.ep.httpResp)
    self.assertEqual(self.ep.jsonResponse["resultCode"], 'Authorised', 'Payment was NOT authorized') 


  def test_ConnectivityFailure(self):
    '''Example that has a connectivity failure. Should get a 1 response.'''
    raw_input('\nDisable your internet connection then press enter')
    resp = self.ep.sendRequest(self.request)
    self.assertEqual(resp,1,'Response is %i not 1' % resp)
    raw_input('\nRe-enable your internet connection then press enter')
    

  def test_WebServiceAuthorizationFailure(self):
    ''' Example with authorization failure (send unknown user). Should get a 2 response. '''
    merchant = testData.merchants.marketPlaceMerchants.Merchant(testData.merchants.marketPlaceMerchants.BAD_AUTH_MERCHANT)
    self.ep = endPoint.AuthorizePaymentEndPoint(merchant.psp_credentials, debug=DEBUG)
    resp = self.ep.sendRequest(self.request)
    self.assertEqual(resp,2,'Response is %i not 2' % resp)
    self.assertEqual(self.ep.httpResp,401,'Response is %i not 401' % self.ep.httpResp)
  
  
  def test_AttemptToQueryMPAccountHolderWhichDoesNotExist(self):
    ''' Used to test rthe case where http response is NOT 200 but contains JSON  '''
    self.ep = endPoint.GetAccountHolderEndPoint(self.testMerchant.mp_credentials, debug=DEBUG)
    resp = self.ep.sendRequest(  {'accountCode' : '9999999999'} )
    self.assertEqual(resp,99,'Response is %i not 99' % resp)
    self.assertEqual(self.ep.httpResp,422,'Response is %i - 422 expected' % self.ep.httpResp)

    

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestAuthorizationEndPoint)
  unittest.TextTestRunner(verbosity=3).run(suite)