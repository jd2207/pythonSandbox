'''
Usage:

import tickable
    
class foo(tickable.tickable):
  def __init__(self, value=0):
    self.value = value
    tickable.__init__(self)

  def setProp(self, newValue=0):
    self.value = newValue
    return self.value  

  def tick(self):
    self.value += 1
    print self
            
  def __str__(self):
    return str(self.value)      

>>> a = foo()
>>> a.pulse(5)

After 5 seconds expect ...
tickable object now has value: 1

After 10 seconds expect ...
tickable object now has value: 2

After 15 seconds expect ...
tickable object now has value: 3
        
>>> a.setProp(100)

After 20 seconds expect ...
tickable object now has value: 101

>>> a.stopPulse(100)

'''

import threading
   
class Tickable:
  
  DEFAULT_PULSE = 5       # 5 seconds
  
  def __init__(self):
    self.tickNo = 0 
    
  def startPulse(self, period=DEFAULT_PULSE):
    print 'Timer expired'
    self.tick()
    self.t = threading.Timer(period, Tickable.pulse, [self, period] )    # restart the timer
    print 'Starting the timer'
    self.t.start()
    
  def stopPulse(self):
    print 'Stopping the timer'
    self.t.cancel()
        
  def tick(self):
    """ Overridden by subclasses which implement tickable interface """
                
  
  
class foo(Tickable):
  def __init__(self, value=0):
    self.value = value
    Tickable.__init__(self)

  def setProp(self, newValue=0):
    self.value = newValue
    return self.value  

  def tick(self):
    self.value += 1
    print self
            
  def __str__(self):
    return str(self.value)      
  