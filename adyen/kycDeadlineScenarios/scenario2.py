'''
Scenario #2: Lazy/inattentive CO, small campaign > $100 but no KYC before state deadline expires

Steps:
  New account holder   =>  LimitedProcessing, no deadline
  Make payment > 100  =>  LimitedProcessing state now has a deadline  
  ACCOUNT_HOLDER_STATUS_CHANGE notification
  Do some more processing => should work
  Let the deadline expire => 
  AccountHolder is made inactive; processing should fail,
  ACCOUNT_HOLDER_STATUS_CHANGE notification
  6 week limit is set
  Accountholder then provides valid KYC and Bank Info (or force to LimitedPayout on TEST) => account is now active again in LImitedPayout, ACCOUNT_HOLDER_STATUS_CHANGE
'''

import accountHolder, testUtils, time

psp_credentials = testUtils.TEST_CRED_PAYMENT
mp_credentials = testUtils.TEST_CRED_MP_JOHNDICK
  
ah = accountHolder.AccountHolder( mp_credentials, debug=True )

# Make a payment to take over initial KYC limit
initialLimit = 10100
ah.simpleSplitPayment(psp_credentials, ah.getDefaultVirtualAccount(), { 'value' : initialLimit, 'currency' : 'EUR' })

print "PAUSING FOR 5 MINUTES"
time.sleep(300)
ah.dump()
print "Check that accountHolder as dumped above has an appropriate deadline set:"


print "PAUSING TO LET THE DEADLINE EXPIRE"
time.sleep( 60 * 30 + 1)    # 30 minutes for test 
ah.dump()
print "Check that accountHolder as dumped above is now deactiveated. Also, should have received a ACCOUNT_HOLDER_STATUS_CHANGE"

print "try a transaction here, should fail"
ah.simpleSplitPayment(psp_credentials, ah.getDefaultVirtualAccount(), { 'value' : 101, 'currency' : 'EUR' })
ah.dump()
print "Check that transaction failed"


print "upload valid KYC to reactivate the accountHolder..."
ah.updateForceLimitedPayout()
print "PAUSING FOR 5 MINUTES"
time.sleep(300)
ah.dump()
print "Check that accountHolder as dumped above has moved to Limited Payout. And there is no longer a deadline. Also, should have received a ACCOUNT_HOLDER_STATUS_CHANGE"

print "make one more payment"
ah.simpleSplitPayment(psp_credentials, ah.getDefaultVirtualAccount(), { 'value' : 100, 'currency' : 'EUR' })

ah.dump()
print "Check that transaction was approved."

