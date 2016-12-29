'''
Scenario #1 Typical, happy flow 
User uploads KYC to clear the LimitedProcessing deadline, but remains in Limited Processing.

Steps:
 New minimal account holder   =>  LimitedProcessing, no deadline
 Make payment < 100 => ditto
 Make payment > 100 => Deadline is set ACCOUNT_HOLDER_STATUS_CHANGE
 Upload KYC and Bank to move to LimitedPayout => Deadline is removed, state is now LimitedPayout
 Receive ACCOUNT_HOLDER_STATUS_CHANGE notification
 Do more processing (but less than the LimitedProcessingLimit) => should work
'''

INITIAL_KYC_LIMIT = 10000        # $ 100 

LIMITED_LIMIT = 500000    # $ 5000


import accountHolder, testUtils, time

psp_credentials = testUtils.TEST_CRED_PAYMENT
mp_credentials = testUtils.TEST_CRED_MP_JOHNDICK

print "Create a new, minimal accountHolder ..."
ah = accountHolder.AccountHolder( mp_credentials, debug=True )

print "Make a simple payment, less than the initial_kyc_needed limit"
ah.simpleSplitPayment(psp_credentials, ah.getDefaultVirtualAccount(), { 'value' : 100, 'currency' : 'EUR' })

print "Check that accountHolder as now dumped has no deadline set, and that the transaction was approved:"
ah.dump()

print "Make a simple payment than now exceeds the initial_kyc_needed limit"
ah.simpleSplitPayment(psp_credentials, ah.getDefaultVirtualAccount(), { 'value' : INITIAL_KYC_LIMIT, 'currency' : 'EUR' })

print "PAUSING FOR 1 MINUTE"
time.sleep(60)
print "Check that accountHolder as dumped below has an appropriate deadline set:"
ah.dump()

print "Now force the accountHolder to LimitedPayout"
ah.updateForceLimitedPayout()
print "PAUSING FOR 5 MINUTES"
time.sleep(300)
print "Check that accountHolder as dumped below has moved to LimitedPayout. And there is no longer a deadline"
ah.dump()

print "Check that transaction below is approved."
ah.simpleSplitPayment(psp_credentials, ah.getDefaultVirtualAccount(), { 'value' : 100, 'currency' : 'EUR' })

ah.dump()


# Add a section to now pass through LimitedPayout limit
print "Make a payment than now exceeds the LimitedPayout limit"
ah.simpleSplitPayment(psp_credentials, ah.getDefaultVirtualAccount(), { 'value' : LIMITED_LIMIT, 'currency' : 'EUR' })

print "PAUSING FOR 3 MINUTES - wait for deadline to be set"
time.sleep(180)

print "Check that accountHolder now has new accountEvent / deadline to move to Limitless Payout"
ah.dump()

