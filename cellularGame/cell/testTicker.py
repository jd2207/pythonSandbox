import unittest, ticker, time

# ---------------------------------------------------------------------
#
#      *** MUST BE EXECUTED FROM COMMAND LINE ***
#      (Eclipse IDE seems to have trouble stopping threading.Timers)
#
# ---------------------------------------------------------------------


class TestTicker(unittest.TestCase):

  def setUp(self):
    self.t = ticker.Tickable()

  def testTickerCreation(self):
    """ test constructor """  
    self.assertEqual(self.t.tickNo, 0)
    self.assertEqual(self.t.playing, False)
    self.assertEqual(self.t.period, 1)
    self.assertEqual(self.t.tickTimer, None)
    self.assertEqual(self.t.lastTick, 0)

    self.t.setPeriod(10)
    self.assertEqual(self.t.period, 10)

  def testTickerTick(self):
    self.t.tickSeq()
    self.assertEqual(self.t.tickNo, 1)
    self.assertEquals(self.t.tickTimer, None)
    
    # lastTick is non zero, ticks should advance until lastTick
    self.t.lastTick = 5
    self.t.tickSeq()
    time.sleep(10)    # ticks should only take 5 seconds
    self.assertEqual(self.t.tickNo, self.t.lastTick)
    
    self.t.lastTick = 10
    self.t.tickSeq()
    time.sleep(10)    # ticks should only take 5 seconds
    self.assertEqual(self.t.tickNo, self.t.lastTick)

  def testTickerPlayPause(self):
    self.t.pause()                          # pause when already paused
    self.assertEqual(self.t.playing, False)
    self.t.play()
    self.assertEqual(self.t.tickNo, 1)
    self.assertEqual(self.t.playing, False)

    self.t.play(5)
    self.assertEqual(self.t.playing, True)
    self.t.play()     # attempt to play during playing should do nothing
    self.assertEqual(self.t.playing, True)
    time.sleep(10)    # ticks should only take 5 seconds
    self.assertEqual(self.t.playing, False)
    self.assertEqual(self.t.tickNo, 6)
    
    # ability to pause a long sequence
    self.t.play(100)
    time.sleep(10)  
    self.t.pause()
    self.assertEqual(self.t.playing, False)
    self.assertEquals(self.t.tickTimer, None)
    
  def testSimpleTicker(self):
    t = ticker.SimpleTicker()
    self.assertEqual(str(t), "{'tickNo': 0, 'playing?': False, 'period': 1, 'value': 0}")
    t.play(10)
    self.assertEqual(str(t), "{'tickNo': 1, 'playing?': True, 'period': 1, 'value': 1}")
    time.sleep(11)
    self.assertEqual(str(t), "{'tickNo': 10, 'playing?': False, 'period': 1, 'value': 10}")

    t.play(100)   # start a long sequence
    time.sleep(0.5)
    self.assertEqual(str(t), "{'tickNo': 11, 'playing?': True, 'period': 1, 'value': 11}")
    t.setValue(100)
    time.sleep(5)
    t.pause()
    self.assertEqual(str(t), "{'tickNo': 16, 'playing?': False, 'period': 1, 'value': 105}")
  

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestTicker)
  unittest.TextTestRunner(verbosity=3).run(suite)
