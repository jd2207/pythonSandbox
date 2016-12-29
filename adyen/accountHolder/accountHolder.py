import endPoint.endPoint, utils.testUtils, json


''' class instance '''
def getAccountHolder(accountHolderCode, auth, live=False, debug=False):
    ''' does the same as using __init__ with new flag set to false '''
    return AccountHolder(auth, new=False, code=accountHolderCode, live=live, debug=debug)


class AccountHolder(object):
  '''
    class to represent marketPay accountHolder 
  '''
    
  def __init__(self, auth, new=True, code=None, details=None, live=False, legal='Individual', debug=False, merchantAccount='JohnDickMarketPlace'):
    ''' 
    Creates a new accountHolder object corresponding to an accountHolder in marketpay. Authentication is mandatory. 
     - if new=True or not set, will create a new accountHolder in the given marketplace and an accountHolder object.  
         if no name provided for the new accountHolder, a default name is created from a timestamp.
         if details are provided, will use this data to create the accountHolder in the marketplace.
   
     - if new=False, a code name must be specified. This name will be used to lookup an existing accountHolder from the marketplace. 
         in this case details is ignored
    '''
 
    self.credentials = auth
    self.live = live
    self.debug = debug
    self.merchantAccount = merchantAccount
  
    if new:             #  means create a new accountHolder in the marketplace 
      if code:
        self.accountHolderCode = code
      else:  
      # create a new account holder with a default name
        self.accountHolderCode = utils.testUtils.uniquenameFromTimestamp()
  
      if details == None:   # default, individual 
        self.accountHolderDetails = utils.testUtils.MP_TEST_PERSON
      else:
        self.accountHolderDetails = details  # use the supplied data to create to the new accountHolder
  
      self.legalEntity = legal
        
      ep = endPoint.endPoint.CreateAccountHolderEndPoint(self.credentials, self.live, self.debug)
      ep.sendRequest({ 
                      'accountHolderCode' : self.accountHolderCode,
                      'accountHolderDetails' : self.accountHolderDetails,
                      'legalEntity' : self.legalEntity
                      })
#      resp = ep.getResponse()
#      self.attribsFromDict(resp)      # set the attributes based on the response
    
    else:              # means lookup an existing accountHolder from the marketplace
      self.accountHolderCode = code
      
    self.refresh()
      
   
  def refresh(self):
    ep = endPoint.endPoint.GetAccountHolderEndPoint( self.credentials, live=self.live, debug=self.debug )
    ep.sendRequest( { 'accountHolderCode' : self.accountHolderCode } )
    resp = ep.getResponse()
    self.attribsFromDict(resp)      # set the attributes based on the response
      
    
  def attribsFromDict(self, dataDict):
      
    self.accountHolderDetails = dataDict["accountHolderDetails"]
        
    self.address = self.accountHolderDetails["address"] if "address" in self.accountHolderDetails.keys() else None
    self.bankAccountDetails = self.accountHolderDetails["bankAccountDetail"] if "bankAccountDetail" in self.accountHolderDetails.keys() else []
    self.email = self.accountHolderDetails["email"] if "email" in self.accountHolderDetails.keys() else None
    self.individualDetails = self.accountHolderDetails["individualDetails"] if "individualDetails" in self.accountHolderDetails.keys() else None
    self.merchantCategoryCode = self.accountHolderDetails["merchantCategoryCode"] if "merchantCategoryCode" in self.accountHolderDetails.keys() else None
    self.phoneNumber = self.accountHolderDetails["phoneNumber"] if "phoneNumber" in self.accountHolderDetails.keys() else None
      
    if "legalEntity" in dataDict.keys() and dataDict["legalEntity"]:
      self.legalEntity = dataDict["legalEntity"]
      
    self.accountStatus = dataDict["accountStatus"] if "accountStatus" in dataDict.keys() else None
    self.kycVerificationResults = dataDict["kycVerificationResults"] if "kycVerificationResults" in dataDict.keys() else None
    self.requirementsForNextState = dataDict["requirementsForNextAccountState"] if "requirementsForNextAccountState" in dataDict.keys() else None
    self.defaultVirtualAccountCode = dataDict["virtualAccounts"][0] if "virtualAccounts" in dataDict.keys() else None


  def dumptoDict(self):
    self.refresh()
    return  { 'accountHolder' : self.accountHolderCode, 
              'accountHolderDetails' : self.accountHolderDetails,
              'accountStatus' : self.accountStatus,
              'legalEntity' : self.legalEntity,
              'kycVerificationResults' : self.kycVerificationResults,
              'requirmentsForNextAccountState' : self.requirementsForNextState,
              "defaultVirtualAccountCode" : self.defaultVirtualAccountCode
            }
  
  
  def dump(self):
    return json.dumps( self.dumptoDict(), sort_keys=True, indent=4)


  def getConfig(self):  
    ep = endPoint.endPoint.GetAccountStateConfiguration(self.credentials, live=self.live, debug=self.debug)
    ep.sendRequest( { "accountHolderCode" : self.accountHolderCode } )
    return ep.getResponse()["stateConfiguration"]

  def getCode(self):
    return self.accountHolderCode
  
  def getDefaultVirtualAccount(self):
    return self.defaultVirtualAccountCode
  
  def getStatus(self):
    self.refresh()
    return self.accountStatus
  
  def getBalance(self):
    ep = endPoint.endPoint.AccountHolderBalanceEndPoint(self.credentials, live=self.live, debug=self.debug)
    ep.sendRequest( { "accountHolderCode" : self.accountHolderCode } )
    return ep.getResponse()  
  
  def getKYCVerificationResults(self):
    self.refresh()
    return self.kycVerificationResults
    
  def update(self, accountHolderDetails):
    ep = endPoint.endPoint.UpdateAccountHolderEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest( { "accountHolderCode" : self.accountHolderCode,
                      "accountHolderDetails" : accountHolderDetails
                    } )
    self.refresh()

  def updateForceLimitedPayout(self):
    self.refresh()
    ahd = self.accountHolderDetails
    ahd["individualDetails"]["name"]["lastName"] = "TestData"
    
    ahd["individualDetails"]["personalData"] = { "dateOfBirth":"1970-01-01",
                                                 "idNumber":"1234567890",
                                                 "nationality":"NL"
                                               }
    ahd["address"] = utils.testUtils.MP_TEST_ADDRESS_LIMITEDPAYOUTCITY
    ahd["phoneNumber"] = utils.testUtils.MP_TEST_PHONE_NUMBER
    ahd["bankAccountDetails"] = [{  
      "BankAccountDetail" : utils.testUtils.MP_TEST_BANK_ACCOUNT_DETAIL_NO_IBAN
      }]
    self.update(ahd)
  
  
  def refundAll(self, virtualAccountCode):
    ep = endPoint.endPoint.RefundAllEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest( { "accountHolderCode" : self.accountHolderCode,
                      "accountCode" : virtualAccountCode
                    } )
    return ep.getResponse()
  
  
  def getTransactionList(self):
    ep = endPoint.endPoint.TransactionListEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest( { "accountHolderCode" : self.accountHolderCode
                    } )
    return ep.getResponse()
  
  def suspend(self):
    ep = endPoint.endPoint.SuspendAccountHolderEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest( { "accountHolderCode" : self.accountHolderCode
                    } )
    return ep.getResponse()
    
  def unSuspend(self):
    ep = endPoint.endPoint.UnSuspendAccountHolderEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest( { "accountHolderCode" : self.accountHolderCode
                    } )
    return ep.getResponse()

  def deleteBankAccounts(self, uuids):
    ep = endPoint.endPoint.DeleteBankAcountsEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest( { "accountHolderCode" : self.accountHolderCode,
                      "bankAccountUUIDs" : uuids
                    } )
    return ep.getResponse()
    
  def getKYCCheckReviews(self):
    ep = endPoint.endPoint.GetKYCCheckReviewsEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest( { "filter" : { 
                          "accountHolderCode" : self.accountHolderCode
                       }   
                    } )
    return ep.getResponse()
  
  
  def payout(self, amount, desc='', bankUuid=None, accountCode=None):
    ep = endPoint.endPoint.PayoutAccountHolderEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest ( { "accountHolderCode" : self.accountHolderCode,
                        "amount" : amount,
                        "accountCode" : accountCode,
                        "description" : desc,
                        "bankAccountUUID" : bankUuid
                        } )
    return ep.getResponse() 
  
  
  def uploadDocument(self, document):
    ep = endPoint.endPoint.UploadDocumentEndPoint(self.credentials, self.live, debug=self.debug)
    ep.sendRequest ( { "accountHolderCode" : self.accountHolderCode,
                        "documentContent" : document["content"],
                        "documentDetail" : document["detail"]
                        } )
    return ep.getResponse() 
  
  
  def simpleSplitPayment(self, auth, virtualAccount, amount):
    # amount like  { 'value' : 500, 'currency' : 'EUR' }
    
    ep = endPoint.endPoint.AuthorizePaymentEndPoint(auth, self.live, debug=self.debug)
    testCard = utils.testUtils.TEST_CARD_VISA
    merchantRef = utils.testUtils.timestampMerchantRef()

    paymentReq = utils.testUtils.CardPayment (amount, merchantRef, self.merchantAccount, testCard).payment
    paymentReq["additionalData"] = {
      "split.api":1,
      "split.nrOfItems":1,
      "split.totalAmount": amount["value"],
      "split.currencyCode": amount["currency"],
      "split.item1.reference":"to " + self.accountHolderCode,
      "split.item1.description":"test",
      "split.item1.type":"MarketPlace",
      "split.item1.amount":amount["value"],
      "split.item1.account": virtualAccount
    }

    utils.testUtils.jsonPrint(paymentReq)
    ep.sendRequest(paymentReq)

    

if __name__ == "__main__":
   
  '''
  See queries folder for sample usage
  '''
  
  '''
# Create new, default name, get default values
  ah1 = AccountHolder( credentials, debug=True )
  ah2 = getAccountHolder(ah1.getAccountHolderCode(), credentials, debug=True)
  print ah1.dumptoDict()
  print ah2.dumptoDict() 
  '''

  '''
# Create new and provide a name to use, otherwise get default values)
  name = utils.testUtils.uniquenameFromTimestamp()
  ah2 = AccountHolder( credentials, name )
  print ah2.dump()
  '''
  
  '''
# Create new with specific details
  accountHolderDetails = \
    { 
      "email":"someemail@gmail.com",
      "individualDetails": { 
        "name": { 
          "firstName":"TestFirstName",
          "gender":"MALE",
          "lastName":"TestData"
        }
      },
      "address": {
        "city":"CITY",
        "country":"US",
        "postalCode":"12345",
        "stateOrProvince":"NH",
        "street":"Teststreet 1"
      },
      "phoneNumber":{
        "phoneCountryCode":"NL",
        "phoneNumber":"0612345678",
        "phoneType":"Mobile"
      }
    }
  
  ah3 = AccountHolder( credentials, details=accountHolderDetails )
  print ah3.dump()
  '''
