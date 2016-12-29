import accountHolder, testUtils


# ---------------------------------------------------------------------------------------------------------
# Flow Test: Default new > Update identity & bank info to trigger KYC checks > Force LimitedPayout flow 
# ---------------------------------------------------------------------------------------------------------

class FlowCreateUpdateFraudSuspend():
  
  def __init__(self, debug=False):

    # New, default accountHolder
    self.debug=debug
    self.credentials = testUtils.TEST_CRED_MP_JOHNDICK


  def do(self):
    ah = accountHolder.AccountHolder( self.credentials, debug=self.debug )
 
    # Use FRAUDCITY and secondname = Testdata 
    ah.update( { "individualDetails" : 
                  { "name" : 
                    { "firstName" : "TestData",
                      "lastName" : "TestData", 
                      "gender" : "MALE"
                    } 
                  },
                 "address" : testUtils.MP_FRAUD_ADDRESS,
                 "phoneNumber" : testUtils.MP_TEST_PHONE_NUMBER
               } )
    return ah

  
if __name__ == "__main__":
  ah = FlowCreateUpdateFraudSuspend(debug=True).do()
  ah.dump()
  
  
  