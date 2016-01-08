import unittest, ticker, threading, time

# ---------------------------------------------------------------------
# Tests for Ticker
# ---------------------------------------------------------------------
class TestTicker(unittest.TestCase):

  def setUp(self):
    self.t = ticker.Tickable()

  def testTickerCreation(self):
    """ test constructor """  
    self.assertEqual(self.t.tickNo, 0)
    self.assertEqual(self.t.paused, True)
    self.assertEqual(self.t.period, 5)
    self.assertEqual(self.t.tickTimer, None)

  def testTickerTick(self):
    self.t.tick()
    self.assertTrue(isinstance(self.t.tickTimer, threading._Timer))
    self.t.tickTimer.cancel()
    self.assertTrue(self.t.tickNo, 1)

  
  def testTickerPlayPause(self):
    self.t.pause()
    self.assertEqual(self.t.paused, True)
    self.t.play()
    self.assertEqual(self.t.paused, False)

    time.sleep(11)
    self.t.play()
    self.assertEqual(self.t.paused, False)

    self.t.pause()
    self.assertEqual(self.t.paused, True)
    self.assertEqual(self.t.tickTimer, None)

  def testSimpleTicker(self):
    t = ticker.SimpleTicker()
    self.assertEqual(str(t), "{'tickNo': 0, 'pause?': True, 'period': 10, 'value': 0}")
    t.play()
    self.assertEqual(str(t), "{'tickNo': 1, 'pause?': False, 'period': 10, 'value': 1}")
    time.sleep(11)
    self.assertEqual(str(t), "{'tickNo': 2, 'pause?': False, 'period': 10, 'value': 2}")
    t.pause()
    self.assertEqual(str(t), "{'tickNo': 2, 'pause?': True, 'period': 10, 'value': 2}")
  
  def testSetValue(self):
    t = ticker.SimpleTicker()
    t.setValue(10)
    self.assertEqual(t.value, 10)
    t.setValue()
    self.assertEqual(t.value, 0)
    

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestTicker)
  unittest.TextTestRunner(verbosity=3).run(suite)

  