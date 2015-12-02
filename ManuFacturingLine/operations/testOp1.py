import factoryStation, factoryOperation

class testOp1(factoryOperation.factoryOperation):
  '''Simple operation where all arguments to the subprocess are hard-wired''' 

  def initialize(self):
    self.args = ['ls', '-al']
    return True

if __name__ == "__main__":

  ''' Basic test -------------------------------------------------------
       Provide no log file (prints to screen only)
       Passes a default factoryStation object
       The subprocess and its arguments are hard-wired 
       Operation has no name 
       No serial number used
       No logs are collected
  '''

if __name__ == '__main__':
  fs = factoryStation.factoryStation()               # default factoryStation object
  fo = testOp1(fs)
  fo.postResult(fo.do())
