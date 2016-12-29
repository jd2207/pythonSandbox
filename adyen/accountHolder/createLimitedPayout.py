import accountHolder, utils.testUtils, time

class CreateLimitedPayout():
  
  def __init__(self, debug=False):

    # New, default accountHolder
    self.debug=debug
    self.credentials = utils.testUtils.TEST_CRED_MP_JOHNDICK

  def do(self):
    ah = accountHolder.AccountHolder( self.credentials, debug=self.debug )
    ah.updateForceLimitedPayout()
    return ah
  
if __name__ == "__main__":
  ah = CreateLimitedPayout(debug=True).do()
  print ah.dump()
  print "Waiting for KYC process to complete ..."
  time.sleep(180)
  print ah.dump()