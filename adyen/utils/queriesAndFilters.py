
# --------------------------------------------------------------------------------------
# Repository of child classes of AccountHoldersQuery and associated filter functions
# --------------------------------------------------------------------------------------

import utils.accountHoldersQuery
import re
                          

# --------------------------------------------------------------------------------------
class ShowGFMNonTest(utils.accountHoldersQuery.AccountHolderQuery):
  ''' Show all accountHolders that are NOT GFM test account '''

  def setFilter(self):
    self.filterFunct = isNotGFMTestAccountHolder  


# --------------------------------------------------------------------------------------
class ShowAccountHoldersIdentity(utils.accountHoldersQuery.AccountHolderQuery):
  ''' Show Identity name versus bank account owner names for mismatch purposes '''    
  def setHeader(self):
    self.header = 'AccountHolders of %s:\n\n'  % self.merchant
    self.header += '%20s %20s %20s %30s %40s' % ('AccountHolderCode','FirstName','LastName', 'Email', 'Bank Account Owner')
  
  def displayRow(self, accountHolder):
    individualName = accountHolder.individualDetails['name']
    print '%20s %20s %20s %30s' % ( accountHolder.accountHolderCode, 
                               individualName['firstName'],
                               individualName['lastName'],
                               accountHolder.email
                              ),
    for bankAcc in accountHolder.bankAccountDetails:
      print '%40s' % bankAcc['BankAccountDetail']['ownerName']
    else:
      print

  def setFilter(self):
    self.filterFunct = isNotGFMTestAccountHolder



# --------------------------------------------------------------------------------------
class ShowIdentitiesOfPayoutStates(ShowAccountHoldersIdentity):
  ''' Show only accountHolders which have reached any payout state '''
  def setFilter(self):
    self.filterFunct = isPayoutState

 
# --------------------------------------------------------------------------------------
class ShowStates(utils.accountHoldersQuery.AccountHolderQuery):
  ''' Show states info including deadlines '''
  def displayRow(self, accountHolder):
    print accountHolder.accountHolderCode + ': ' + str(accountHolder.getStates())
      
# --------------------------------------------------------------------------------------
class ShowTxAndKYC(utils.accountHoldersQuery.AccountHolderQuery):
  ''' Show a summary of transaction data and KYC status '''
    
  def setHeader(self):
    self.header = 'AccountHolders of %s:\n\n'  % self.merchant
    self.header += '%20s %15s %15s %15s %15s %15s %15s %15s %15s' % ('AccountHolderCode','P. Balance', 'Credited Count', 'Credited Value', 'Balance', 'Tot Payout', 'Identity', 'Bank', 'Passport')
  
  def displayRow(self, accountHolder):
    txData = accountHolder.getTransactionData()
    balances = accountHolder.getBalance()
  
    (identity, bank, passport) = (None, None, None)
    for kyc in accountHolder.kycVerificationResults:
      res = kyc['KYCVerificationResult']['verificationStatuses']
      if 'IDENTITY_VERIFICATION' in res.keys():
        identity = res['IDENTITY_VERIFICATION']
         
      if 'BANK_ACCOUNT_VERIFICATION' in res.keys():
        bank = res['BANK_ACCOUNT_VERIFICATION'] 

      if 'PASSPORT_VERIFICATION' in res.keys():
        passport = res['PASSPORT_VERIFICATION'] 
        
    print '%20s %15i %15i %15i %15i %15i %15s %15s %15s' % ( accountHolder.accountHolderCode, 
                                    balances['PendingBalance'],
                                    txData['Credited']['count'], 
                                    txData['Credited']['value'],
                                    balances['Balance'],
                                    txData['Payout']['value'],
                                    identity, bank, passport
                                  )


    
# --------------------------------------------------------------------------------------
# Filter functions
# --------------------------------------------------------------------------------------


def isNotGFMTestAccountHolder(accountHolder):
  ''' Return True if accountHolder is real, and not a GFM test '''
    
  if ( accountHolder.individualDetails['name']['firstName'] == 'Test' or
       accountHolder.individualDetails['name']['lastName'] in ('Lin' , 'Adyen', 'Ladyen', 'Tester', 'TestData', 'lad') or 
       re.search('gofundme', accountHolder.email)
      ):
    return False
  else:
    return True



def isPayoutState(accountHolder):
  ''' Return true if accountHolder has reached any payout state '''
  for state in accountHolder.getStates():
    if state['state'] in ('LimitedPayout','LimitlessPayout'):
      return True
    else:
      next
  return False
