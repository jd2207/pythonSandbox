import flowCreateLimitedPayout, json

# Create a new account, with limited payout
ah = flowCreateLimitedPayout.FlowCreateLimitedPayout(debug=True).do()
ah.dump()

# suspend it
print json.dumps( ah.suspend(), sort_keys=True, indent=4)

# un-suspendit
print json.dumps( ah.unSuspend(), sort_keys=True, indent=4)
