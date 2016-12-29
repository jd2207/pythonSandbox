import flowCreateLimitedPayout, testUtils

# Create a new account, with limited payout
ah = flowCreateLimitedPayout.FlowCreateLimitedPayout(debug=True).do()
 
testUtils.jsonPrint( ah.getBalance() )
testUtils.jsonPrint( ah.getTransactionList() )
print ah.dump()

# print json.dumps( ah.refundAll('192916721') , sort_keys=True, indent=4)
