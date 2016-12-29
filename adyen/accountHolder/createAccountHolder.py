import accountHolder, utils.testUtils, time

# set the person
#from fredpotter import TEST_EMAIL, TEST_ADDRESS, TEST_INDIVIDUAL_DETAILS, TEST_BANK_ACCOUNT_DETAILS, TEST_PHONE
#from robfreedman import TEST_EMAIL, TEST_ADDRESS, TEST_INDIVIDUAL_DETAILS, TEST_BANK_ACCOUNT_DETAILS, TEST_PHONE
#from testData.individuals.lukestrudwick import TEST_EMAIL, TEST_ADDRESS, TEST_INDIVIDUAL_DETAILS, TEST_BANK_ACCOUNT_DETAILS, TEST_PHONE
#from testData.individuals.brianmapley import TEST_EMAIL, TEST_ADDRESS, TEST_INDIVIDUAL_DETAILS, TEST_BANK_ACCOUNT_DETAILS, TEST_PHONE
#from testData.individuals.jamiecollings import TEST_EMAIL, TEST_ADDRESS, TEST_INDIVIDUAL_DETAILS, TEST_BANK_ACCOUNT_DETAILS, TEST_PHONE
#from testData.individuals.marcuswheelhouse import TEST_EMAIL, TEST_ADDRESS, TEST_INDIVIDUAL_DETAILS, TEST_BANK_ACCOUNT_DETAILS, TEST_PHONE
from testData.individuals.chrispinnegar import TEST_EMAIL, TEST_ADDRESS, TEST_INDIVIDUAL_DETAILS, TEST_BANK_ACCOUNT_DETAILS, TEST_PHONE
#from testData.individuals.iancampbell import TEST_EMAIL, TEST_ADDRESS, TEST_INDIVIDUAL_DETAILS, TEST_BANK_ACCOUNT_DETAILS, TEST_PHONE
#from testData.individuals.paulsimms import TEST_EMAIL, TEST_ADDRESS, TEST_INDIVIDUAL_DETAILS, TEST_BANK_ACCOUNT_DETAILS, TEST_PHONE
#from gfm import TEST_EMAIL, TEST_ADDRESS, TEST_INDIVIDUAL_DETAILS, TEST_BANK_ACCOUNT_DETAILS, TEST_PHONE
#from testData.annperry import TEST_EMAIL, TEST_ADDRESS, TEST_INDIVIDUAL_DETAILS, TEST_BANK_ACCOUNT_DETAILS, TEST_PHONE
#from pendingReviewPerson import TEST_INDIVIDUAL_DETAILS, TEST_ADDRESS, TEST_PHONE


credentials = utils.testUtils.TEST_CRED_LIVE
#credentials = testUtils.TEST_CRED_MP_JOHNDICK

ah = accountHolder.AccountHolder( credentials, debug=True, live=True )

# get 
#    ah = accountHolder.getAccountHolder(self.name, self.credentials, live=self.live, debug=True)  

ah.update({ 
            "address" : TEST_ADDRESS,
            "email" : TEST_EMAIL,
            "phoneNumber" : TEST_PHONE,
            "individualDetails" : TEST_INDIVIDUAL_DETAILS,
            "bankAccountDetails" : TEST_BANK_ACCOUNT_DETAILS
          })
    
print "Waiting for 3 minutes for KYC verification..."
time.sleep(180)
print ah.dump()
