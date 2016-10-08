"""

Need to install and play with Request package on Ubuntu @ HOME 
http://requests.readthedocs.io/en/master/

"""

import requests, json


class AbstractEndPoint(object):

	def __init__(self):
		self.setURL()

	def sendRequest(self, credentials, endPointRequest):
		return requests.post(self.url, auth=credentials, json=endPointRequest).json()


class AuthorizePaymentEndPoint(AbstractEndPoint):

	def setURL(self):
		self.url = 'https://pal-test.adyen.com/pal/servlet/Payment/v12/authorise'



if __name__ == "__main__":

	user = 'ws_586199@Company.AdyenTechSupport' 
	pw = 'Q*-h6a?8Ut!qU<Q(F2y1br{MM'

	credentials = ( user,  pw )
		
	paymentJSON =  \
	{              
  		"card":   
  		{                                      
    		"number": "4111111111111111",                 
    		"expiryMonth": "8",                           
    		"expiryYear": "2018",                         
    		"cvc": "737",                                 
    		"holderName": "John Smith"                    
  		},                                              
  		"amount":
  		{                                     
    		 "value": 1500,                                
    		 "currency": "EUR"                             
  		},                                              
  		"reference": "from python",                 
  		"merchantAccount": "JohnDick"                   
	}
	

	# expectedResponseJSON = ''

	ep = AuthorizePaymentEndPoint()
	respJSON = ep.sendRequest(credentials, paymentJSON)

#	print json.dumps(respJSON, sort_keys=True, indent=4)

	print 'PSP: %s\nResult: %s' % (respJSON["pspReference"], respJSON["resultCode"])


	# then compare resp versus expected response