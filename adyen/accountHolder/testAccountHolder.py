import unittest
import accountHolder, testData.misc
import time
import utils.testUtils

# ---------------------------------------------------------------------------
#  Constants 
# ---------------------------------------------------------------------------

TEST_MARKETPLACE_MERCHANT = 'JohnDickMarketPlace'
DEBUG = True

# ---------------------------------------------------------------------------
#  The tests 
# ---------------------------------------------------------------------------

class TestAccountHolderCreation(unittest.TestCase):

  def test_DefaultCreation(self):
    """ Create a new accountHolder with default values in the marketplace, then read it to a new accountHolder via the code"""
    ah1 = accountHolder.AccountHolder(TEST_MARKETPLACE_MERCHANT, new=True, debug=True)
    self.assertIsInstance(ah1, accountHolder.AccountHolder, 'Unable to create new accountHolder object')    
 
    # Check the state
    self.assertEqual(ah1.accountHolderDetails['email'], testData.misc.MP_TEST_EMAIL, 'Default email is wrong')
    self.assertEqual(ah1.accountHolderDetails['individualDetails'], {"name": testData.misc.MP_TEST_NAME}, 'Default name iss wrong')
    self.assertEqual(ah1.merchantCategoryCode, accountHolder.DEFAULT_MERCHANT_CATEGORY_CODE, 'Default merchant category code is wrong')
    self.assertEqual(ah1.getConfig(), accountHolder.DEFAULT_STATE_CONFIG,'Default state configuration is wronng')

    # Read this accountHolder via the accountHoder code 
    ah2 = accountHolder.AccountHolder(TEST_MARKETPLACE_MERCHANT, code=ah1.accountHolderCode, debug=True)

    self.assertEqual(ah2.accountHolderCode, ah1.accountHolderCode, 'accountHolder codes do not match ')
    self.assertEqual(ah2.accountHolderDetails['email'], testData.misc.MP_TEST_EMAIL, 'Email addresses do not match')
    self.assertEqual(ah2.accountHolderDetails['individualDetails'], {"name": testData.misc.MP_TEST_NAME}, 'Individual details do not match')
    self.assertEqual(ah2.merchantCategoryCode, accountHolder.DEFAULT_MERCHANT_CATEGORY_CODE, 'Merchant category codes do not match')
    self.assertEqual(ah2.getConfig(), accountHolder.DEFAULT_STATE_CONFIG,'State configurations do not match')
    
    # Read this accountHolder via the virtual account Code
    ah3 = accountHolder.AccountHolder(TEST_MARKETPLACE_MERCHANT, virtualAccount=ah1.defaultVirtualAccountCode, debug=True)
    self.assertEqual(ah3.accountHolderCode, ah1.accountHolderCode, 'accountHolder codes do not match ')
    self.assertEqual(ah3.defaultVirtualAccountCode, ah1.defaultVirtualAccountCode, 'virtual account codes do not match ')
    self.assertEqual(ah3.accountHolderDetails['email'], testData.misc.MP_TEST_EMAIL, 'Email addresses do not match')
    self.assertEqual(ah3.accountHolderDetails['individualDetails'], {"name": testData.misc.MP_TEST_NAME}, 'Individual details do not match')
    self.assertEqual(ah3.merchantCategoryCode, accountHolder.DEFAULT_MERCHANT_CATEGORY_CODE, 'Merchant category codes do not match')
    self.assertEqual(ah3.getConfig(), accountHolder.DEFAULT_STATE_CONFIG,'State configurations do not match')

    # Trivial test of update() method (does not trigger KYC)
    ah3.accountHolderDetails['email'] = testData.misc.MP_TEST_EMAIL2
    ah3.update()
    self.assertEqual(ah3.accountHolderDetails['email'], testData.misc.MP_TEST_EMAIL2,'Check email update')
 
    # Check the default state
    s = ah3.getStates()
    self.assertEqual(len(s), 1, 'More than one state')
    self.assertEqual(s[0], accountHolder.LIMITED_PROCESSING, 'The state is not %s' % accountHolder.LIMITED_PROCESSING)
    self.assertEqual(ah3.accountStatus['status'], 'Active', 'The state is not Active')


  def test_CreationFromKnownPersonDetails(self):
    ah = accountHolder.AccountHolder(TEST_MARKETPLACE_MERCHANT, new=True, details='TestPerson', debug=DEBUG)
    self.assertEqual(ah.accountHolderDetails['individualDetails'], {
      "name" : testData.misc.MP_TEST_NAME,
      "personalData" : testData.misc.MP_TEST_PERSONAL_DATA
      }, 'Individual details do not match')
  
  def test_UploadTestPassportLimitless(self):
    ah = accountHolder.AccountHolder(TEST_MARKETPLACE_MERCHANT, new=True, details='TestPerson', debug=DEBUG)
    doc = testData.misc.MP_TEST_PASSPORT_LIMITLESS
    ah.accountHolderDetails['individualDetails']['name']['lastName'] = 'TestData'
    ah.update() 
    ah.uploadDocument(doc)
    ah.dump()

  def test_DefaultCreationThenForceLimitedPayout(self):
    ah = accountHolder.AccountHolder(TEST_MARKETPLACE_MERCHANT, new=True, details='TestPerson', debug=DEBUG)
    ah.forceLimitedPayout()

    states = ah.getStates()
    self.assertEqual(len(states), 2, 'Should be two states')
    for s in states:
      self.assertTrue(s in (accountHolder.LIMITED_PROCESSING, accountHolder.LIMITED_PAYOUT), 'Unexpected state %s' % s)

 
  

class TestAccountHolderFunds(unittest.TestCase):

  
  def setUp(self):
    merchantAccount = 'JohnDickMarketPlace'
    ahCode = '1481325809'
    live = False
  
    self.ah = accountHolder.AccountHolder(merchantAccount, code=ahCode, live=live, debug=DEBUG)
 
 
  def test_getTxData(self):
    resp = self.ah.getTransactionData(txTypes=['Debited','Credited'])
    self.assertEqual(resp['Credited'], { "count": 4, "value": 510200 }, 'Unexpected Credited')
    self.assertEqual(resp['Debited'], { "count": 2, "value": -200 }, 'Unexpected Debited')    

 
  def test_getBalance(self):
    resp = self.ah.getBalance()
    self.assertEqual(resp['Balance'], 510000, 'Unexpected Balance')
    self.assertEqual(resp['PendingBalance'], 0, 'Unexpected PendingBalance')

    
if __name__ == '__main__':

# AccountHolder Creation tests    
#  suite = unittest.TestLoader().loadTestsFromTestCase(TestAccountHolderCreation)
#  unittest.TextTestRunner(verbosity=3).run(suite)
  
# AccountHolder reading tests  
  suite = unittest.TestLoader().loadTestsFromTestCase(TestAccountHolderFunds)
  unittest.TextTestRunner(verbosity=3).run(suite)
  
  
