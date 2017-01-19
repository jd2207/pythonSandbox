import unittest
import utils.testUtils, testData.testCards, accountHolder, utils.cardPayment


class TestBeneficiaryTransfers(unittest.TestCase):


  def test_attemptToSendWhenZeroBalance(self):
    ''' Create two new accountHolders. Np payments. Perform a transfer from first to second ''' 
    merchantAccount = 'JohnDickMarketPlace'

    # Create accountHolder 1 (implicitly in LimitedProcessing)   
    ah1 = accountHolder.AccountHolder(merchantAccount, new=True, debug=True)
  
    # Create accountHolder 2
    ah2 = accountHolder.AccountHolder(merchantAccount, new=True, debug=True)

    resp = ah1.accountHolderTransfer(ah2.defaultVirtualAccountCode, utils.testUtils.TEST_1_EUR_AMOUNT, 'BALANCE_TRANSFER')
  
    utils.testUtils.jsonPrint(resp)
  
  
  '''
  def test_A_HappyFlow(self):
    """ Create two new accountHolders. Make a split payment to the first, force second to LimitedPayout, then perform a transfer from first to second """
    merchantAccount = 'JohnDickMarketPlace'

    # Create accountHolder 1 (implicitly in LimitedProcessing)   
    ah1 = accountHolder.AccountHolder(merchantAccount, new=True, debug=True)
    marketPayAccount = ah1.defaultVirtualAccountCode

    # Make a split payment to this    
    amount = utils.testUtils.TEST_1_EUR_AMOUNT
    mps = (amount['value'], 'to '+ah1.accountHolderCode, marketPayAccount)
    cardPaymentReq = utils.cardPayment.CardPayment( merchantAccount, amount, testData.testCards.TEST_CARD_VISA, 
                                                  'Beneficiary test', 
                                                  marketPaySplit=mps)
    cardPaymentReq.do()
    
    # Create accountHolder 2
    ah2 = accountHolder.AccountHolder(merchantAccount, new=True, debug=True)
 
    # Force accountHolder2 to LimitedPayout
    ah2.forceLimitedPayout()
 
    # Attempt to move funds from accountHolder1 to accountHolder2
    ah1.accountHolderTransfer(ah2.defaultVirtualAccountCode, amount, 'BALANCE_TRANSFER')
  '''
    
    
    
if __name__ == '__main__':
    
  suite = unittest.TestLoader().loadTestsFromTestCase(TestBeneficiaryTransfers)
  unittest.TextTestRunner(verbosity=3).run(suite)
