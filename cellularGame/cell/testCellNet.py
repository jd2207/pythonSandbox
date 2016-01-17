import unittest, cell, cellNet, time

class TestCellNets(unittest.TestCase):
  """ Tests for CellNet objects """

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

    cn.play()
    time.sleep(1.5)
    cn.cells[1].update()
    time.sleep(1)
    cn.pause()
    self.assertEqual( [c.state for c in cn.cells], [False, True, False])
    self.assertEqual(cn.generation, 4)
  
  def testCellTriangleIntegerCells(self):
    """ Test for a SimpleCellTriangle object """
    cn = cellNet.SimpleCellTriangle([ cell.IntegerCell('Cell A', 1), 
                                      cell.IntegerCell('Cell B', 5), 
                                      cell.IntegerCell('Cell C', 7) ])
    self.assertEqual( [c.state for c in cn.cells], [1, 5, 7])
    cn.play()
    cn.pause()
    self.assertEqual( [c.state for c in cn.cells], [12, 8, 6])

    cn.play()
    time.sleep(1.5)
    cn.cells[1].update(10)
    time.sleep(1)
    cn.pause()
    self.assertEqual( [c.state for c in cn.cells], [42, 70, 48])

  def testCellGrid3x3(self):
    """ Tests for a simple 3 x 3 Grid esp setupNeighbors() """ 
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
