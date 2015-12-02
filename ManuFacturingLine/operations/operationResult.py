# Classes for reporting the result of factory Operations

# Operation result codes
class operationResult:      # abstract parent class
  def __init__(self):
    None
      
class opResultSuccess(operationResult):
  def __init__(self):
    self.code = 0
    self.desc = "Success"

class opResultAbort(operationResult):
  def __init__(self):
    self.code = 1
    self.desc = "User aborted"

class opResultUnexpected(operationResult):
  def __init__(self):
    self.code = 10
    self.desc = "Unexpected response"

class opResultSubprocessFail(operationResult):
  def __init__(self):
    self.code = 11
    self.desc = "Problem with subprocess execution"

class opResultDebugAdapterNoPing(operationResult):
  def __init__(self):
    self.code = 12
    self.desc = "Debug adapter not responding to pings"
    
class opResultDebugAdapterNoDXPrun(operationResult):
  def __init__(self):
    self.code = 13
    self.desc = "Debug adapter: dxp-run received unexpected response"

class opResultNoIMEIinProdDeviceData(operationResult):
  def __init__(self):
    self.code = 14
    self.desc = "IMEI not found in production device data file"

class opResultDownloadFileNotFound(operationResult):
  def __init__(self):
    self.code = 15
    self.desc = "File to be downloaded not found"

class opResultTestMode(operationResult):
  def __init__(self):
    self.code = 99
    self.desc = "Test mode in operation"

    
    
