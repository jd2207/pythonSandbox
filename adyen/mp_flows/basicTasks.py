
import accountHolder.accountHolder, testData.misc

TEST_MARKETPLACE_MERCHANT = 'JohnDickMarketPlace'
LIVE_MERCHANT = 'TestMarketPlaceMerchant'

DEBUG = True



'''
# Create a new minimal accountHolder 
ah = accountHolder.accountHolder.AccountHolder(TEST_MARKETPLACE_MERCHANT, new=True, debug=True)
ah.dump()
'''

'''
# Force an existing test accountHolder to LimitedPayout
ah = accountHolder.accountHolder.AccountHolder(TEST_MARKETPLACE_MERCHANT, new=False, debug=DEBUG)
ah.forceLimitedPayout()
'''

# Upload a dummy passport to *** LIVE *** accountHolder 
ACCOUNT_HOLDER_CODE = '1484265026'
ah = accountHolder.accountHolder.AccountHolder(LIVE_MERCHANT, code=ACCOUNT_HOLDER_CODE, live=True, debug=DEBUG)
ah.uploadDocument(testData.misc.MP_TEST_PASSPORT_LIMITLESS)


