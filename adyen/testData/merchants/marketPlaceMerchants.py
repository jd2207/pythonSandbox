


class Merchant(object):
  def __init__(self):
    None
    
    
class JohnDickMarketPlace(Merchant):
  
  TEST_MERCHANT_NAME = 'JohnDickMarketPlace'
  TEST_COMPANY_NAME = 'AdyenTechSupport' 
  TEST_MARKETPLACE_NAME = 'JohnDick'
  TEST_MP_CRED =  ( 'ws_635247' + '@MarketPlace.' +  TEST_MARKETPLACE_NAME , 'N)G^xjE#&<6Jc6r!~/mQMHM8F' )
  TEST_PSP_CRED = ( 'ws_586199' + '@Company.' +  TEST_COMPANY_NAME , 'Q*-h6a?8Ut!qU<Q(F2y1br{MM'  )


# This is on LIVE only
class TestMarketPlace(Merchant):
  
  TEST_MERCHANT_NAME = 'TestMarketPlaceMerchant'
  TEST_COMPANY_NAME = 'TestMarketPlaceCompany' 
  TEST_MARKETPLACE_NAME = 'TestMarketPlace'
  TEST_MP_CRED =  ( 'ws_032172' + '@MarketPlace.' +  TEST_MARKETPLACE_NAME , 'C>)^6p=DyJe[J&X9sqJj=L]4N' )
  TEST_PSP_CRED = ( 'ws_074722' + '@Company.' +  TEST_COMPANY_NAME , 'd9Bc{g2L>L/#+u8Y<^5SHvD3Q'  )
  
class GoFundMeIE(Merchant):
  
  TEST_MERCHANT_NAME = 'GoFundMeIE'
  TEST_COMPANY_NAME = 'GoFundMe' 
  TEST_MARKETPLACE_NAME = 'GoFundMe'
  TEST_MP_CRED =  ( 'ws_100468' + '@MarketPlace.' +  TEST_MARKETPLACE_NAME , '%H9s62gJsZYvEkU6D(+(?\cW/' )
  
  