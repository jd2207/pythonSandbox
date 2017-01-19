
import accountHolder.accountHolder

#fn = 'uid.txt'
#merchant = 'GoFundMeIE'

fn = 'uid.txt'
merchant = 'GoFundMeIE'


with open(fn) as f:
  for line in f.readlines():
    ahcode = line.rstrip('\n\r')
    ah = accountHolder.accountHolder.AccountHolder(merchant, code=ahcode, new=False, live=True, debug=True)
    ah.getTransactionList()