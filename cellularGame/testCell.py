import unittest, Cell


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
    """ test constructor """
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
    c1 = Cell.BooleanCell("Cell 1")         # default False
    c2 = Cell.BooleanCell('Cell 2', True)
    
    self.assertFalse(c1.state)
    self.assertEqual(c2.dump(), 'State: 1')

    c1.mutate()                    # in this case mutate() should perform a toggle on the boolean
    self.assertTrue(c1.state)

    c2.update()                    # update also means toggle for BooleanCells 
    self.assertFalse(c2.state)



class TestCellNets(unittest.TestCase):

# ---------------------------------------------------------------------
# Tests for CellNet 
# ---------------------------------------------------------------------


  def testCellNet(self):
    cn = Cell.CellNet()
    self.assertEqual(cn.cells, [])
    self.assertEqual(cn.generation, 0)
    self.assertEqual(cn.dump(), 'Gen 0:\n')

    cn.cells = [ Cell.BooleanCell('Cell 1'), Cell.BooleanCell('Cell 2'), Cell.BooleanCell('Cell 3') ]
    self.assertEqual( [cell.state for cell in cn.cells], [0, 0, 0])
    cn.tick()
    self.assertEqual(cn.generation, 1)
    self.assertEqual( [cell.state for cell in cn.cells], [1, 1, 1])
 
  def testCellTriangleIntegerCells(self):
    
    cn = Cell.simpleCellTriangle([ Cell.IntegerCell('Cell A', 1), 
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
    cg = Cell.CellGrid(3,3)
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

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCells)
  unittest.TextTestRunner(verbosity=3).run(suite)
