import unittest, Cell

class TestCell(unittest.TestCase):

# ---------------------------------------------------------------------
# Tests for AbstractCell 
# ---------------------------------------------------------------------

  def testAbstractCellDefault(self):
    """ default instantiation """  
    c = Cell.AbstractCell()
    self.assertEqual(str(c), 'Cell @ (0, 0) is a child of None.')
    
  def testAbstractCellSpecifyIdentity(self):
    """ instantiate with specific (row,col) identity """  
    c = Cell.AbstractCell(identity=(1,1))
    self.assertEqual(str(c), 'Cell @ (1, 1) is a child of None.')

# ---------------------------------------------------------------------
# Tests for BooleanCell 
# ---------------------------------------------------------------------

  def testBooleanCellDefaultState(self):
    """ instantiate with default state """  
    c = Cell.BooleanCell(identity=(1,1))
    self.assertEqual(str(c), 'Cell @ (1, 1) is a child of None. State = 0')

  def testBooleanCellToggle(self):
    """ Boolean cell can be toggled"""  
    c = Cell.BooleanCell(identity=(1,1), state=True)
    self.assertTrue(c.state)
    c.toggle()
    self.assertFalse(c.state)
    c.toggle()
    self.assertTrue(c.state)
  
  def testBooleanCellMakeDescendantChain(self):
    """ Boolean cell - make a descendant chain  """  
    c = Cell.BooleanCell(identity=(1,1), state=True)
    for i in range(5):
      cnext = c.makeDescendant()
      self.assertTrue(isinstance(cnext, Cell.BooleanCell) and cnext.state != c.state)
      c = cnext

# ---------------------------------------------------------------------
# Tests for CellGrid 
# ---------------------------------------------------------------------

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

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCell)
  unittest.TextTestRunner(verbosity=3).run(suite)
