import unittest, Cell
import CellViewerController

class TestCellsMVC(unittest.TestCase):


# ---------------------------------------------------------------------
# Tests for CellViewerController 
# ---------------------------------------------------------------------
  def testCellViewerController(self):

# create a BaseCell and a Viewer/Controller
    c1 = Cell.BaseCell('Cell 1')
    v = CellViewerController.CellViewerController(c1)
    
# check association and initial value of the py string
    self.assertTrue( v.cell is c1)
    self.assertEqual( str(v), 'Cell 1')

# test setCell 
    c2 = Cell.BaseCell('Cell 2')
    v.setCell(c2)
    self.assertTrue( v.cell is c2)
    self.assertEqual( str(v), 'Cell 2')

# ---------------------------------------------------------------------
# Tests for IntegerCellViewerController 
# ---------------------------------------------------------------------
  def testIntegerCellViewerController(self):

# create a cell and a py
    c1 = Cell.IntegerCell('Cell1')
    v = CellViewerController.IntegerCellViewerController(c1)
    
# check association and initial value of the py string
    self.assertEqual( str(v), '0')

# set up neighbors of c1
    c2 = Cell.IntegerCell('Cell2', state=5)
    c3 = Cell.IntegerCell('Cell3', state=10)
    c1.addNeighbor(c2)
    c1.addNeighbor(c3)
    
# two types of modification. Each should update the py string  
    v.mutateCell()        # mutate according to Cells internal rules
    self.assertEqual( str(v), '15')

    v.updateCell(state=50)             
    self.assertEqual( str(v), '50')

# ---------------------------------------------------------------------
# Tests for BooleanCellViewer 
# ---------------------------------------------------------------------
  def testBooleanCellViewerController(self):
    """ Tests pubsub effects using a CellViewerController object """

# create a boolean cell and a py
    c1 = Cell.BooleanCell('Cell1')
    v = CellViewerController.BooleanCellViewerController(c1)

# check association and initial value of the py string
    self.assertEqual( str(v),'-')

# two types of modification. Each should update the py string  
    v.mutateCell()     
    self.assertEqual( str(v), '*')

    v.updateCell()             
    self.assertEqual( str(v), '-')


# ---------------------------------------------------------------------
# Tests for BooleanCellGridViewerController 
# ---------------------------------------------------------------------

  def testBooleanCellGridViewerControllerBasic(self):

  # create the grid, set up the cells then link to the py/controller
    bcg = Cell.BooleanCellGrid(3,3)
    (bcg.cells[0][1].state, bcg.cells[1][1].state, bcg.cells[2][1].state) = (1,1,1)
    vc = CellViewerController.BooleanGridViewerController(bcg)

  # test viewers cells align with the models cells
    self.checkViewerCellsMatchModelCells(vc, bcg)
    print 'Initial state \n', str(vc)
    
  # test that underlying cell can be manipulated via the controller and the change reflected in the associated py
    vc.mutateCell(1, 0)
    vc.updateCell(1, 2)
  
    self.assertEquals( str(vc.viewers[1][0]), '*')  
    self.assertEquals( str(vc.viewers[1][2]), '*')  

  # test, after a tick() that the cells pointed to by all the viewers are still aligned with the model 
    vc.play()
    self.checkViewerCellsMatchModelCells(vc, bcg)



  def testBooleanCellGridViewerControllerSpecific(self):
  
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
    bcg = Cell.BooleanCellGrid(5, 5)
    v = CellViewerController.BooleanGridViewerController(bcg)
    self.assertEqual( str(v), EMPTY_GRID_STRING)
    v.play()
    self.assertEqual( str(v), FULL_GRID_STRING)
  
    # setup a 'cross' pattern on a 3x3 grid, should be reflected in the py
    bcg = Cell.BooleanCellGrid(3,3)
    v = CellViewerController.BooleanGridViewerController(bcg)
    v.mutateCell(0,1); v.mutateCell(1,0); v.mutateCell(1,1); v.mutateCell(1,2); v.mutateCell(2,1);
    self.assertEqual( str(v), CROSS_PATTERN)
    # tick it twice should get back same pattern
    v.play(2)
    self.assertEqual( str(v), CROSS_PATTERN)

    
  def checkViewerCellsMatchModelCells(self, viewer, model):
    """ test that the cells pointed to by all the viewers match the correct cells from the underlying grid """
    for i in range( len(model.cells) ):
      for j in range ( len( model.cells[i] )):
        self.assertTrue( viewer.viewers[i][j].cell is model.cells[i][j], 'Cell (%i, %i)' % (i,j))  
  

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCellsMVC)
  unittest.TextTestRunner(verbosity=3).run(suite)
