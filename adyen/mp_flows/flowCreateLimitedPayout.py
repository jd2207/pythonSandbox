import accountHolder, testUtils


# ---------------------------------------------------------------------------------------------------------
# Flow Test: Default new > Update identity & bank info to trigger KYC checks > Force LimitedPayout flow 
# ---------------------------------------------------------------------------------------------------------

class FlowCreateLimitedPayout():
  
  def __init__(self, debug=False):

    # New, default accountHolder
    self.debug=debug
    self.credentials = testUtils.TEST_CRED_MP_JOHNDICK


  def do(self):
    ah = accountHolder.AccountHolder( self.credentials, debug=self.debug )
 
    # Add required identity info
    ah.update({ "address" : testUtils.MP_TEST_ADDRESS,
             "phoneNumber" : testUtils.MP_TEST_PHONE_NUMBER
             })
  
    # Force to limited payout
    ah.updateForceLimitedPayout()
    return ah

  
if __name__ == "__main__":
  ah = FlowCreateLimitedPayout(debug=True).do()
  ah.dump()
  
  
  