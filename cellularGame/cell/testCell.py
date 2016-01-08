import unittest, Cell
from Cell import Cell_VC


class TestCells(unittest.TestCase):

# ---------------------------------------------------------------------
# Tests for BaseCell 
# ---------------------------------------------------------------------
  def setUp(self):
    self.cell1 = Cell.BaseCell('Cell 1')
    self.cell2 = Cell.BaseCell('Cell 2')

  def testBaseCellCreation(self):
    """ test constructor """  
    self.assertEqual(str(self.cell1), 'Cell 1<0> A: None D: None N: None ')
    self.assertEqual(self.cell1.generation, 0)
    self.assertEqual(self.cell1.neighbors, [])
    self.assertEqual(self.cell1.ancestor, None)
    self.assertEqual(self.cell1.descendant, None)
    self.assertEqual(str(self.cell2), 'Cell 2<0> A: None D: None N: None ')

  def testBaseCellAddNeighbors(self):
    """ test adding neighbors """  
    cell3 = Cell.BaseCell('Cell 3')
    [ cell3.addNeighbor(c) for c in (self.cell1, self.cell2) ]
    self.assertEqual(str(cell3), "Cell 3<0> A: None D: None N: ['Cell 1<0>', 'Cell 2<0>'] ")

  def testBaseCellCloneUpdate(self):
    cell4 = self.cell1.clone()
    cell5 = self.cell2.clone('Cell 5')

    self.assertFalse(self.cell1 is cell4)
    self.assertNotEqual(self.cell1, cell4)
    self.assertEqual(str(cell4), 'Cell 1<1> A: Cell 1<0> D: None N: None ')
    self.assertTrue( cell4.ancestor is self.cell1 )
    self.assertTrue( self.cell1.descendant is cell4 )
    self.assertEqual( cell4.generation, 1 )

    self.assertFalse(self.cell2 is cell5)
    self.assertNotEqual(self.cell2, cell5)
    self.assertEqual(str(self.cell2), 'Cell 2<0> A: None D: Cell 5<1> N: None ')
    self.assertEqual(str(cell5), 'Cell 5<1> A: Cell 2<0> D: None N: None ')
    self.assertTrue( cell5.ancestor is self.cell2 )
    self.assertTrue( self.cell2.descendant is cell5 )
    self.assertEqual( cell5.generation, 1 )
  
    # test nextGen()
    cell6 = cell5.nextGen('Cell 6')
    self.assertTrue( cell6.ancestor is cell5 )
    self.assertTrue( cell5.descendant is cell6 )
    self.assertEqual( cell6.generation, 2 )
    self.assertEqual(str(cell6), 'Cell 6<2> A: Cell 5<1> D: None N: None ')
    
    
# ---------------------------------------------------------------------
# Tests for IntegerCell 
# ---------------------------------------------------------------------
  def testIntegerCell(self):
    """ tests specific to IntegerCell """
    c1 = Cell.IntegerCell("Cell 1")         # default state
    c2 = Cell.IntegerCell('Cell 2', 1)
    c3 = Cell.IntegerCell('Cell 3', 5)
    c4 = Cell.IntegerCell('Cell 4', 10)
    
    self.assertEqual(c1.dump(), 'State: 0')
    self.assertEqual(c2.dump(), 'State: 1')

    [ c4.addNeighbor(c) for c in (c1,c2,c3) ]
    
    c4.mutate()                          # new state depends on neighbor state
    self.assertEqual(c4.state, 6)

    c4.update(state=100)                 # directly change state 
    self.assertEqual(c4.state, 100)
    
    c1.state = 10
    c5 = c4.nextGen('Cell 5')            # nextGen includes a mutate()
    self.assertEqual(c5.state, 16)
  
  # test modify() method
    c5.modify()                         # modify with no args equals return to default state
    self.assertEqual(c5.state, 0)
    
    c5.state = 100
    c5.modify(False)                    # modify with arg1=False equals same as no args
    self.assertEqual(c5.state, 0)
    
    c5.state = 100
    c5.modify(True)                     # modify with arg1=True equals same as mutate()
    self.assertEqual(c5.state, 16)

    c5.state = 100
    c5.modify(True, state=99)          # modify with arg1=True and kwargs -> ignore the kwargs
    self.assertEqual(c5.state, 16)

    c5.state = 100
    c5.modify(False, state=99)          # modify with arg1=False equals same as update()
    self.assertEqual(c5.state, 99)
  
# ---------------------------------------------------------------------
# Tests for BooleanCell 
# ---------------------------------------------------------------------
  def testBooleanCell(self):
    """ tests specific to BooleanCell """
    c1 = Cell.BooleanCell("Cell 1")         # default False
    c2 = Cell.BooleanCell('Cell 2', True)
    
    self.assertFalse(c1.state)
    self.assertEqual(c2.dump(), 'State: 1')

    c1.mutate()                    # in this case mutate() should perform a toggle on the boolean
    self.assertTrue(c1.state)

    c2.update()                    # update also means toggle for BooleanCells 
    self.assertFalse(c2.state)


# ---------------------------------------------------------------------
# Tests for CellViewerController 
# ---------------------------------------------------------------------
  def testCell_VC(self):
    """ general tests for Cell Viewer/Controllers """

# create a BaseCell and a Viewer/Controller
    c1 = Cell.BaseCell('Cell 1')
    vc = Cell_VC(c1)
    
# check association and initial value of the viewer/controller string
    self.assertTrue( vc.cell is c1)
    self.assertEqual( str(vc), 'Cell 1')

# test setCell 
    c2 = Cell.BaseCell('Cell 2')
    vc.setCell(c2)
    self.assertTrue( vc.cell is c2)
    self.assertEqual( str(vc), 'Cell 2')

# ---------------------------------------------------------------------
# Tests for IntegerCellViewerController 
# ---------------------------------------------------------------------
  def testIntegerCell_VC(self):
    """ tests specific to Integer Cell VC """

# create an IntegerCell and a Viewer/Controller
    c1 = Cell.IntegerCell('Cell1')
    vc = Cell.IntegerCell_VC(c1)
    
# check association and initial value of the viewer/controller string
    self.assertEqual( str(vc), '0')

# set up neighbors of c1
    c2 = Cell.IntegerCell('Cell2', state=5)
    c3 = Cell.IntegerCell('Cell3', state=10)
    c1.addNeighbor(c2)
    c1.addNeighbor(c3)
    
# two types of modification. Each should update the py string  
    vc.mutateCell()        # mutate according to Cells internal rules
    self.assertEqual( str(vc), '15')

    vc.updateCell(state=50)             
    self.assertEqual( str(vc), '50')

# ---------------------------------------------------------------------
# Tests for BooleanCellViewer 
# ---------------------------------------------------------------------
  def testBooleanCell_VC(self):
    """ tests specific to Boolean Cell VC """

# create a boolean cell and a viewer/controller
    c1 = Cell.BooleanCell('Cell1')
    vc = Cell.BooleanCell_VC(c1)

# check association and initial value of the viewer/controller string
    self.assertEqual( str(vc),'-')

# two types of modification. Each should update the viewer/controller string  
    vc.mutateCell()     
    self.assertEqual( str(vc), '*')

    vc.updateCell()             
    self.assertEqual( str(vc), '-')



if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCells)
  unittest.TextTestRunner(verbosity=3).run(suite)
