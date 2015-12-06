import unittest, Cell

class TestCell(unittest.TestCase):

# ---------------------------------------------------------------------
# Tests for AbstractCell 
# ---------------------------------------------------------------------

  DEFAULT_CELL = 'defaultCell'
  DEFAULT_CELL_WITH_NEIGHBORS = 'neighboredCell'

  DEFAULT_BOOLEAN_CELL = 'defaultBooleanCell'
  DEFAULT_BOOLEAN_CELL_WITH_NEIGHBORS = 'BooleanCell'
  BOOLEAN_CELL_NEIGHBOR1 = 'neighbor 1'
  BOOLEAN_CELL_NEIGHBOR2 = 'neighbor 2'
  BOOLEAN_CELL_NEIGHBOR3 = 'neighbor 3'
  
  def setUp(self):
    self.defaultAbstractCell = Cell.AbstractCell(TestCell.DEFAULT_CELL)
    self.defaultNeighboredCell = Cell.AbstractCell(TestCell.DEFAULT_CELL_WITH_NEIGHBORS, [1,2,3] )
    
    self.defaultBooleanCell = Cell.BooleanCell(TestCell.DEFAULT_BOOLEAN_CELL)
    self.neighborCell1 = Cell.BooleanCell(TestCell.BOOLEAN_CELL_NEIGHBOR1)
    self.neighborCell2 = Cell.BooleanCell(TestCell.BOOLEAN_CELL_NEIGHBOR1)
    self.neighborCell3 = Cell.BooleanCell(TestCell.BOOLEAN_CELL_NEIGHBOR1)
    self.BooleanCell = Cell.BooleanCell( TestCell.DEFAULT_BOOLEAN_CELL_WITH_NEIGHBORS, 
                          [ self.neighborCell1, self.neighborCell2, self.neighborCell3] )
  
  def testAbstractCreateDefault(self):
    """ default instantiation - no list of neighbors """  
    self.assertEqual(str(self.defaultAbstractCell), TestCell.DEFAULT_CELL)
  
  def testAbstractNeighbors(self):  
    """ default instantiation - with a list of neighbors """  
    self.assertEqual(str(self.defaultNeighboredCell), 
                     TestCell.DEFAULT_CELL_WITH_NEIGHBORS + ' with neighbors: 1 2 3')

  def testAbstractNextGen(self):
    """ default make a copy """  
    cnext = self.defaultAbstractCell.nextGen()
    self.assertFalse(self.defaultAbstractCell is cnext)
    self.assertNotEqual(self.defaultAbstractCell, cnext)
  
    cnext = self.defaultNeighboredCell.nextGen()
    self.assertFalse(self.defaultNeighboredCell is cnext)
    self.assertNotEqual(self.defaultNeighboredCell, cnext)

  
# ---------------------------------------------------------------------
#  Tests for BooleanCell 
# ---------------------------------------------------------------------

  def testBooleanCellDefaultState(self):
    """ instantiate with default state """  
    self.assertEqual(str(self.defaultBooleanCell), TestCell.DEFAULT_BOOLEAN_CELL + ' State: 0')
    self.assertFalse(self.defaultBooleanCell.state)

  def testBooleanCellToggle(self):
    """ Boolean cell can be toggled"""  
    self.defaultBooleanCell.toggle()
    self.assertTrue(self.defaultBooleanCell.state)
    self.assertEqual(str(self.defaultBooleanCell), TestCell.DEFAULT_BOOLEAN_CELL + ' State: 1')
    self.defaultBooleanCell.toggle()
    self.assertFalse(self.defaultBooleanCell.state)
    self.assertEqual(str(self.defaultBooleanCell), TestCell.DEFAULT_BOOLEAN_CELL + ' State: 0')

  def testBooleanCellNextGen(self):
    """ Boolean cell - make a descendant chain  """  
    for i in range(5):
      cnext = self.defaultBooleanCell.nextGen()
      self.assertTrue(isinstance(cnext, Cell.BooleanCell) and cnext.state != self.defaultBooleanCell.state)
      self.defaultBooleanCell = cnext
      

# ---------------------------------------------------------------------
# Tests for CellGrid 
# ---------------------------------------------------------------------
  '''
  EMPTY_GRID_STRING = \
    '------------------' + '\n'\
  + '    0  1  2  3  4 ' + '\n'\
  + ' 0  -  -  -  -  - ' + '\n'\
  + ' 1  -  -  -  -  - ' + '\n'\
  + ' 2  -  -  -  -  - ' + '\n'\
  + ' 3  -  -  -  -  - ' + '\n'\
  + ' 4  -  -  -  -  - ' + '\n'\
  + '------------------'

  DIAG_GRID_STRING = \
    '------------------' + '\n'\
  + '    0  1  2  3  4 ' + '\n'\
  + ' 0  *  -  -  -  - ' + '\n'\
  + ' 1  -  *  -  -  - ' + '\n'\
  + ' 2  -  -  *  -  - ' + '\n'\
  + ' 3  -  -  -  *  - ' + '\n'\
  + ' 4  -  -  -  -  * ' + '\n'\
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
    
  INV_DIAG_GRID_STRING = \
    '------------------' + '\n'\
  + '    0  1  2  3  4 ' + '\n'\
  + ' 0  -  *  *  *  * ' + '\n'\
  + ' 1  *  -  *  *  * ' + '\n'\
  + ' 2  *  *  -  *  * ' + '\n'\
  + ' 3  *  *  *  -  * ' + '\n'\
  + ' 4  *  *  *  *  - ' + '\n'\
  + '------------------'


  def testCellGrid(self):
    """ Create empty CellGrid """  
    g = Cell.CellGrid(5,5)
    self.assertEqual(str(g), TestCell.EMPTY_GRID_STRING)
        
  def testCellGridCreation(self):
    """ Create empty CellGrid and check str() """  
    g = Cell.CellGrid(5,5)
    self.assertEqual(str(g), TestCell.EMPTY_GRID_STRING)

  def testCellGridNextState(self):
    """ Check nextState() transitions """  
    g = Cell.CellGrid(5,5)
    self.assertEqual(str(g), TestCell.EMPTY_GRID_STRING)
    
    g.nextState()
    self.assertEqual(str(g), TestCell.FULL_GRID_STRING)

    for i in range(5):
      g[i][i] = Cell.BooleanCell( (i,i) )
    
    self.assertEqual(str(g), TestCell.INV_DIAG_GRID_STRING)
    g.nextState()
    self.assertEqual(str(g), TestCell.DIAG_GRID_STRING)

  def testCellGridNeighbors(self):
    """ Counting cell neighbors """  
    g = Cell.CellGrid(3,3)
    self.assertEqual( g.neighbors(0,0), [ (0,1), (1,1), (1,0) ] )
    self.assertEqual( g.neighbors(1,1), [ (0,1), (0,2), (1,2), (2,2), (2,1), (2,0), (1,0), (0,0) ] )
  '''

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCell)
  unittest.TextTestRunner(verbosity=3).run(suite)
