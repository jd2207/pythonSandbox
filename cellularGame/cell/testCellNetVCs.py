import unittest, cell, cellNet, time
from pubsub import pub

class TestCellNetVCs(unittest.TestCase):
  """ Tests for CellNet Viwer/Controller objects """

  def tearDown(self):
    pub.unsubAll()
    
  def testCellNet_VC(self):
    cn = cellNet.SimpleCellTriangle([ cell.IntegerCell('Cell A', 1), 
                                      cell.IntegerCell('Cell B', 5), 
                                      cell.IntegerCell('Cell C', 7) ])
    cnvc = cellNet.CellNet_VC(cn)
    self.assertEqual(str(cnvc), '\n0: 1\n1: 5\n2: 7')

    # Use mutate() and update() to change specific cells 
    cnvc.mutateCell(0)
    self.assertEqual(str(cnvc), '\n0: 12\n1: 5\n2: 7')
    cnvc.updateCell(1, 10)
    self.assertEqual(str(cnvc), '\n0: 12\n1: 10\n2: 7')

    cnvc.play()
    cnvc.pause()
    self.assertEqual(str(cnvc), '\n0: 17\n1: 19\n2: 22')
    
    cnvc.play()
    time.sleep(2.5)
    self.assertEqual(str(cnvc), '\n0: 157\n1: 155\n2: 152')
    
    cnvc.updateCell(1, 10)
    time.sleep(1)
    cnvc.pause()
    self.assertEqual( [c.state for c in cnvc.cellNet.cells], [162, 309, 167])

  def testCellGrid_VC(self):
    """ Specific tests for BooleanGrid_VC """
    CROSS_PATTERN = \
        '------------' + '\n'\
      + '    0  1  2 ' + '\n'\
      + ' 0  -  *  - ' + '\n'\
      + ' 1  *  *  * ' + '\n'\
      + ' 2  -  *  - ' + '\n'\
      + '------------'

  # create the grid, set up the cells then link to the viewer/controller
    bcg = cellNet.BooleanCellGrid(3,3)
    (bcg.cells[0][1].state, bcg.cells[1][1].state, bcg.cells[2][1].state) = (1,1,1)
    vc = cellNet.BooleanGrid_VC(bcg)
    self.assertEqual(str(vc), '------------\n    0  1  2 \n 0  -  *  - \n 1  -  *  - \n 2  -  *  - \n------------')

  # test that underlying cell can be manipulated via the controller and the change reflected in the associated cellNet
    vc.mutateCell(1, 0)
    vc.updateCell(1, 2)
    self.assertEqual( str(vc), CROSS_PATTERN)
  
  # perform two ticks without separate thread - should still be the same as before
    vc.play()
    time.sleep(1.5)
    vc.pause()
    self.assertEqual( str(vc), CROSS_PATTERN)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCellNetVCs)
  unittest.TextTestRunner(verbosity=3).run(suite)
