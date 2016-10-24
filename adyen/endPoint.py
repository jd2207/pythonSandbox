import requests   # See http://docs.python-requests.org/en/master/api/
import json, testUtils


class AbstractEndPoint(object):

	def __init__(self, credentials=None, debug=False):
		self.setURL()
		self.credentials=credentials				# default credentials for the endpoint
		self.debug = debug

	def sendRequest(self, endPointRequest, auth=None):
		credentials = auth if auth else self.credentials		# override default credentials
		self.request = endPointRequest
		resp = requests.post(self.url, auth=credentials, json=endPointRequest)
		self.response = resp.json()
		self.httpResp = resp.status_code
		
		if self.debug:
			self.transactionDump()
		
		return self.httpResp
		
	def getRequest(self):
		return self.request

	def getResponse(self):
		return self.response
	
	def dumpRequest(self):
		return json.dumps(self.getRequest(), sort_keys=True, indent=4)

	def dumpResponse(self):
		return json.dumps(self.getResponse(), sort_keys=True, indent=4)
	
	def transactionDump(self):
		print '\n======================================================\n'
		print ' >>> Sending JSON to endpoint: %s\n\n' % self.url
		print ' >>> JSON request... \n%s\n\n' % self.dumpRequest()
		print ' <<< Http response: %s\n' % self.httpResp
		print ' <<< JSON response... \n%s\n' % self.dumpResponse()
		print '======================================================\n'
		

# ----------------------------------------------------------------------------------
#  Standard PSP authorize endpoint 
# ----------------------------------------------------------------------------------

class AuthorizePaymentEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://pal-test.adyen.com/pal/servlet/Payment/v12/authorise'


# ----------------------------------------------------------------------------------
#  Marketpay specific endpoints 
# ----------------------------------------------------------------------------------

class CreateAccountHolderEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-test.adyen.com/cal/services/Account/v1/createAccountHolder'

class GetAccountHolderEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-test.adyen.com/cal/services/Account/v1/getAccountHolder'

class GetAccountStateConfiguration(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-test.adyen.com/cal/services/Account/v1/getAccountStateConfiguration'

class UploadDocumentEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-test.adyen.com/cal/services/Account/v1/uploadDocument'

class AccountHolderBalanceEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-test.adyen.com/cal/services/Fund/v1/accountHolderBalance'



if __name__ == "__main__":
	
	# Basic authorization --------------------------------------------------------------
	credentials = ('ws_586199@Company.AdyenTechSupport', 'Q*-h6a?8Ut!qU<Q(F2y1br{MM')
	endPoint = AuthorizePaymentEndPoint(credentials, debug=True)

	testMerchantAccount = "JohnDick"
	testCard = testUtils.TEST_CARD_VISA
	merchantRef = testUtils.timestampMerchantRef()
	amount = testUtils.TEST_EUR_AMOUNT

	paymentReq = testUtils.CardPayment (amount, merchantRef, testMerchantAccount, testCard).payment
	endPoint.sendRequest(paymentReq)
	