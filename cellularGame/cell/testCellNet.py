import unittest, cell, cellNet
from pubsub import pub

class TestCellNets(unittest.TestCase):
  """ Tests for CellNet objects """

  def tearDown(self):
    pub.unsubAll()          # ensure no pubsub subscriptions hanging over between tests
  
  def testCellNet(self):
    """ Constructor tests for parent CellNet """
    cn = cellNet.CellNet()
    self.assertEqual(cn.cells, [])
    self.assertEqual(cn.generation, 0)
    self.assertEqual(cn.dump(), 'Gen 0:\n')

    cn.cells = [ cell.BooleanCell('Cell 1'), cell.BooleanCell('Cell 2'), cell.BooleanCell('Cell 3') ]
    self.assertEqual( [c.state for c in cn.cells], [0, 0, 0])
    cn.nextGen()
    self.assertEqual(cn.generation, 1)
    self.assertEqual( [c.state for c in cn.cells], [1, 1, 1])
 
  def testCellTriangleIntegerCells(self):
    """ Test for a SimpleCellTriangle object """
    cn = cellNet.SimpleCellTriangle([ cell.IntegerCell('Cell A', 1), 
                                      cell.IntegerCell('Cell B', 5), 
                                      cell.IntegerCell('Cell C', 7) ])
    self.assertEqual( [c.state for c in cn.cells], [1, 5, 7])
    self.assertEqual(cn.generation, 0)
    cn.nextGen()
    self.assertEqual(cn.generation, 1)
    self.assertEqual( [c.state for c in cn.cells], [12, 8, 6])
    cn.nextGen()
    self.assertEqual(cn.generation, 2)
    self.assertEqual( [c.state for c in cn.cells], [14, 18, 20])

  def testCellGrid3x3(self):
    """ Tests for a simple 3 x 3 Grid """ 
    cg = cellNet.CellGrid(3,3)
    # need to test that each cell 
    #    - is a BaseCell
    #    - has correct Identity
    #    - has correct neighbors
    # and check dump state is unchanged after tick()
    
    for row in range(cg.rows):
      for col in range(cg.cols):
        c = cg.cells[row][col]
        self.assertTrue( isinstance(c, cell.BaseCell))
        self.assertEqual(str(c.identity), '(%i, %i)' % (row, col))

        if row==0 and col==0:
          self.assertEqual( c.neighbors, [ cg.cells[0][1], cg.cells[1][1], cg.cells[1][0] ] )
        
        if row==1 and col==1:
          self.assertEqual( c.neighbors, [ cg.cells[0][1], cg.cells[0][2], cg.cells[1][2],
                                           cg.cells[2][2], cg.cells[2][1], cg.cells[2][0], 
                                           cg.cells[1][0], cg.cells[0][0] ] )
        # ... Need more of these ... 
        
# Check dump values 
    before = cg.dump()
    self.assertEqual(before, "Gen 0:\n(0, 0)<0> A: None D: None N: ['(0, 1)<0>', '(1, 1)<0>', '(1, 0)<0>']\n(0, 1)<0> A: None D: None N: ['(0, 2)<0>', '(1, 2)<0>', '(1, 1)<0>', '(1, 0)<0>', '(0, 0)<0>']\n(0, 2)<0> A: None D: None N: ['(1, 2)<0>', '(1, 1)<0>', '(0, 1)<0>']\n(1, 0)<0> A: None D: None N: ['(0, 0)<0>', '(0, 1)<0>', '(1, 1)<0>', '(2, 1)<0>', '(2, 0)<0>']\n(1, 1)<0> A: None D: None N: ['(0, 1)<0>', '(0, 2)<0>', '(1, 2)<0>', '(2, 2)<0>', '(2, 1)<0>', '(2, 0)<0>', '(1, 0)<0>', '(0, 0)<0>']\n(1, 2)<0> A: None D: None N: ['(0, 2)<0>', '(2, 2)<0>', '(2, 1)<0>', '(1, 1)<0>', '(0, 1)<0>']\n(2, 0)<0> A: None D: None N: ['(1, 0)<0>', '(1, 1)<0>', '(2, 1)<0>']\n(2, 1)<0> A: None D: None N: ['(1, 1)<0>', '(1, 2)<0>', '(2, 2)<0>', '(2, 0)<0>', '(1, 0)<0>']\n(2, 2)<0> A: None D: None N: ['(1, 2)<0>', '(2, 1)<0>', '(1, 1)<0>']\n") 
    cg.nextGen()
    after = cg.dump()
    self.assertEqual(after, "Gen 1:\n(0, 0)<1> A: (0, 0)<0> D: None N: ['(0, 1)<1>', '(1, 1)<1>', '(1, 0)<1>']\n(0, 1)<1> A: (0, 1)<0> D: None N: ['(0, 2)<1>', '(1, 2)<1>', '(1, 1)<1>', '(1, 0)<1>', '(0, 0)<1>']\n(0, 2)<1> A: (0, 2)<0> D: None N: ['(1, 2)<1>', '(1, 1)<1>', '(0, 1)<1>']\n(1, 0)<1> A: (1, 0)<0> D: None N: ['(0, 0)<1>', '(0, 1)<1>', '(1, 1)<1>', '(2, 1)<1>', '(2, 0)<1>']\n(1, 1)<1> A: (1, 1)<0> D: None N: ['(0, 1)<1>', '(0, 2)<1>', '(1, 2)<1>', '(2, 2)<1>', '(2, 1)<1>', '(2, 0)<1>', '(1, 0)<1>', '(0, 0)<1>']\n(1, 2)<1> A: (1, 2)<0> D: None N: ['(0, 2)<1>', '(2, 2)<1>', '(2, 1)<1>', '(1, 1)<1>', '(0, 1)<1>']\n(2, 0)<1> A: (2, 0)<0> D: None N: ['(1, 0)<1>', '(1, 1)<1>', '(2, 1)<1>']\n(2, 1)<1> A: (2, 1)<0> D: None N: ['(1, 1)<1>', '(1, 2)<1>', '(2, 2)<1>', '(2, 0)<1>', '(1, 0)<1>']\n(2, 2)<1> A: (2, 2)<0> D: None N: ['(1, 2)<1>', '(2, 1)<1>', '(1, 1)<1>']\n")

  def testCellBooleanGrid3x3(self):
    bcg = cellNet.BooleanCellGrid(3,3)
    (bcg.cells[1][0].state, bcg.cells[1][1].state, bcg.cells[1][2].state) = (1,1,1)
    self.assertEqual(str(bcg), "\n['0', '0', '0']\n['1', '1', '1']\n['0', '0', '0']\n")
    bcg.nextGen()
    self.assertEqual(str(bcg), "\n['True', 'True', 'True']\n['False', 'False', 'False']\n['True', 'True', 'True']\n")


# ---------------------------------------------------------------------
# Tests for CellNet Viewer-Controller objects
# ---------------------------------------------------------------------
  def testCellNet_VC(self):
    """ General Tests """
    cn = cellNet.SimpleCellTriangle([ cell.IntegerCell('Cell A', 1), 
                                      cell.IntegerCell('Cell B', 5), 
                                      cell.IntegerCell('Cell C', 7) ])
    cnvc = cellNet.CellNet_VC(cn)
    self.assertEqual(str(cnvc), '\n0: 1\n1: 5\n2: 7')

    # Use doTick() method to one tick(), independent of ticker.Tickable interface
    cnvc.doTick()
    cnvc.refreshOnTock()
    self.assertEqual(str(cnvc), '\n0: 12\n1: 8\n2: 6')
    cnvc.doTick()
    cnvc.refreshOnTock()
    self.assertEqual(str(cnvc), '\n0: 14\n1: 18\n2: 20')
        
    # Use ticker.Tickable interface to do one tick()
    import time
    cnvc.play()
    time.sleep(cnvc.period + 0.5)      # 0.5 second more than tick = 2 ticks 
    cnvc.pause()
    self.assertEqual(str(cnvc), '\n0: 66\n1: 70\n2: 72')

    # Use mutate() and update() to change specific cells 
    cnvc.mutateCell(0)
    self.assertEqual(str(cnvc), '\n0: 142\n1: 70\n2: 72')
    cnvc.updateCell(1, 10)
    self.assertEqual(str(cnvc), '\n0: 142\n1: 10\n2: 72')

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
    vc = cellNet.CellGrid_VC(bcg)
    self.assertEqual(str(vc), '------------\n    0  1  2 \n 0  -  *  - \n 1  -  *  - \n 2  -  *  - \n------------')
    
  # test that underlying cell can be manipulated via the controller and the change reflected in the associated cellNet
    vc.mutateCell(1, 0)
    vc.updateCell(1, 2)
    self.assertEqual( str(vc), CROSS_PATTERN)
  
  # perform two ticks without separate thread - should still be the same as before
    vc.doTick()
    vc.refreshOnTock()
    vc.doTick()
    vc.refreshOnTock()
    self.assertEqual( str(vc), CROSS_PATTERN)
   
    # Use ticker.Tickable interface to do one tick()
    import time
    vc.play()
    time.sleep(vc.period + 0.5)      # 0.5 second more than tick = 2 ticks 
    vc.pause()
    self.assertEqual( str(vc), CROSS_PATTERN)

  '''
  def checkViewerCellsMatchModelCells(self, viewer, model):
    """ test that the cells pointed to by all the viewers match the correct cells from the underlying grid """
    for i in range( len(model.cells) ):
      for j in range ( len( model.cells[i] )):
        self.assertTrue( viewer.viewers[i][j].cell is model.cells[i][j], 'Cell (%i, %i)' % (i,j))  

  '''

  
if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCellNets)
  unittest.TextTestRunner(verbosity=3).run(suite)
