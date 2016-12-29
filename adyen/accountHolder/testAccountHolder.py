import accountHolder, unittest, testUtils

class TestAccountHolderCreation(unittest.TestCase):

  def setUp(self):
    self.credentials = ('ws_635247@MarketPlace.JohnDick', 'N)G^xjE#&<6Jc6r!~/mQMHM8F')
    self.maxDiff = None
    
  def test_DefaultCreation(self):
    ah1 = accountHolder.AccountHolder( self.credentials, debug=True )  #   expectedDefaultAccountHolder 
    self.assertIsInstance(ah1, accountHolder.AccountHolder)            #  is an accountHolder object

    self.assertEqual(ah1.getCode(), ah1.accountHolderCode)
    
    self.assertEqual(ah1.accountHolderDetails, testUtils.MP_TEST_ACCOUNT_HOLDER_DETAILS, 'check Default account holder details')
    self.assertEqual(ah1.getConfig(), testUtils.MP_TEST_DEFAULT_STATE_CONFIG) # 'check default state configuration limits') 
    
    self.assertEqual(ah1.legalEntity, "Individual")  #  # test legal entity
  
  # test Account Status 
    self.assertEqual(ah1.getStatus()["status"],"Active")
    self.assertEqual(ah1.getStatus()["states"],[ { "AccountState" : testUtils.MP_TEST_DEFAULT_LIMITEDPROCESSING } ] )
                                           
   #    that status = Active
   #    that there exists a stateType = LimitedProcessing
   #    that there is NO state type = LimitlessProcessing
   #    that there is no state = LimitedPayout
   #    that there is no state = LimitelessPayoit
   
   # test Requirments for next state
   
   # test kycVerifiction Results
   
# def test_CreationFromExisting(self):
   
#    ah2 = accountHolder.getAccountHolder(ah1.getCode(), self.credentials, debug=True)  # can read this accountHolder and create a new object
   # self.assertEquals(ah1.dumptoDict(), ah2.dumptoDict()) # 'loaded object should be equal to the created object')  
#    print json.dumps(ah1.dumptoDict(), sort_keys=True, indent=4)
#    print json.dumps(ah2.dumptoDict(), sort_keys=True, indent=4)


if __name__ == '__main__':
    
  suite = unittest.TestLoader().loadTestsFromTestCase(TestAccountHolderCreation)
  unittest.TextTestRunner(verbosity=3).run(suite)
