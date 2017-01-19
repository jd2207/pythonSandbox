# ---------------------------------------------------------------------------------------
# Module containing EndPoint abstract class and some frequently child classes
# ---------------------------------------------------------------------------------------


import requests   # See http://docs.python-requests.org/en/master/api/
import json, logging


class AbstractEndPoint(object):
	""" A wrapper for defining endpoints and sending JSON data via http requests and handling the response (or any exceptions that occur) """
	
	def __init__(self, credentials, live=False, debug=False):
		self.system = 'live' if live else 'test'
		self.debug = debug
		self.setURL()
		self.credentials=credentials				# default credentials (http user and passwprd) for the endpoint
		self.jsonResponse = None
		
		logging.basicConfig(format = '%(asctime)s %(levelname)s:%(message)s', level = (logging.DEBUG if self.debug else logging.INFO ))		

	def sendRequest(self, endPointRequest, retry=False):
		""" Returns 0 for success, else returns an error code:
					1 - connectivity exception occurred 
					2 - response is not JSON
					99 - response is JSON, but http code is not 200 '
		"""
	
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
			self.errorCode = 1

		else:																										# got some kind of http response
			self.httpResp = resp.status_code
			logging.info('HTTP response %s' % self.httpResp)

			try:
				self.jsonResponse = resp.json()
			except ValueError:														#	if response is NOT json
				logging.error('Response is not JSON')

				if self.httpResp == 401:
					logging.error('Authentication problem: Web services user: %s' % self.credentials[0])
				
				self.errorCode = 2
			else:																					# response is JSON
				logging.debug(' <<< JSON response: \n%s\n' % self.dumpResponse())
				if self.httpResp == 200:
					self.errorCode = 0
				else: 
					logging.error('HTTP response is %s, not 200' % self.httpResp)
					self.errorCode = 99
		
		return self.errorCode
	
		
	def getRequest(self):
		return self.request


	def getJsonResponse(self):
		return self.jsonResponse

	
	def dumpRequest(self):
		return json.dumps(self.getRequest(), sort_keys=True, indent=4)


	def dumpResponse(self):
		return json.dumps(self.getJsonResponse(), sort_keys=True, indent=4)

	

# ----------------------------------------------------------------------------------
#  Standard PSP authorize endpoint 
# ----------------------------------------------------------------------------------

class AuthorizePaymentEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://pal-'+self.system+'.adyen.com/pal/servlet/Payment/v12/authorise'



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
			
class UpdateAccountHolderEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Account/v1/updateAccountHolder'

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


# Funds related ----------------------------------------------------------------------------------

class AccountHolderBalanceEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Fund/v1/accountHolderBalance'

class RefundAllEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Fund/v1/refundNotPaidOutTransfers'

class TransactionListEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Fund/v1/accountHolderTransactionList'

class PayoutAccountHolderEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Fund/v1/payoutAccountHolder'

class TransferFundsEndPoint(AbstractEndPoint):
	def setURL(self):
		self.url = 'https://cal-'+self.system+'.adyen.com/cal/services/Fund/v1/transferFunds'


if __name__ == "__main__":
	None
	#	Use testEndPoint for testing using basic authorization endpoint 
	# See accountHolder for tests of marketpay related endpoints
