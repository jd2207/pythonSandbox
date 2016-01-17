import threading 
from pubsub import pub

   
class Tickable(object):
  
  def __init__(self):
    self.tickNo = 0 
    self.playing = False
    self.setPeriod(1)         # default period = 1 second
    self.tickTimer = None
    
  def setPeriod(self, period):
    self.period = period
    
  def tick(self):
    """ performs the timer controlled tick sequence at least but possibly many times depending on self.playing """
    self.tickNo += 1
    self.doTick()
    print 'tick-tock'
    pub.sendMessage('Tock')
    if self.playing:
      self.tickTimer = threading.Timer(self.period, Tickable.tick, [self] )    # restart the timer
      print 'started the timer'
      self.tickTimer.start()  

  def doTick(self):
    """ Overridden by subclasses which implement tickable interface """
    pass
  
  def play(self):
    """ start timer controlled tick()s of any class implementing ticker.Tickable() """
    if not self.playing: 
      print 'Start playing...'
      self.playing = True
      self.tick()      # start tick sequence (in another thread !!)
    else:
      print 'Already playing'
    
  def pause(self):
    if self.playing:
      print 'Pause enabled'
      self.playing = False
      print 'Stopping the timer'
      self.tickTimer.cancel()
      self.tickTimer = None
    else:
      print 'Already paused'

  def toDict(self):
    return { 'period' : self.period,
             'playing?' : self.playing, 
             'tickNo' : self.tickNo,
           }



class SimpleTicker(Tickable):
  """ simple example of a subclass of ticker.Tickable """
  
  def __init__(self, value=0):
    self.value = value
    Tickable.__init__(self)

  def setValue(self, newValue=0):
    self.value = newValue
    print 'Value is set to', self.value

  def getValue(self):
    return self.value

  def doTick(self):
    self.value += 1
    print 'Value is incremented to', self.value



if __name__=="__main__":
  print "See testTicker for tests"
