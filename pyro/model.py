
class model:
  def __init__(self):
    print 'created a new model'
    self.value = 0
  
  def increment(self):
    self.value += 1
    print 'incremented the value'
    
  def decrement(self):
    self.value -= 1
    print 'decremented the value'
    
  def __str__(self):
    return str(self.value)

if __name__=="__main__":
  m = model()
  print m
  m.increment()
  print m
  m.decrement()
  print m

    