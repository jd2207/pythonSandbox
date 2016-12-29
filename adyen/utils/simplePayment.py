#! /usr/bin/python

# --------------------------------------------------------------------------------------------------------------
#
#  Utility for sending Adyen payments via command line
#
#  See simplePayment --help for command line options
#
# --------------------------------------------------------------------------------------------------------------

import utils.testUtils, endPoint.endPoint
import argparse, sys
import testData.merchants.MarketPlaceMerchants


def parseArgs( ):
  desc = "Simple utility for card payments via Adyen's authorization endpoint"
  parser = argparse.ArgumentParser(description=desc)
 
  #Mandatory arguments
  parser.add_argument( 'merchantAccount', help='merchant account (destination of the payment)')
 
  #Optional arguments (some with defaults)
  parser.add_argument( '--live', action='store_true', help='flag to specify the LIVE system, otherwise TEST system is assumed')
  parser.add_argument( '--value', type=int, default=100, help='amount of currency')
  parser.add_argument( '--currency', default='EUR', help='currency code')
  parser.add_argument( '--mref', help='merchant reference')
  parser.add_argument( '--card', default='testVisa', choices=['testVisa','johnLive'], help='handle to a test credit card')
  parser.add_argument( '--retry', action='store_true', help='send as a retry (http header has pragma:process-retry)')         
  
  parser.add_argument( '--shopperStatement', help='dynamic descriptor text on shopper statement')
    
  parser.add_argument( '--split', type=int, help='split amount (marketpay split payments - this amount is attributed to the submerchant )')
  parser.add_argument( '--accountHolder', help='accountHolder (marketpay split payments)')
  parser.add_argument( '--marketPayAccount', help='virtual account (marketpay split payments)')
  
  parser.add_argument( '--debug', action='store_true', help='debug flag, default = OFF')
   
  
  args = parser.parse_args()    
  return args


if __name__ == '__main__':

  args = parseArgs()  # Parse command line arguments

# --------------------------------------------------------------------------------------------------------------
#  Post process the arguments provided 
# --------------------------------------------------------------------------------------------------------------
  amount = { "value": args.value, "currency" : args.currency }   # How much?
      
  # Set card from the 'alias' argument
  if (args.card == 'testVisa'):
    card = utils.testUtils.TEST_CARD_VISA                   # What card?
  elif (args.card == 'johnLive'):
    card = utils.testUtils.JOHN_VISA                   
  else:
    sys.exit('ERROR: Card type not available')
  
  # Create the payment
  cardPaymentReq = utils.testUtils.CardPayment( args.merchantAccount, amount, card, args.mref).paymentReq  


# Read the credentials from testData 
  if (args.merchantAccount == 'JohnDickMarketPlace'):
    credentials = testData.merchants.MarketPlaceMerchants.JohnDickMarketPlace.TEST_PSP_CRED
  elif (args.merchantAccount == 'TestMarketPlaceMerchant'):
    credentials = testData.merchants.MarketPlaceMerchants.TestMarketPlace.TEST_PSP_CRED
  else:
    sys.exit('ERROR: No credential data setup for merchant %s' % args.merchantAccount)

# Shopper statememt
  if (args.shopperStatement):
    cardPaymentReq["shopperStatement"] = args.shopperStatement


# Marketpay arguments
  if (args.split != None):
    if (args.split < 0 or args.split > amount['value']):
      sys.exit('ERROR: Invalid split amount %n' % args.split)
    else:
      if (args.accountHolder):
        ah = args.accountHolder
      else:
        sys.exit('ERROR: accountHolder code not specified')

      if (args.marketPayAccount):
        acc = args.marketPayAccount
      else:
        sys.exit('ERROR: marketpay virtual account code not specified')
      
      cardPaymentReq["additionalData"] = {
        "split.api":1,
        "split.nrOfItems":2,
        "split.totalAmount": amount['value'],
        "split.currencyCode": amount["currency"],
        "split.item1.reference":"to " + ah,
        "split.item1.description":"split test",
        "split.item1.type":"MarketPlace",
        "split.item1.amount" : args.split,
        "split.item1.account" : acc,
        "split.item2.reference":"fee",
        "split.item2.description":"split test",
        "split.item2.type":"PaymentFee",
        "split.item2.amount" : amount['value'] - args.split
        }


  if args.debug:
    print 'Merchant account: %s' % args.merchantAccount
    print 'Live flag: %s' % args.live
    print 'Amount: %s %i' % (args.currency, args.value)
    print 'Merchant reference: %s' % args.mref
    print 'Card Payment:' + utils.testUtils.jsonDump(cardPaymentReq)
    if args.retry:
      print 'This is a RETRY!'
    if args.shopperStatement:
      print 'Shopper Statement: %s' % args.shopperStatement 
    if args.split:
      print 'Split Transaction: Amount %i %s split to accountholder/account %s/%s' % (args.split, amount['currency'], args.accountHolder, args.marketPayAccount)
    print 'Debug is ON' 
  else:
    print 'Debug is OFF'
 
# JOHN LIVE CARD warning and abort
  if (args.live):
    s = raw_input('You selected card="JohnLive", press YES to continue: ')
    if (s != 'YES'):
      print ('Quitting...')
      sys.exit()

# LIVE warning and abort
  if (args.live):
    s = raw_input('You selected LIVE, press YES to continue: ')
    if (s != 'YES'):
      print ('Quitting...')
      sys.exit()
  
 
 
# --------------------------------------------------------------------------------------------------------------
#  Perform the payment 
# --------------------------------------------------------------------------------------------------------------
  
  ep = endPoint.endPoint.AuthorizePaymentEndPoint(credentials, debug=args.debug, live=args.live)
  ep.sendRequest( cardPaymentReq, retry=args.retry )
