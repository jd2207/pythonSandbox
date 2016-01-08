import threading 
from pubsub import pub


   
class Tickable:
  
  def __init__(self, period=5):
    self.tickNo = 0 
    self.paused = True
    self.period = period
    self.tickTimer = None
    
  def play(self):
    if self.paused: 
      print 'Start playing...'
      self.paused = False
      self.tick()
    else:
      print 'Already playing'
    
  def pause(self):
    if not self.paused:
      print 'Pause enabled'
      self.paused = True
      print 'Stopping the timer'
      self.tickTimer.cancel()
      self.tickTimer = None
    else:
      print 'Already paused'

  def tick(self):
    self.tickNo += 1
    self.doTick()
    pub.sendMessage('Tock')
    self.tickTimer = threading.Timer(self.period, Tickable.tick, [self] )    # restart the timer
    print 'Re-starting the timer'
    self.tickTimer.start()
                
  def doTick(self):
    """ Overridden by subclasses which implement tickable interface """
    pass
  
  
  
class SimpleTicker(Tickable):
  """ simple example of a subclass of ticker.Tickable """
  
  def __init__(self, value=0):
    self.value = value
    self.period = 10
    Tickable.__init__(self, self.period)

  def setValue(self, newValue=0):
    self.value = newValue

  def doTick(self):
    self.value += 1
    print 'Value is incremented to', self.value

  def __str__(self):
    return str({ 'value' : self.value, 'pause?' : self.paused, 'tickNo' : self.tickNo, 'period' : self.period })

  

if __name__=="__main__":
  print "See testTicker for tests"
