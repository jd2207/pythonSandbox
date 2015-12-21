import unittest, Cell
import CellViewerController

class TestCellsMVC(unittest.TestCase):

# ---------------------------------------------------------------------
# Tests for IntegerCellViewerController 
# ---------------------------------------------------------------------
  def testIntegerCellViewerController(self):
    """ Tests pubsub effects using a IntegerCellViewerController object """

# create a cell and a viewer
    c1 = Cell.IntegerCell('Cell1')
    v = CellViewerController.IntegerCellViewerController(c1)
    
# check association and initial value of the viewer string
    self.assertTrue( v.cell is c1)
    self.assertEqual( v.strValue, '0')

# check pointing to a different cell 
    c2 = Cell.IntegerCell('Cell2', state=99)
    v.setCell(c2)
    self.assertTrue( v.cell is c2)
    self.assertEqual( v.strValue, '99')

# two types of modification. Each should update the viewer string  
    v.modify()               # mutate according to Cells internal rules
    self.assertEqual( v.strValue, '0')

    v.setCell(c1)             
    c1.modify(state=50)       # mutate according to **kwargs
    self.assertEqual( v.strValue, '50')


# ---------------------------------------------------------------------
# Tests for BooleanCellViewer 
# ---------------------------------------------------------------------
  def testBooleanCellViewerController(self):
    """ Tests pubsub effects using a CellViewerController object """

# create a boolean cell and a viewer
    c1 = Cell.BooleanCell('Cell1')
    v = CellViewerController.BooleanCellViewerController(c1)
    self.assertEqual( v.strValue,'-')

# two type of modification; each should update the viewer string  
    v.modify()
    self.assertEqual( v.strValue,'*')

    v.modify(state=False)
    self.assertEqual( v.strValue,'-')
    

# ---------------------------------------------------------------------
# Tests for BooleanCellGridViewerController 
# ---------------------------------------------------------------------

  def testBooleanCellGridViewerControllerBasic(self):
    """ Tests pubsub effects on a simple BooleanCellGrid object """

  # create the grid, set up the cells then link to the viewer/controller
    bcg = Cell.BooleanCellGrid(3,3)
    (bcg.cells[0][1].state, bcg.cells[1][1].state, bcg.cells[2][1].state) = (1,1,1)
    gridViewerController = CellViewerController.BooleanGridViewerController(bcg)

  # test viewers cells align with the models cells
    self.checkViewerCellsMatchModelCells(gridViewerController, bcg)

  # test the value of the cellViewerController Class
    self.getcellViewerControllerClass = getattr(__import__('CellViewerController'), 'CellViewerController')

  # test that underlying cell can be manipulated via the controller and the change reflected in the associated viewer
    gridViewerController.modifyCell(1, 1)
    self.assertFalse( gridViewerController.viewers[1][1].cell.state )  

    gridViewerController.modifyCell(1, 1, state=True)
    self.assertTrue( gridViewerController.viewers[1][1].cell.state )  

  # test, after a tick() that the cells pointed to by all the viewers are still aligned with the model 
    gridViewerController.play()
    self.checkViewerCellsMatchModelCells(gridViewerController, bcg)


  def testBooleanCellGridViewerStr(self):
  
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
  
    # setup a 'cross' pattern on a 3x3 grid, should be reflected in the viewer
    bcg = Cell.BooleanCellGrid(3,3)
    v = CellViewerController.BooleanGridViewerController(bcg)
    v.modifyCell(0,1); v.modifyCell(1,0); v.modifyCell(1,1); v.modifyCell(1,2); v.modifyCell(2,1);
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
