# ---------------------------------------------------------------------------------------
# Unit testing of CardPayment module
# ---------------------------------------------------------------------------------------

import unittest
import testData.merchants.marketPlaceMerchants
from utils.cardPayment import CardPayment, TEST_1_EUR_AMOUNT, TEST_CARD_VISA


# ---------------------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------------------

TEST_MERCHANT_ALIAS = 'JohnDickMarketPlace'
DEBUG = True


# ---------------------------------------------------------------------------------------------------------------------------------------------------------
#  Unit tests for CardPayment class 
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

class TestCardPayment(unittest.TestCase):


  def setUp(self):
    self.testMerchant = testData.merchants.marketPlaceMerchants.getMerchantFromAlias(TEST_MERCHANT_ALIAS) 
 

  def test_BasicAuthorization(self):
    ''' Make basic payments to TEST_MERCHANT_ALIAS '''

    # merchant reference is a timestamp 
    cardPayment = CardPayment( self.testMerchant, TEST_1_EUR_AMOUNT, TEST_CARD_VISA )   
    resp = cardPayment.do()
    self.assertEqual(resp, 0, 'Payment response is 0')

    # merchant reference is given
    cardPayment = CardPayment( self.testMerchant, TEST_1_EUR_AMOUNT, TEST_CARD_VISA, merchantReference='basic payment' )   
    resp = cardPayment.do()
    self.assertEqual(resp, 0, 'Payment response is 0')

 
    
  def test_FailAuthorization(self):
    ''' Attempt a payment with bad credentials '''
    self.testMerchant = testData.merchants.marketPlaceMerchants.Merchant(testData.merchants.marketPlaceMerchants.BAD_AUTH_MERCHANT) 
    cardPayment = CardPayment( self.testMerchant, TEST_1_EUR_AMOUNT, TEST_CARD_VISA )   
    resp = cardPayment.do()
    self.assertNotEqual(resp, 0, 'Payment response should be non-zero!')


  def test_BasicMarketPaySplitPayment(self):
    ''' Make a basic marketpay split payment to TEST_MERCHANT_ALIAS '''
    mps = ( TEST_1_EUR_AMOUNT, 'split ref', self.testMerchant.mp_testVirtualAccount )
    cardPayment = CardPayment( self.testMerchant, TEST_1_EUR_AMOUNT, TEST_CARD_VISA, merchantReference='test split payment', marketPaySplit=mps )   
    resp = cardPayment.do()
    self.assertEqual(resp, 0, 'Payment response is 0')


    
if __name__ == '__main__':
    
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCardPayment)
  unittest.TextTestRunner(verbosity=3).run(suite)