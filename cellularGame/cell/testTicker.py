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

    self.t.setPeriod(10)
    self.assertEqual(self.t.period, 10)

    self.assertEqual(self.t.toDict(), {'tickNo': 0, 'playing?': False, 'period': 10})


  def testTickerTick(self):
    self.t.tick()
    self.assertEqual(self.t.toDict(), {'tickNo': 1, 'playing?': False, 'period': 1})
    self.assertEquals(self.t.tickTimer, None)
    
  def testTickerPlayPause(self):
    self.t.pause()                          # pause when already paused
    self.assertEqual(self.t.toDict(), {'tickNo': 0, 'playing?': False, 'period': 1})
    self.t.play()
    time.sleep(3.5)
    self.assertEqual(self.t.toDict(), {'tickNo': 4, 'playing?': True, 'period': 1})
    self.t.play()
    self.t.pause()                          # pause when already paused
    self.assertEqual(self.t.toDict(), {'tickNo': 4, 'playing?': False, 'period': 1})
    
  def testSimpleTicker(self):
    self.t = ticker.SimpleTicker()
    self.assertEqual(self.t.value, 0)
    self.t.play()
    time.sleep(1.5)
    self.t.setValue(100)
    time.sleep(1)
    self.assertEqual(self.t.value, 101)
    self.t.pause()
    time.sleep(5)
    self.assertEqual(self.t.value, 101)
    

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestTicker)
  unittest.TextTestRunner(verbosity=3).run(suite)
