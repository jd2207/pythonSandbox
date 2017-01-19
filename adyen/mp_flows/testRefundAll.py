
import accountHolder.accountHolder
import testData.testCards
import utils.cardPayment
import time, logging

# Steps:
#   Comment out Part2 and run.
#   Will create a new accountHolder and make 3 small payments to it
#   Wait for these payments to all settle then comment out Part 1 and run part2


# ---------------------------------------------------------------------------
#  Useful functions
# ---------------------------------------------------------------------------

DEBUG = True
#DEBUG = False
TEST_MARKETPLACE_MERCHANT = 'JohnDickMarketPlace'


def makeOneEuroSplitPayment(merchantAccount, marketPayAccount, mref="MP test"):

  ah = accountHolder.accountHolder.AccountHolder(merchantAccount, virtualAccount=marketPayAccount, debug=DEBUG)

  amount = testData.misc.TEST_1_EUR_AMOUNT
  card = testData.testCards.TEST_CARD_VISA                   # What card?
  split = amount                                            # Send all funds to the accountHolder
  mps = (split, 'to '+ah.accountHolderCode, marketPayAccount)
    
  cardPaymentReq = utils.cardPayment.CardPayment( merchantAccount, amount, card, mref, marketPaySplit=mps)
  cardPaymentReq.do()


# ---------------------------------------------------------------------------
#  The test flow
# ---------------------------------------------------------------------------

logging.basicConfig(format = '%(asctime)s %(levelname)s:%(message)s', level = logging.DEBUG if DEBUG else logging.INFO)

'''
# PART 1 -------------------------------------------------------------------------------------------
    # Make N payments
ah = accountHolder.accountHolder.AccountHolder(TEST_MARKETPLACE_MERCHANT, new=True, debug=True)

logging.info('Creating 3 split payments')

for i in range(0,3):
  makeOneEuroSplitPayment(TEST_MARKETPLACE_MERCHANT, ah.defaultVirtualAccountCode, 'test payment #'+str(i))

logging.info('Waiting for 3 minutes')
time.sleep(180)
    
logging.info('Attempt to suspend accountHolder %s' % ah.accountHolderCode)
resp1 = ah.suspend()
  
if (resp1 and resp1["accountStatus"]["status"] == 'Suspended'):
  logging.info('Suspend succeeded.')
else:
  logging.info('Suspend failed.')
# End PART 1-------------------------------------------------------------------------------------------------
'''

# PART 2 -------------------------------------------------------------------------------------------

# ACCOUNT_HOLDER_CODE = '1484093903'  or '1484094765'
ACCOUNT_HOLDER_CODE = '1484094765'

ah = accountHolder.accountHolder.AccountHolder(TEST_MARKETPLACE_MERCHANT, code=ACCOUNT_HOLDER_CODE, debug=True)

logging.info('Attempt to refundAll on accountHolder %s' % ah.accountHolderCode)
resp = ah.refundAll(virtualAccountCode=ah.defaultVirtualAccountCode)

if (resp and resp["resultCode"] == 'Passed'):
  logging.info('refundAll succeeded.')
else:
  logging.info('refundAll failed.')
  


# End Part 2 ---------------------------------------------------------------------------------------
    