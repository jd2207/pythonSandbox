import utils.testUtils, endPoint.endPoint
import testData.merchants.MarketPlaceMerchants
import logging

#logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)


# ------------------------------------------------------------------------------
# Set the test merchant, accountHolderCode, virtual account code and possibly the amount and card type

mpm = testData.merchants.MarketPlaceMerchants.JohnDickMarketPlace 
  
ACCOUNT_HOLDER_CODE = "xxx"
ACCOUNT_CODE = "1234"
LIVE = False
DEBUG = True

testCard =utils.testUtils.TEST_CARD_VISA
amount = utils.testUtils.TEST_1_EUR_AMOUNT
# ------------------------------------------------------------------------------


credentials = mpm.TEST_PSP_CRED
ep = endPoint.endPoint.AuthorizePaymentEndPoint(credentials, live=LIVE, debug=DEBUG)
testMerchantAccount = mpm.TEST_MERCHANT_NAME

merchantRef = utils.testUtils.timestampMerchantRef()
paymentRequest = utils.testUtils.CardPayment (testMerchantAccount, amount, testCard, merchantReference=merchantRef).paymentReq

paymentRequest["additionalData"] = {
      "split.api":1,
      "split.nrOfItems":1,
      "split.totalAmount": amount["value"],
      "split.currencyCode": amount["currency"],
      "split.item1.reference":"to " + ACCOUNT_HOLDER_CODE,
      "split.item1.description":"test",
      "split.item1.type":"MarketPlace",
      "split.item1.amount" : amount["value"],
      "split.item1.account" : ACCOUNT_CODE
    }
  
ep.sendRequest(paymentRequest)


'''
# Basic TEST split payment --------------------------------------------------------------
credentials = testUtils.TEST_CRED_PAYMENT
endPoint = endPoint.AuthorizePaymentEndPoint(credentials, 'test', debug=True)

testMerchantAccount = "JohnDickMarketPlace"
testCard = testUtils.TEST_CARD_VISA
  
amount = { 'value' : 500, 'currency' : 'EUR' }


# LIVE basic payment --------------------------------------------------------------
credentials = utils.testUtils.TEST_CRED_LIVE_PAYMENT
endPoint = endPoint.endPoint.AuthorizePaymentEndPoint(credentials, 'live')
testCard = utils.testUtils.JOHN_VISA
testMerchantAccount = "TestMarketPlaceMerchant"
amount = { 'value' : 100, 'currency' : 'GBP' }
'''


