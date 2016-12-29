import accountHolder, testUtils


# ---------------------------------------------------------------------------------------------------------
# Flow Test: Default new > Upload a passport such that PASSPORT verification state goes to PENDING_REVIEW 
# ---------------------------------------------------------------------------------------------------------

class FlowCreatePassportPendingReview():
  
  def __init__(self, debug=False):

    # New, default accountHolder
    self.debug=debug
    self.credentials = testUtils.TEST_CRED_MP_JOHNDICK


  def do(self):
    ah = accountHolder.AccountHolder( self.credentials, debug=self.debug )
    doc = testUtils.MP_TEST_DOC_PASSPORT
    ah.update( {"individualDetails" : 
                  { "name" : 
                    { "firstName" : "John",
                      "lastName" : "TestData", 
                      "gender" : "MALE"
                    } 
                  }
                } )
    
    ah.uploadDocument(doc)
    return ah

  
if __name__ == "__main__":
  ah = FlowCreatePassportPendingReview(debug=True).do()
  ah.dump()
  
  
  