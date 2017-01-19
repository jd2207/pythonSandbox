#! /usr/bin/python

import endPoint.endPoint, utils.testUtils
import testData.individuals
import testData.merchants.marketPlaceMerchants

from testData.misc import MP_TEST_ADDRESS, MP_LIMITEDPAYOUTCITY

import json, argparse, sys, logging, time, copy


# ---------------------------------------------------------------------------------------------------------------------------------------------------------
#  Constants
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

DEFAULT_MERCHANT_CATEGORY_CODE = '7999'

LIMITED_PROCESSING = 'LimitedProcessing'
LIMITED_PAYOUT = 'LimitedPayout'
LIMITLESS_PROCESSING = 'LimitlessProcessing'
LIMITLESS_PAYOUT = 'LimitlessPayout'


DEFAULT_LIMITEDPROCESSING = { 
  "allowPayout": "false", 
  "allowProcessing": "true", 
  "stateLimit": {
    "amount": 500000, 
    "currency": "EUR"
    }, 
  "stateType": LIMITED_PROCESSING
  }

DEFAULT_LIMITEDPAYOUT = {
  "allowPayout": "true", 
  "allowProcessing": "false", 
  "stateLimit": {
    "amount": 500000, 
    "currency": "EUR"
    }, 
  "stateType": LIMITED_PAYOUT
  }

DEFAULT_LIMITLESSPROCESSING = {
  "allowPayout": "false", 
  "allowProcessing": "true", 
  "stateType": LIMITLESS_PROCESSING
  }

DEFAULT_LIMITLESSPAYOUT = {
  "allowPayout": "true", 
  "allowProcessing": "false", 
  "stateType": LIMITLESS_PAYOUT
  }


DEFAULT_LIMITEDPROCESSING_DERIVED = copy.copy(DEFAULT_LIMITEDPROCESSING)
DEFAULT_LIMITEDPROCESSING_DERIVED["derived"] = "true"

DEFAULT_LIMITEDPAYOUT_DERIVED = copy.copy(DEFAULT_LIMITEDPAYOUT)
DEFAULT_LIMITEDPAYOUT_DERIVED["derived"] = "true"

DEFAULT_LIMITLESSPROCESSING_DERIVED = copy.copy(DEFAULT_LIMITLESSPROCESSING)
DEFAULT_LIMITLESSPROCESSING_DERIVED["derived"] = "true"

DEFAULT_LIMITLESSPAYOUT_DERIVED = copy.copy(DEFAULT_LIMITLESSPAYOUT)
DEFAULT_LIMITLESSPAYOUT_DERIVED["derived"] = "true"

DEFAULT_STATE_CONFIG = [ { "AccountStateConfiguration" : DEFAULT_LIMITLESSPAYOUT_DERIVED  }, 
                         { "AccountStateConfiguration" : DEFAULT_LIMITLESSPROCESSING_DERIVED }, 
                         { "AccountStateConfiguration" : DEFAULT_LIMITEDPAYOUT_DERIVED }, 
                         { "AccountStateConfiguration" : DEFAULT_LIMITEDPROCESSING_DERIVED }
                       ]


# ---------------------------------------------------------------------------------------------------------------------------------------------------------
#  AccountHolder class 
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

class AccountHolder(object):
  '''
    class to represent marketPay accountHolder 
  '''
    
  def __init__(self, merchant, new=False, code=None, virtualAccount=None, details=None, live=False, debug=False):
    ''' 
    Creates a new accountHolder object corresponding to an accountHolder in marketpay.  
     - if new=True or not set, constructor will create a new accountHolder in the given marketplace and an accountHolder object instance.
         if no name provided for the new accountHolder, a default name is created from a timestamp.
         if optional details are provided, will use this data.
         
     - if new=False, a code name must be specified. This code name will be used to lookup an existing accountHolder from the marketplace. 
         in this case virtualAccount and details are ignored
     
     - details - used to specify a handle identifying a known person's details (as specified in testData.individuals)
         if new flag is not set, this is ignored.
         
     Notes:
       virtualAccount argument is used to read an existing marketplace accountHolder by virtual account lookup. 
       This is ignored if new flag is true or if new flag is false but code is specified. 
         
    '''

    # merchant object from merchant alias
    self.merchantAccount = testData.merchants.marketPlaceMerchants.getMerchantFromAlias(merchant)
    self.credentials = self.merchantAccount.mp_credentials
    
    self.live = live
    self.debug = debug

    logging.basicConfig(format = '%(asctime)s %(levelname)s:%(message)s', 
                        level = (logging.DEBUG if self.debug else logging.INFO ))    
    logging.debug('Merchant account: %s' % self.merchantAccount.merchantName)
    logging.debug('Credential user name: %s' % self.credentials[0])
    logging.debug('Account Holder Code: %s' % code)
    logging.debug('Live flag: %s' % self.live)
    logging.debug('Debug flag: %s' % self.debug)  
    if new:             #  means create a new accountHolder in the marketplace 
      if code:
        self.accountHolderCode = code
      else:  
      # create a new account holder with a default name
        self.accountHolderCode = utils.testUtils.uniquenameFromTimestamp()

      logging.info(' Attempting to create a new accountHolder: %s' % self.accountHolderCode)
  
      self.accountHolderDetails = testData.individuals.getDetailsFromHandle(details)  
  
      self.legalEntity = 'Individual'   # hardwired for now
        
      ep = endPoint.endPoint.CreateAccountHolderEndPoint(self.merchantAccount.mp_credentials, self.live, self.debug)
      resp = ep.sendRequest({ 
        'accountHolderCode' : self.accountHolderCode,
        'accountHolderDetails' : self.accountHolderDetails,
        'legalEntity' : self.legalEntity
        })
      if resp != 0:
        logging.error('FATAL: Not able to create new accountHolder')
        sys.exit()
      else:
        logging.info('Created new accountHolder %s' % self.accountHolderCode)
      
    else:              # means lookup an existing accountHolder from the marketplace
      
      if code: 
        self.accountHolderCode = code
        logging.info('Attempting to read accountHolder by accountHolderCode: %s' % self.accountHolderCode)
      else:
        if virtualAccount:
          self.accountHolderCode = None
          self.defaultVirtualAccountCode = virtualAccount
          logging.info('Attempting to read accountHolder by virtual account code: %s' % virtualAccount)
        else:
          logging.error('FATAL: Must specify an accountHolder code OR virtualAccount code to read an existing accountHolder' )
          sys.exit()
      
    self.refresh()
      
   
  def refresh(self):
    ''' Updates (synchs) the accountHolder object by reading all the details of the corresponding marketplace accountHolder'''
    ep = endPoint.endPoint.GetAccountHolderEndPoint( self.credentials, live=self.live, debug=self.debug )
    if self.accountHolderCode:
      resp = ep.sendRequest( { 'accountHolderCode' : self.accountHolderCode } )
    else:
      resp = ep.sendRequest ( { 'accountCode' : self.defaultVirtualAccountCode } )
 
    if resp != 0:
      logging.error('FATAL: Problem reading from accountHolder: %s' % self.accountHolderCode)
      sys.exit()
    else: 
      dataDict = ep.getJsonResponse()
      if not self.accountHolderCode:    # case where accountHolder is read via the virtual account code
        self.accountHolderCode = dataDict["accountHolderCode"]
      
      self.accountHolderDetails = dataDict["accountHolderDetails"]
 
      # accountHolderDetails       
      self.address = self.accountHolderDetails["address"] if "address" in self.accountHolderDetails.keys() else None
      self.bankAccountDetails = self.accountHolderDetails["bankAccountDetail"] if "bankAccountDetail" in self.accountHolderDetails.keys() else None
      self.email = self.accountHolderDetails["email"] if "email" in self.accountHolderDetails.keys() else None
      self.individualDetails = self.accountHolderDetails["individualDetails"] if "individualDetails" in self.accountHolderDetails.keys() else None
      self.merchantCategoryCode = self.accountHolderDetails["merchantCategoryCode"] if "merchantCategoryCode" in self.accountHolderDetails.keys() else None
      self.phoneNumber = self.accountHolderDetails["phoneNumber"] if "phoneNumber" in self.accountHolderDetails.keys() else None
    
      self.legalEntity = dataDict["legalEntity"] if "legalEntity" in dataDict.keys() else None
      self.accountStatus = dataDict["accountStatus"] if "accountStatus" in dataDict.keys() else None
      self.kycVerificationResults = dataDict["kycVerificationResults"] if "kycVerificationResults" in dataDict.keys() else None
      self.requirementsForNextState = dataDict["requirementsForNextAccountState"] if "requirementsForNextAccountState" in dataDict.keys() else None
      self.defaultVirtualAccountCode = dataDict["virtualAccounts"][0] if "virtualAccounts" in dataDict.keys() else None


  def dumptoDict(self):
    self.refresh()
    return  { 
        'accountHolder' : self.accountHolderCode, 
        'accountHolderDetails' : self.accountHolderDetails,
        'legalEntity' : self.legalEntity,
        'accountStatus' : self.accountStatus,
        'kycVerificationResults' : self.kycVerificationResults,
        'requirmentsForNextAccountState' : self.requirementsForNextState,
        "defaultVirtualAccountCode" : self.defaultVirtualAccountCode
        }
  
  
  def dump(self):
    return json.dumps( self.dumptoDict(), sort_keys=True, indent=4)


  def getConfig(self):  
    ep = endPoint.endPoint.GetAccountStateConfiguration(self.credentials, live=self.live, debug=self.debug)
    if ep.sendRequest( { "accountHolderCode" : self.accountHolderCode } ) == 0:
      return ep.getJsonResponse()["stateConfiguration"]
    else:
      logging.error('Unable to retrieve state configuration for accountHolderCode %s' % self.accountHolderCode)
      return None
      

  def update(self):
    ep = endPoint.endPoint.UpdateAccountHolderEndPoint(self.credentials, self.live, debug=self.debug)
    if ep.sendRequest( { 
        "accountHolderCode" : self.accountHolderCode,
        "accountHolderDetails" : self.accountHolderDetails
        } ) == 0:
      self.refresh()
    else:
      logging.error('FATAL: Unable perform update for accountHolderCode %s' % self.accountHolderCode)
      sys.exit()
      

    
  def getBalance(self):
    ep = endPoint.endPoint.AccountHolderBalanceEndPoint(self.credentials, live=self.live, debug=self.debug)
    resp = ep.sendRequest({ "accountHolderCode" : self.accountHolderCode }) 
    if resp == 0 or resp == 99:
      return ep.getJsonResponse()
    else:
      logging.error('FATAL: Unable get balance for accountHolderCode %s' % self.accountHolderCode)
      return None


  def refundAll(self, virtualAccountCode):
    ep = endPoint.endPoint.RefundAllEndPoint(self.credentials, self.live, debug=self.debug)
    resp = ep.sendRequest({ "accountHolderCode" : self.accountHolderCode,
                            "accountCode" : virtualAccountCode })
    if resp == 0 or resp == 99:
      return ep.getJsonResponse()
    else:
      logging.error('FATAL: Unable perform RefundAll for accountHolderCode %s' % self.accountHolderCode)
      return None
      
  
  def getTransactionList(self):
    ep = endPoint.endPoint.TransactionListEndPoint(self.credentials, self.live, debug=self.debug)
    if ( ep.sendRequest({ "accountHolderCode" : self.accountHolderCode }) ) == 0:
      return ep.getJsonResponse()
    else: 
      logging.error('FATAL: Unable get transaction list for accountHolderCode %s' % self.accountHolderCode)
      return None
      
  
  def suspend(self):
    ep = endPoint.endPoint.SuspendAccountHolderEndPoint(self.credentials, self.live, debug=self.debug)
    resp = ep.sendRequest( { "accountHolderCode" : self.accountHolderCode } )
    if resp == 0 or resp == 99:
      return ep.getJsonResponse()
    else:
      logging.error('FATAL: Unable suspend accountHolderCode %s' % self.accountHolderCode)
      return None
    
    
  def unSuspend(self):
    ep = endPoint.endPoint.UnSuspendAccountHolderEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest( { "accountHolderCode" : self.accountHolderCode } )
    return ep.getJsonResponse()


  def deleteBankAccounts(self, uuids):
    ep = endPoint.endPoint.DeleteBankAcountsEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest( { "accountHolderCode" : self.accountHolderCode,
                      "bankAccountUUIDs" : uuids
                    } )
    return ep.getJsonResponse()

    
  def getKYCCheckReviews(self):
    ep = endPoint.endPoint.GetKYCCheckReviewsEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest( { "filter" : { 
                      "accountHolderCode" : self.accountHolderCode
                      }   
                    } )
    return ep.getJsonResponse()
  
  
  def payout(self, amount, desc='', bankUuid=None, accountCode=None):
    ep = endPoint.endPoint.PayoutAccountHolderEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest ( { "accountHolderCode" : self.accountHolderCode,
                        "amount" : amount,
                        "accountCode" : accountCode,
                        "description" : desc,
                        "bankAccountUUID" : bankUuid
                      } )
    return ep.getJsonResponse() 
  
  
  def uploadDocument(self, document):
    ep = endPoint.endPoint.UploadDocumentEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest ( { "accountHolderCode" : self.accountHolderCode,
                       "documentContent" : document["content"],
                       "documentDetail" : document["detail"]
                      } )
    return ep.getJsonResponse() 


  def accountHolderTransfer(self, destination, amount, code):
    ''' Move funds from this accountHolder virtual account to the specified virtual account '''

    ep = endPoint.endPoint.TransferFundsEndPoint(self.credentials, self.live, debug=self.debug)
    resp = ep.sendRequest ({
      "sourceAccountCode" : self.defaultVirtualAccountCode,
      "destinationAccountCode" : destination,
      "amount": amount,
      "transferCode":  code
      })
    
    if resp == 0 or resp == 99:
      logging.info('Transfer %s' % 'succeeded' if resp == 0 else 'failed')
      return ep.getJsonResponse()
    else:
      logging.error('Transfer failed')
      return None


  def getStates(self):
    """ Return an array of the labels of all active states """
    states = []
    for s in self.accountStatus['states']:
      states.append(s['AccountState']['stateType'])
    return states


  def forceLimitedPayout(self):
    logging.info('Attempting to force accountHolder %s to LimitedPayout state' % self.accountHolderCode)
    
    if self.live:
      logging.error('Operation not allowed on LIVE environment')
      sys.exit()
    
    # Force to LimitedPayout
    self.accountHolderDetails['individualDetails']['name']['lastName'] = 'TestData'
    self.accountHolderDetails['address'] = MP_TEST_ADDRESS
    self.accountHolderDetails['address']['city'] = MP_LIMITEDPAYOUTCITY
    self.update() 
    
    logging.info("Waiting for 5 minutes for KYC verification...")
    time.sleep(300)

    

if __name__ == "__main__":
  ''' When used from command line, allows user to create new accountHolder or read the details of an existing accountHolder '''


  def parseArgs( ):
    desc = "Utility for creating, querying and manipulating marketpay accountHolders"
    parser = argparse.ArgumentParser(description=desc)
 
  #Mandatory arguments
    parser.add_argument( 'merchantAccount', help='merchant account')
 
  #Optional/keyword arguments
    parser.add_argument( '--accountHolderCode', help='marketpay accountHolder code.')
    parser.add_argument( '--virtualAccount', help='virtual account - ignored if accountHolder is specified')
    parser.add_argument( '--live', action='store_true', help='flag to specify the LIVE system, otherwise TEST system is assumed')
    parser.add_argument( '--person', help='String used to lookup a set of personal data')
    parser.add_argument( '--new', action='store_true', help='flag to specify if a new account holder should be created, otherwise an existing accountHolder is assumed')
    parser.add_argument( '--debug', action='store_true', help='debug flag, default = OFF')
    args = parser.parse_args()    

    if not args.new:
      if not args.accountHolderCode and not args.virtualAccount: 
        sys.exit('ERROR: No account holder code or virtual account specified')
    
    return args


  args = parseArgs()  # Parse command line arguments
  ah = AccountHolder(args.merchantAccount, new=args.new, code=args.accountHolderCode, virtualAccount=args.virtualAccount, live=args.live, details=args.person, debug=args.debug)
  ah.getBalance()
  ah.getTransactionList()