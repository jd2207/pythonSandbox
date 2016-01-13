import threading 
from pubsub import pub

   
class Tickable(object):
  
  def __init__(self):
    self.tickNo = 0 
    self.playing = False
    self.setPeriod(1)         # default period = 1 second
    self.tickTimer = None
    self.lastTick = 0  
    
  def setPeriod(self, period):
    self.period = period
    
  def tickSeq(self):
    """ performs the timer controlled tick sequence at least but possibly many times depending on self.lastTick """

    print 'starting the tick, lastTick: %i, tickNo: %i' % (self.lastTick, self.tickNo)

    self.tickNo += 1
    self.doTick()
    print 'tick performed'
    pub.sendMessage('Tock')
    if self.tickNo < self.lastTick:
      self.tickTimer = threading.Timer(self.period, Tickable.tickSeq, [self] )    # restart the timer
      print 'starting the timer, lastTick: %i, tickNo: %i' % (self.lastTick, self.tickNo)
      self.tickTimer.start()
    else:
      print 'reached last tick'
      self.playing = False

  def doTick(self):
    """ Overridden by subclasses which implement tickable interface """
    pass
  
  def play(self, ticksPerPlay=1):
    """ start timer controlled tick()s of any class implementing ticker.Tickable() """
    if not self.playing: 
      print 'Start playing...'
      self.playing = True
      self.lastTick = self.tickNo + ticksPerPlay 
      self.tickSeq()      # perform tick sequence (in another thread !!)
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



class SimpleTicker(Tickable):
  """ simple example of a subclass of ticker.Tickable """
  
  def __init__(self, value=0):
    self.value = value
    Tickable.__init__(self)

  def setValue(self, newValue=0):
    self.value = newValue
    print 'Value is set to', self.value

  def doTick(self):
    self.value += 1
    print 'Value is incremented to', self.value

  def __str__(self):
    return str({ 'value' : self.value, 'playing?' : self.playing, 'tickNo' : self.tickNo, 'period' : self.period })

  

if __name__=="__main__":
  print "See testTicker for tests"
