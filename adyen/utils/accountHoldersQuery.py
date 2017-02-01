#! /usr/bin/python

'''
#
#   Tool to loop through a list account holder codes, apply a filter and format the list 
#
#   Defines abstract parent class AccountHolderQuery.
#
#   Child classes of this may define specific header, filter and formating
#
#   Examples when used from command line as main:
#
#       1. Single accountHolder specified:
#            accountHoldersQuery.py marketplaceMerchantName --accountHolder accountHolderCode --live --debug 
#          If accountHolder is NOT specified, user will be prompted to provide it
#
#       2. List of accountHolders provided from a file or STDIN (from a pipe)
#          a)  accountHoldersQuery.py marketplaceMerchantName --live --debug < accountHolderList.txt
#        
#          b)  egrep -o <pattern> file | accountHoldersQuery.py marketplaceMerchantName --live --debug
#
#
#   NOTE: To generate a list of newly created accountHolders use a Kibana search: 
#             classname: com.adyen.vias.rpl.marketplace.account.CreateAccountHolder AND message: <marketplacename>
#
#         then pass this through a grep filter.
#
#         For example:
#             -> classname: com.adyen.vias.rpl.marketplace.account.CreateAccountHolder AND message: GoFundMe
#             -> cut n paste this to temp.txt 
#             -> egrep -o 'GoFundMe:UID-\d{8}' temp.txt | egrep -o 'UID-\d{8}'
#
#   Also see examples in TESTS section below
#
# ------------------------------------------------------------------------------------
'''

import accountHolder.accountHolder
import sys, argparse

import utils.queriesAndFilters


DEBUG = True

def NO_FILTER(accountHolder):
  return True

def SIMPLE_VIEW(accountHolder):
  print accountHolder.accountHolderCode



class AccountHolderQuery(object):
  ''' Abstract class. Child classes define and override applyFilter, formatRow
    - see class showAccountHoldersOnly as trivial example
  ''' 
    
  def __init__(self, merchant, accountHolderCodes, live=False, debug=DEBUG):
    ''' Create a new accountHolderQuery object from a list of accountHolder codes '''
    self.merchant = merchant
    self.accountHolderCodes = accountHolderCodes
    
    self.debug = debug
    self.live = live

    self.setHeader()
    self.setFilter()
 
  def setHeader(self):
    self.header = 'Sample Header'

  def setFilter(self):
    self.filterFunct = NO_FILTER
    
  def displayRow(self, accountHolder):
    print accountHolder.accountHolderCode
   
    
  def do(self):
    
    # Output Header
    print '\n' + self.header + '\n' + ('=' * len(self.header)) + '\n'
    if len(self.accountHolderCodes) == 0:
      print ('WARNING: List of accountHolder codes is empty')
  
    # Read accountHolders which pass the filter and make a list
    found = 0 
    for ahcode in self.accountHolderCodes:
      ah = accountHolder.accountHolder.AccountHolder(self.merchant, code=ahcode, live=self.live, debug=self.debug)
      if self.filterFunct(ah):
        found += 1
        self.displayRow(ah) 
        
    # Output Footer      
    print '\nFound %i accountHolders out of %i searched.\n' % (found, len(self.accountHolderCodes))
 

# ------------------------------------------------------------------------------------------------------



   
if __name__ == '__main__':
    
# ----------------------------------------------------------------------------------------------------------    
# Tests
# ----------------------------------------------------------------------------------------------------------    

  '''
#  TESTS ONLY 
  testList = ['UID-16819842','UID-16813564','UID-16811872']
  
  # Basic query, no filter and simple view
  ahq = AccountHolderQuery('GoFundMeIE', testList, live=True)
  ahq.do()

  # Show identities
  ahq = ShowAccountHoldersIdentity('GoFundMeIE', testList, live=True)
  ahq.do()
  
  # Show KYC states
  ahq = ShowStates('GoFundMeIE', testList, live=True)
  ahq.do()

  # Show only those accountHolders in LimitedPayout 
  ahq = ShowOnlyPayoutStates('GoFundMeIE', testList, live=True)
  ahq.do()      
  
  # Show tranactionSummary Data
  ahq = ShowTransactionSummary('GoFundMeIE', testList, live=True)
  ahq.do()
  '''

  def parseArgs( ):
    desc = "Utility for querying one single marketpay accountHolder or a list of marketpay accountHolders"
    parser = argparse.ArgumentParser(description=desc)
 
  #Mandatory arguments
    parser.add_argument( 'merchantAccount', help='merchant account')
 
  #Optional/keyword arguments
    parser.add_argument( '--accountHolderCode', help='marketpay accountHolder code.')
    parser.add_argument('--query', help='alias to a known AccountHolderQuery class.')    
    parser.add_argument('inputFile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='filename of list of accountHolders (default to STDIN). Ignored if accountHolderCode arg is set.')    
    parser.add_argument( '--live', action='store_true', help='flag to specify the LIVE system, otherwise TEST system is assumed')
    parser.add_argument( '--debug', action='store_true', help='debug flag, default = OFF')
    args = parser.parse_args()    
    return args
    
  args = parseArgs()  # Parse command line arguments
  
  queryClass = getattr(utils.queriesAndFilters, args.query)

# Use single accountHolder or read from STDIN/redirecte file
  if args.accountHolderCode:
    accountHoldersList = [args.accountHolderCode]
  else:
    accountHoldersList = []
    for line in args.inputFile:
      accountHoldersList.append(str.rstrip(line))
  
# Create the query and perform it
  ahq = queryClass(args.merchantAccount, accountHoldersList, live=args.live)
  ahq.do()
