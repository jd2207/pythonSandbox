import unittest
from endPoint import endPoint
from datetime import datetime

class TestEndPoints(unittest.TestCase):

  def setUp(self):
    self.credentials = ('ws_586199@Company.AdyenTechSupport', 'Q*-h6a?8Ut!qU<Q(F2y1br{MM')
    self.endPoint = endPoint.AuthorizePaymentEndPoint()
    self.testCard = endPoint.TestVisaCard().card
    self.testMerchantAccount = "JohnDick"

  def testBasicAuthorization(self):
    merchantRef = "Test @ " + str(datetime.now())
    amount = {"value": 1500, "currency" : "EUR"}
    
    payment = endPoint.CardPayment (amount, merchantRef, self.testMerchantAccount, self.testCard).payment
    respJSON = self.endPoint.sendRequest(self.credentials, payment)
    self.assertEqual(respJSON["resultCode"], 'Authorised')

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestEndPoints)
  unittest.TextTestRunner(verbosity=3).run(suite)
