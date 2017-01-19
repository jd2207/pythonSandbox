#! /usr/bin/python

# ----------------------------------------------------------------------------------
#  Module containing CardPayment class used to perform Adyen credit card payments 
#    - May be used as a utility for creating adyen card payments via command line
# ----------------------------------------------------------------------------------

import utils.testUtils, endPoint.endPoint
import testData.merchants.marketPlaceMerchants
from testData.liveCreditCard import LIVE_CARD
import sys, logging, argparse


# ---------------------------------------------------------------------------------------------------------------------------------------------------------
#  Constants
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

TEST_1_EUR_AMOUNT = {"value": 100, "currency" : "EUR"}

# Test holders ----------------------------------------------------------------------------------
TEST_HOLDER = "John Smith" 
TEST_CHARGEBACK_HOLDER = "CHARGEBACK" 


# Test credit cards -----------------------------------------------------------------------------
TEST_CARD_VISA =  { 
  "number": "4111111111111111",                 
  "expiryMonth": "8",                           
  "expiryYear": "2018",                         
  "cvc": "737",                                 
  "holderName": TEST_HOLDER                    
  }   


# ---------------------------------------------------------------------------------------------------------------------------------------------------------
#  CardPayment class 
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

class CardPayment(object):
  
  def __init__(self, merchant, amount, creditCard, live=False, merchantReference=None, shopperStatement=None, marketPaySplit=None, debug=False):
    # marketPaySplit is a tuple like (splitAmount, splitReference, splitAccount)

    self.debug = debug
    self.live = live

    logging.basicConfig(format = '%(asctime)s %(levelname)s:%(message)s', 
                        level = (logging.DEBUG if self.debug else logging.INFO ))    

    self.credentials = merchant.psp_credentials
    self.paymentReq = \
      { "card" : creditCard,
        "amount" : amount,  
        "reference": merchantReference if merchantReference!=None else utils.testUtils.timestampMerchantRef(),                 
        "merchantAccount": merchant.merchantName
      } 

    # Shopper statememt
    if (shopperStatement):
      self.paymentReq['shopperStatement'] = shopperStatement


# Marketpay arguments
    if (marketPaySplit != None):
      splitAmount = marketPaySplit[0]['value']
      splitRef = marketPaySplit[1]
      splitAccount = marketPaySplit[2]
      
      if (splitAmount < 0 or splitAmount > amount['value']):
        sys.exit( 'ERROR: Invalid split amount %i %s' % (splitAmount['value'], splitAmount['currency']) ) 
      
      self.paymentReq["additionalData"] = {
        "split.api":1,
        "split.nrOfItems":2,
        "split.totalAmount": amount['value'],
        "split.currencyCode": amount["currency"],
        "split.item1.reference": splitRef,
        "split.item1.description":"split test",
        "split.item1.type":"MarketPlace",
        "split.item1.amount" : splitAmount,
        "split.item1.account" : splitAccount,
        "split.item2.reference":"fee",
        "split.item2.description":"split test",
        "split.item2.type":"PaymentFee",
        "split.item2.amount" : amount['value'] - splitAmount
        }
      
      logging.debug('Merchant account: %s' % merchant.merchantName)
      logging.debug('Live flag: %s' % self.live)
      logging.debug('Amount: %s %i' % (amount['currency'], amount['value']))
      logging.debug('Merchant reference: %s' % merchantReference)
      logging.debug('Card Payment:' + utils.testUtils.jsonDump(self.paymentReq))
      if shopperStatement:
        logging.debug('Shopper Statement: %s' % shopperStatement)
      if marketPaySplit:
        logging.debug('Split Transaction: Amount %i %s split to account %s' % (splitAmount, amount['currency'], splitAccount))
      
      if self.debug:
        logging.debug('Debug is ON')
      else:
        logging.info('Debug is OFF')


  def do(self, retry=False):
    if retry:
      logging.info('This is a RETRY!')
    ep = endPoint.endPoint.AuthorizePaymentEndPoint(self.credentials, debug=self.debug, live=self.live)

    resp = ep.sendRequest(self.paymentReq, retry=retry)
    logging.debug('Payment response code: %s' % resp)
    if resp == 0:
      jSonResp = ep.jsonResponse
      logging.info(jSonResp['resultCode'])
      logging.info('PSP = ' + jSonResp['pspReference'])
    else:
      logging.error('Payment failed!')
 
    return resp



if __name__ == "__main__":
  ''' For command line use. For tests / example of use see testCardPayment.py '''
   
  def parseArgs( ):
    desc = "Simple utility for card payments via Adyen's authorization endpoint"
    parser = argparse.ArgumentParser(description=desc)
 
    # Mandatory arguments
    parser.add_argument( 'merchant', help='merchant account (destination of the payment)')
 
    # Optional arguments (some with defaults)
    parser.add_argument( '--live', action='store_true', help='flag to specify the LIVE system. Card is then read from testData.liveCreditCard')
    parser.add_argument( '--value', type=int, default=100, help='amount of currency')
    parser.add_argument( '--currency', default='EUR', help='currency code')
    parser.add_argument( '--mref', help='merchant reference')
    parser.add_argument( '--card', default='testVisa', choices=['testVisa'], help='handle to a test credit card')
    parser.add_argument( '--retry', action='store_true', help='send as a retry (http header has pragma:process-retry)')         
  
    parser.add_argument( '--shopperStatement', help='dynamic descriptor text on shopper statement')
    
    parser.add_argument( '--split', type=int, help='split amount (marketpay split payments - this amount is attributed to the submerchant )')
    parser.add_argument( '--marketPayAccount', help='virtual account (marketpay split payments) - ignored if split is not specified')
  
    parser.add_argument( '--rehearse', action='store_true', help='flag. Used for debug. If set no action is done')
    parser.add_argument( '--debug', action='store_true', help='debug flag, default = OFF')
  
    args = parser.parse_args()   

    return args

  
  args = parseArgs()  # Parse command line arguments

# --------------------------------------------------------------------------------------------------------------
#  Post process the arguments provided 
# --------------------------------------------------------------------------------------------------------------
 
  # amount from value and currency
  amount = { "value": args.value, "currency" : args.currency }
  
  # merchant object from merchant alias
  merchant = testData.merchants.marketPlaceMerchants.getMerchantFromAlias(args.merchant)
  
  # marketpay case, setup the split 
  if args.split:
    if not args.marketPayAccount:
      print ('If doing a marketpay split, you must specify a virtual account code. Quitting...')
      sys.exit()
    
    split = { "value": args.split, "currency" : args.currency }
    mps = (split, 'split reference', args.marketPayAccount)
  else:
    mps = None

  # LIVE warning and abort
  if (args.live):
    s = raw_input('You selected LIVE, press YES to continue: ')
    if (s != 'YES'):
      print ('Quitting...')
      sys.exit()
    else:
      card = LIVE_CARD
  else:  
  # Set card from the 'alias' argument
    if (args.card == 'testVisa'):
      card = TEST_CARD_VISA                   # What card?
    else:
      sys.exit('ERROR: Card type not available')
   
  
# --------------------------------------------------------------------------------------------------------------
#  Create and execute the payment  
# --------------------------------------------------------------------------------------------------------------
  
  cardPaymentReq = CardPayment( 
    merchant, amount, card, 
    live=args.live, merchantReference=args.mref, shopperStatement=args.shopperStatement, marketPaySplit=mps, debug=args.debug
  ) 
  
  if not args.rehearse:
    cardPaymentReq.do()  
  else:
    print 'Created a cardPayment with these values:'
    print 'Merchant: %s' % merchant.merchantName
    print 'Amount: %i %s' % (amount['value'], amount['currency'])
    print 'Card details: %s' % utils.testUtils.jsonDump(card)
    print 'Live or Test: %s' % ('LIVE' if args.live else 'TEST')
    print 'Merchant Reference: %s' % args.mref
    print 'Shopper Statement: %s' % args.shopperStatement
    print 'Market pay split: %s' % str(mps)
    print 'Debug: %s' % 'ON' if args.debug else 'OFF'
    
  