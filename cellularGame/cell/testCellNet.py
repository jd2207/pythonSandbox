import unittest, Cell, CellNet


class TestCellNets(unittest.TestCase):

# ---------------------------------------------------------------------
# Tests for CellNet 
# ---------------------------------------------------------------------


  def testCellNet(self):
    cn = CellNet.CellNet()
    self.assertEqual(cn.cells, [])
    self.assertEqual(cn.generation, 0)
    self.assertEqual(cn.dump(), 'Gen 0:\n')

    cn.cells = [ Cell.BooleanCell('Cell 1'), Cell.BooleanCell('Cell 2'), Cell.BooleanCell('Cell 3') ]
    self.assertEqual( [cell.state for cell in cn.cells], [0, 0, 0])
    cn.tick()
    self.assertEqual(cn.generation, 1)
    self.assertEqual( [cell.state for cell in cn.cells], [1, 1, 1])
 
  def testCellTriangleIntegerCells(self):
    cn = CellNet.simpleCellTriangle([ Cell.IntegerCell('Cell A', 1), 
                                      Cell.IntegerCell('Cell B', 5), 
                                      Cell.IntegerCell('Cell C', 7) ])
    self.assertEqual( [cell.state for cell in cn.cells], [1, 5, 7])
    self.assertEqual(cn.generation, 0)
    cn.tick()
    self.assertEqual(cn.generation, 1)
    self.assertEqual( [cell.state for cell in cn.cells], [12, 8, 6])
    cn.tick()
    self.assertEqual(cn.generation, 2)
    self.assertEqual( [cell.state for cell in cn.cells], [14, 18, 20])


# ---------------------------------------------------------------------
# Tests for CellGrid 
# ---------------------------------------------------------------------
  def testCellGridSimple3x3(self):
    cg = CellNet.CellGrid(3,3)
    # need to test that each cell 
    #    - is a BaseCell
    #    - has correct Identity
    #    - has correct neighbors
    # and check dump state is unchanged after tick()
    
    for r in range(cg.rows):
      for c in range(cg.cols):
        cell = cg.cells[r][c]
        self.assertTrue( isinstance(cell, Cell.BaseCell))
        self.assertEqual(str(cell.identity), '(%i, %i)' % (r,c))

        if r==0 and c==0:
          self.assertEqual( cell.neighbors, [ cg.cells[0][1], cg.cells[1][1], cg.cells[1][0] ] )
        
        if r==1 and c==1:
          self.assertEqual( cell.neighbors, [ cg.cells[0][1], cg.cells[0][2], cg.cells[1][2],
                                              cg.cells[2][2], cg.cells[2][1], cg.cells[2][0], 
                                              cg.cells[1][0], cg.cells[0][0] ] )
        # ... Need more of these ... 
        
# Check dump values 
    before = cg.dump()
    self.assertEqual(before, "Gen 0:\n(0, 0)<0> A: None D: None N: ['(0, 1)<0>', '(1, 1)<0>', '(1, 0)<0>'] \n(0, 1)<0> A: None D: None N: ['(0, 2)<0>', '(1, 2)<0>', '(1, 1)<0>', '(1, 0)<0>', '(0, 0)<0>'] \n(0, 2)<0> A: None D: None N: ['(1, 2)<0>', '(1, 1)<0>', '(0, 1)<0>'] \n(1, 0)<0> A: None D: None N: ['(0, 0)<0>', '(0, 1)<0>', '(1, 1)<0>', '(2, 1)<0>', '(2, 0)<0>'] \n(1, 1)<0> A: None D: None N: ['(0, 1)<0>', '(0, 2)<0>', '(1, 2)<0>', '(2, 2)<0>', '(2, 1)<0>', '(2, 0)<0>', '(1, 0)<0>', '(0, 0)<0>'] \n(1, 2)<0> A: None D: None N: ['(0, 2)<0>', '(2, 2)<0>', '(2, 1)<0>', '(1, 1)<0>', '(0, 1)<0>'] \n(2, 0)<0> A: None D: None N: ['(1, 0)<0>', '(1, 1)<0>', '(2, 1)<0>'] \n(2, 1)<0> A: None D: None N: ['(1, 1)<0>', '(1, 2)<0>', '(2, 2)<0>', '(2, 0)<0>', '(1, 0)<0>'] \n(2, 2)<0> A: None D: None N: ['(1, 2)<0>', '(2, 1)<0>', '(1, 1)<0>'] \n") 
    cg.tick()
    after = cg.dump()
    self.assertEqual(after, "Gen 1:\n(0, 0)<1> A: (0, 0)<0> D: None N: ['(0, 1)<1>', '(1, 1)<1>', '(1, 0)<1>'] \n(0, 1)<1> A: (0, 1)<0> D: None N: ['(0, 2)<1>', '(1, 2)<1>', '(1, 1)<1>', '(1, 0)<1>', '(0, 0)<1>'] \n(0, 2)<1> A: (0, 2)<0> D: None N: ['(1, 2)<1>', '(1, 1)<1>', '(0, 1)<1>'] \n(1, 0)<1> A: (1, 0)<0> D: None N: ['(0, 0)<1>', '(0, 1)<1>', '(1, 1)<1>', '(2, 1)<1>', '(2, 0)<1>'] \n(1, 1)<1> A: (1, 1)<0> D: None N: ['(0, 1)<1>', '(0, 2)<1>', '(1, 2)<1>', '(2, 2)<1>', '(2, 1)<1>', '(2, 0)<1>', '(1, 0)<1>', '(0, 0)<1>'] \n(1, 2)<1> A: (1, 2)<0> D: None N: ['(0, 2)<1>', '(2, 2)<1>', '(2, 1)<1>', '(1, 1)<1>', '(0, 1)<1>'] \n(2, 0)<1> A: (2, 0)<0> D: None N: ['(1, 0)<1>', '(1, 1)<1>', '(2, 1)<1>'] \n(2, 1)<1> A: (2, 1)<0> D: None N: ['(1, 1)<1>', '(1, 2)<1>', '(2, 2)<1>', '(2, 0)<1>', '(1, 0)<1>'] \n(2, 2)<1> A: (2, 2)<0> D: None N: ['(1, 2)<1>', '(2, 1)<1>', '(1, 1)<1>'] \n")


# ---------------------------------------------------------------------
# Tests for BooleanCellGrid_VC 
# ---------------------------------------------------------------------

  def testBooleanCellGrid_VC_General(self):

  # create the grid, set up the cells then link to the viewer/controller
    bcg = CellNet.BooleanCellGrid(3,3)
    (bcg.cells[0][1].state, bcg.cells[1][1].state, bcg.cells[2][1].state) = (1,1,1)
    vc = CellNet.BooleanGrid_VC(bcg)

  # test viewers cells align with the models cells
    self.checkViewerCellsMatchModelCells(vc, bcg)
    
  # test that underlying cell can be manipulated via the controller and the change reflected in the associated py
    vc.mutateCell(1, 0)
    vc.updateCell(1, 2)
  
    self.assertEquals( str(vc.viewers[1][0]), '*')  
    self.assertEquals( str(vc.viewers[1][2]), '*')  

  # test, after a tick() that the cells pointed to by all the viewers are still aligned with the model 
    vc.play()
    self.checkViewerCellsMatchModelCells(vc, bcg)



  def testBooleanCellGrid_VC_Specific(self):
  
    EMPTY_GRID_STRING = \
        '------------------' + '\n'\
      + '    0  1  2  3  4 ' + '\n'\
      + ' 0  -  -  -  -  - ' + '\n'\
      + ' 1  -  -  -  -  - ' + '\n'\
      + ' 2  -  -  -  -  - ' + '\n'\
      + ' 3  -  -  -  -  - ' + '\n'\
      + ' 4  -  -  -  -  - ' + '\n'\
      + '------------------'

    FULL_GRID_STRING = \
        '------------------' + '\n'\
      + '    0  1  2  3  4 ' + '\n'\
      + ' 0  *  *  *  *  * ' + '\n'\
      + ' 1  *  *  *  *  * ' + '\n'\
      + ' 2  *  *  *  *  * ' + '\n'\
      + ' 3  *  *  *  *  * ' + '\n'\
      + ' 4  *  *  *  *  * ' + '\n'\
      + '------------------'

    CROSS_PATTERN = \
        '------------' + '\n'\
      + '    0  1  2 ' + '\n'\
      + ' 0  -  *  - ' + '\n'\
      + ' 1  *  *  * ' + '\n'\
      + ' 2  -  *  - ' + '\n'\
      + '------------'
  

    # default pattern
    bcg = CellNet.BooleanCellGrid(5, 5)
    vc = CellNet.BooleanGrid_VC(bcg)
    self.assertEqual( str(vc), EMPTY_GRID_STRING)
    vc.play()
    self.assertEqual( str(vc), FULL_GRID_STRING)
  
    # setup a 'cross' pattern on a 3x3 grid, should be reflected in the py
    bcg = CellNet.BooleanCellGrid(3,3)
    vc = CellNet.BooleanGrid_VC(bcg)
    vc.mutateCell(0,1); vc.mutateCell(1,0); vc.mutateCell(1,1); vc.mutateCell(1,2); vc.mutateCell(2,1);
    self.assertEqual( str(vc), CROSS_PATTERN)
    # tick it twice should get back same pattern
    vc.play(2)
    self.assertEqual( str(vc), CROSS_PATTERN)

    
  def checkViewerCellsMatchModelCells(self, viewer, model):
    """ test that the cells pointed to by all the viewers match the correct cells from the underlying grid """
    for i in range( len(model.cells) ):
      for j in range ( len( model.cells[i] )):
        self.assertTrue( viewer.viewers[i][j].cell is model.cells[i][j], 'Cell (%i, %i)' % (i,j))  




if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCellNets)
  unittest.TextTestRunner(verbosity=3).run(suite)
