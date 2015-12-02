import factoryConfig, factoryStation, factoryOperation
import utilities 
import os.path
import operations.sendATCommand
import argparse


class resice(factoryOperation.factoryOperation):
  '''resice'''
  
  def __init__(self, factoryStation, options):
    '''Launching resice'''
    self.name = 'resice'
    self.description = resice.__doc__
    self.arch = 'win32'
    super(resice,self).__init__(factoryStation, options)
  
  def initialize(self):
    currFolderPath = os.path.abspath(os.curdir)
    self.resiceFolder = os.path.join(currFolderPath, self.options['resiceFolder'])
    self.tool =  os.path.join(self.resiceFolder, 'bin', 'resice.exe')
    if not self.factoryStation.fileExists(self.tool,'Resice tool'):
      if not self.factoryStation.testMode: return False
    
    self.configfolder = os.path.join(self.resiceFolder, 'configuration')
    if not self.factoryStation.fileExists(self.resiceFolder,'Resice configuration'):
      if not self.factoryStation.testMode: return False

    logDir = self.factoryStation.logger.dirname()
    ilgLog = os.path.join(logDir, 'resice.ilg')
    csvLog = os.path.join(logDir, 'resice.csv')
    self.logs = [ ilgLog, csvLog ]
  
    resiceConfig = self.options['resiceConfig']
    prodDefs = self.options['prodDefs']
    icalCableLossXML = self.options['cableLoss']
    icalCableLossDivXML = self.options['cableLossDiv'] 
    prodName = self.factoryStation.productName

    if not self.factoryStation.radioTester == None:
      radioTesterType = self.factoryStation.radioTester.type
      visaAddress = self.factoryStation.radioTester.visaAddress
    else:
      self.printToLog('ERROR: No radio tester specified', 0)
      if not self.factoryStation.testMode:
        return False 
      else:
        radioTesterType = 'DUMMY'
        visaAddress = 'DUMMY'
    
    stopOnFail = self.options['stopOnFail']
    self.args = [ self.tool, 
                  '--config_file=' + os.path.join( self.configfolder, resiceConfig),
                  '--product=' +  prodName,
                  '--product_dir=' + os.path.join( self.configfolder, prodDefs),
                  '--cable_loss_file=' + os.path.join(self.configfolder, icalCableLossXML),
                  '--cable_loss_div_file=' + os.path.join(self.configfolder, icalCableLossDivXML), 
                  '--radio_tester=%s' % (radioTesterType),
                  '--radio_tester_visa_address=%s' % visaAddress,
                  '--log_file=%s' % ilgLog,
                  '--cal_measurements_file_name=%s' % csvLog,
                  '--stop_on_fail=%s' % stopOnFail
                ]
    return True

  def do(self):
    if self.factoryStation.testMode and not hasattr(self.factoryStation,'modemPort'):
      comPort = 'COM999'
    else: 
      comPort = self.factoryStation.modemPort

    self.args.append('--port=%s,115200,HARDWARE' % comPort)   # port not known at initialization
    return super(resice,self).do()

  
# -------------------------------------------------  
# Testing  
# -------------------------------------------------
if __name__ == "__main__":

# Command line arguments and defaults
  parser = argparse.ArgumentParser(description='Invoke resice')
  utilities.cmdLineArgs(parser)                  # general args from parent class
  parser.add_argument( '--resiceFolder',   default = 'resice',                    help = 'Folder to find resice components')
  parser.add_argument( '--resiceConfig',   default = 'ical_system_config.xml',    help = 'Resice system configuration xml')
  parser.add_argument( '--prodDefs',       default = 'product_definitions',       help = 'Product Definitions file')
  parser.add_argument( '--cableLoss',      default = 'ical_cable_loss.xml',       help = 'Cable Loss (Main)')
  parser.add_argument( '--cableLossDiv',   default = 'ical_cable_loss.xml',       help = 'Cable Loss (Div)')
  parser.add_argument( '--stopOnFail',     default = True, action = 'store_false', help = 'Stop-on-fail')
  
  args = parser.parse_args()    

  debugLog = utilities.logger (args.trace, '', args.verbosity)

# Create a RFCV factory station 
  fs = factoryStation.factoryStation(debugLog, args.test)       # default factoryStation object
  fs.setProduct('i500_1720_att')
  fs.setRadioTester()
  
# Set options   
  if args.xml == None:            # set default values if no XML
    options = { 'resiceFolder' : args.resiceFolder,
                'resiceConfig' : args.resiceConfig,
                'prodDefs' : args.prodDefs,
                'cableLoss' : args.cableLoss,
                'cableLossDiv' : args.cableLossDiv ,
                'stopOnFail' : args.stopOnFail
              }  
  else:
    debugLog.lineOut('Getting options from XML')
    options = factoryConfig.operationsParser().itemsFromXML( args.xml, 'operation' )['resice']['subItem']
  
# Create resice operation instance (also need an sendATCommand to retrieve COM port info)
  fo1 = operations.sendATCommand.sendATCommand( fs, {'ATtool' : 'atcmd-itf' } )
  fo2 = resice( fs, options )

# Perform the operation once
  fo1.do()
  fo2.postResult( fo2.do() )
  fo2.collectLogs()
  