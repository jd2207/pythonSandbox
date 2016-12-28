import requests   # See http://docs.python-requests.org/en/master/api/
import json
import logging
import utils.testUtils
import sys

class AbstractEndPoint(object):

	def __init__(self, credentials, live=False, debug=False):
		self.system = 'live' if live else 'test'
		self.debug = debug
		self.setURL()
		self.credentials=credentials				# default credentials for the endpoint
		
		logging.basicConfig(format = '%(asctime)s %(levelname)s:%(message)s', 
											  level = (logging.DEBUG if self.debug else logging.INFO ))		

	def sendRequest(self, endPointRequest, retry=False):
		self.request = endPointRequest
		logging.info(' >>> Sending JSON to endpoint: %s' % self.url)
		logging.debug(' >>> JSON request: \n%s\n' % self.dumpRequest())

		retryPragma = None
		if retry:
			logging.info('Retry request!')
			retryPragma = {'pragma' : "process-retry"}
		
		try:
			resp = requests.post(self.url, auth=self.credentials, json=endPointRequest, headers=retryPragma)
		except (requests.exceptions.ConnectionError, 
					  requests.exceptions.HTTPError,
					  requests.exceptions.RequestException,
					  requests.exceptions.URLRequired,
					  requests.exceptions.TooManyRedirects,
					  requests.exceptions.Timeout)  as e:
			logging.error( "Exception during attempt to send http request: " + str(e))
		else:																										# got some kind of http response
			self.processResponse(resp)
				
		return
		
	def getRequest(self):
		return self.request

	def getResponse(self):
		return self.response
	
	def dumpRequest(self):
		return json.dumps(self.getRequest(), sort_keys=True, indent=4)

	def dumpResponse(self):
		return json.dumps(self.getResponse(), sort_keys=True, indent=4)
	
	def processResponse(self, resp):
		self.httpResp = resp.status_code
		logging.info('HTTP response: ' + str(self.httpResp))
		if self.httpResp != 200:
			logging.error('HTTP response is not 200!')
			if self.httpResp == 403:
				logging.error('FATAL: Authorization error. Web service user is %s' % str(self.credentials) )
				sys.exit()
				
		try:
			self.response = resp.json()
		except ValueError:														#	if response is NOT json
			logging.error('FATAL: Response is not JSON!')
			sys.exit()
		else:
			logging.debug(' <<< JSON response: \n%s\n' % self.dumpResponse())


	
# ----------------------------------------------------------------------------------
#  Standard PSP authorize endpoint 
# ----------------------------------------------------------------------------------

class AuthorizePaymentEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://pal-'+self.system+'.adyen.com/pal/servlet/Payment/v12/authorise'
			
	def processResponse(self, resp):

		super(AuthorizePaymentEndPoint, self).processResponse(resp)
				
		if self.httpResp == 200:
			logging.info(self.response['resultCode'])
			logging.info('PSP = ' + self.response['pspReference'])
	


# ----------------------------------------------------------------------------------
#  Marketpay specific endpoints 
# ----------------------------------------------------------------------------------

class CreateAccountHolderEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Account/v1/createAccountHolder'


class GetAccountHolderEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Account/v1/getAccountHolder'

class GetAccountStateConfiguration(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Account/v1/getAccountStateConfiguration'			

class UploadDocumentEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Account/v1/uploadDocument'
			
class AccountHolderBalanceEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Fund/v1/accountHolderBalance'
			
class UpdateAccountHolderEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Account/v1/updateAccountHolder'

class RefundAllEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Fund/v1/refundNotPaidOutTransfers'

class TransactionListEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Fund/v1/accountHolderTransactionList'

class SuspendAccountHolderEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Account/v1/suspendAccountHolder'

class UnSuspendAccountHolderEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Account/v1/unSuspendAccountHolder'

class DeleteBankAcountsEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Account/v1/deleteBankAccounts'

class GetKYCCheckReviewsEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Account/v1/getKYCCheckReviews'

class PayoutAccountHolderEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Fund/v1/payoutAccountHolder'



if __name__ == "__main__":
	
#	Example here does a basic authorization. For other examples see testEndPoint

	ep = AuthorizePaymentEndPoint(utils.testUtils.TEST_CRED_PAYMENT, debug=True)
	merchantAccount = "JohnDick"
	amount = { 'value' : 500, 'currency' : 'EUR'}
	card = utils.testUtils.TEST_CARD_VISA
		
	cardPayment = utils.testUtils.CardPayment( merchantAccount, amount, card )   
	# ep.sendRequest( cardPayment.paymentReq )

	ep.sendRequest( cardPayment.paymentReq, retry=True )

