
import requests   # See http://docs.python-requests.org/en/master/api/
import json, testUtils, datetime


class AbstractEndPoint(object):

	def __init__(self, credentials=None):
		self.setURL()
		self.credentials=credentials				# default credentials for the endpoint

	def sendRequest(self, endPointRequest, auth=None, debug=False):
		credentials = auth if auth else self.credentials		# override default credentials
		self.request = endPointRequest
		resp = requests.post(self.url, auth=credentials, json=endPointRequest)
		self.response = resp.json()
		self.httpResp = resp.status_code
		
		if debug:
			self.transactionDump()
		
		return self.httpResp
		
	def getRequest(self):
		return self.request

	def getResponse(self):
		return self.response
	
	def dumpRequest(self):
		return json.dumps(self.request, sort_keys=True, indent=4)

	def dumpResponse(self):
		return json.dumps(self.response, sort_keys=True, indent=4)
	
	def transactionDump(self):
		print '\n======================================================\n'
		print ' >>> Sending JSON to endpoint: %s\n\n' % self.url
		print ' >>> JSON request... \n%s\n\n' % self.dumpRequest()
		print ' <<< Http response: %s\n' % self.httpResp
		print ' <<< JSON response... \n%s\n' % self.dumpResponse()
		print '======================================================\n'
		


class AuthorizePaymentEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://pal-test.adyen.com/pal/servlet/Payment/v12/authorise'



if __name__ == "__main__":
	# print "For tests use module 'testEndPoint'"
	
	# Basic authorization
	credentials = ('ws_586199@Company.AdyenTechSupport', 'Q*-h6a?8Ut!qU<Q(F2y1br{MM')
	testMerchantAccount = "JohnDick"
	
	endPoint = AuthorizePaymentEndPoint(credentials)
	testCard = testUtils.TEST_CARD_VISA
	
	merchantRef = "Test @ " + str(datetime.datetime.now())
	amount = testUtils.TEST_EUR_AMOUNT
	paymentReq = testUtils.CardPayment (amount, merchantRef, testMerchantAccount, testCard).payment
	
	endPoint.sendRequest(paymentReq, debug=True)
	