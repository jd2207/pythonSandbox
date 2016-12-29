import accountHolder, testUtils

class CreateMinimumAccountHolder():
  
  def __init__(self, debug=False):

    # New, default accountHolder
    self.debug=debug
    self.credentials = testUtils.TEST_CRED_MP_JOHNDICK

  def do(self):
    ah = accountHolder.AccountHolder( self.credentials, debug=self.debug )
    return ah
  
if __name__ == "__main__":
  ah = CreateMinimumAccountHolder().do()
  ah.dump()
