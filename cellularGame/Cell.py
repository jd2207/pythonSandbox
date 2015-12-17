""" Module for Cell classes """

import copy
from pubsub import pub


class BaseCell(object):
  """ Parent class of all Cell classes 
      Has a mandatory identity object, and a list of neighbors (which must be instances of the same class)
      Child classes will override the nextGen() method and so return a modified (shallow) copy of the object
      This copy records this cell as its ancestor 
  
  Usage:
  >>> import Cell
  >>> c1 = Cell.BaseCell('Cell 1')
  >>> c2 = Cell.BaseCell('Cell 2')
  >>> c3 = Cell.BaseCell('Cell 3')
  >>> [ c3.addNeighbor(c) for c in (c1,c2) ]
  >>> print c3
  "Cell 3" is descended from None. Neighbors @: "Cell 1", "Cell 2",'
  >>> c4 = c1.nextGen('Cell 4')
  >>> print c4
  "Cell 4" is descended from "Cell 1". No neighbors.'
  >>> c5 = self.c3.nextGen('Cell 5')
  >>> print c5
  '"Cell 5" is descended from "Cell 3". Neighbors @: "Cell 1", "Cell 2",'
  
  """
  def __init__(self, identity):
    self.identity = identity
    self.neighbors = []
    self.ancestor = None
    self.descendant = None
    self.generation = 0

  def addNeighbor(self, cell):
    """ Append a new cell to the list of neighbors of this cell """
    self.neighbors.append(cell)
    
  def mutate(self):
    """ Overridden by descendants to change state/properties of the Cell according to specific rules"""
    pass
  
  def clone(self, identity=None):
    """ Make a (shallow) copy of self and (optionally) change the identity """
    new = copy.copy(self)
    new.generation += 1
    new.identity = identity if identity else self.identity
    new.ancestor = self              # record the ancestor cell of this new cell
    self.descendant = new            # record that this new cell is a child of the old one 
    return new

  def nextGen(self, identity=None):
    """ Create a cloned copy of self, and modify according to the rules of this class"""
    new = self.clone(identity)
    new.mutate()
    return new

  def identityString(self):
    return '%s<%i>' % (str(self.identity), self.generation)

  def __str__ (self):
    s = self.identityString()\
        + ' A: ' + ( self.ancestor.identityString() if self.ancestor else 'None' ) \
        + ' D: ' + ( self.descendant.identityString() if self.descendant else 'None' )
    s += ' N: '
    if len(self.neighbors) > 0: 
      s += str( [ cell.identityString() for cell in self.neighbors ] )
    else:
      s += 'None'
    return s + ' ' + self.dump()
  
  def dump(self):
    """ Overridden by descendants - used to return a string of instance attribute values"""
    return ''



class IntegerCell(BaseCell):
  """ A simple Cell that has an integer value
      It's nextGen() method returns a cell with value equal to the sum of the original cells neighbors  

Usage:
>>> import Cell
>>> c1 = Cell.IntegerCell( 'Cell 1')  # state=0
>>> c2 = Cell.IntegerCell( 'Cell 2', state=1)
>>> c3 = Cell.IntegerCell( 'Cell 3', state=2)
>>> c4 = Cell.IntegerCell( 'Cell 4', state=3)
>>> [ c4.addNeighbor(c) for c in (c1,c2,c3) ]
>>> c5 = c4.nextGen('cell 5')
>>> print c5
"Cell 5" is descended from "Cell 4". Neighbors @: "Cell 1", "Cell 2", "Cell 3", State: 3  
  """ 
  def __init__(self, identity, state=0):
    self.state = state
    super(IntegerCell,self).__init__(identity)

  def mutate(self):
    """ sets the state dependent on current state, and state of neighbors """
    self.state = sum ( cell.state for cell in self.neighbors )
  
  def dump(self):
    """ print out current state """
    return 'State: %i' % self.state



class BooleanCell(IntegerCell):
  """ A simpler version of Integer cell where state is a boolean value
      update() method toggles the state so nextGen() creates a new BooleanCell with the inverse state to the ancestor cell 
  
Usage:
>>> import Cell
>>> c1 = Cell.BooleanCell( 'Cell 1') 
>>> c2 = Cell.BooleanCell( 'Cell 2', True)
>>> print c1,c2
>>> (c3, c4) = (c1.nextGen(), c2.nextGen())
>>> print c3,c4

  """
  def mutate(self):
    """ toggle the state """
    self.toggle()

  def toggle(self):
    """ toggle the state """
    self.state = not self.state
    pub.sendMessage('Cell-Toggled')


class CellNet(object):
  """ An abstract collection of Cells 
      The collection of Cells may be ticked() - i.e. modified en-masse according to the re-generation rules of each cell
      to form a next generation  
  Usage example: See simpleCellTriangle 
  """

  def __init__(self):
    """ Usually overridden by subclasses. Otherwise, makes a new CellNet which is just a list of Cells """ 
    self.cells = getattr(self, 'cells', [])  # set self.cells to [] if not defined by the subclass __init__() 
    self.generation = 0 
    self.setupNeighbors()
     
  def makeCell(self, identity ):
    """ Make a cell for this class of CellNet - overridden by child classes""" 
    return BaseCell( identity )
  
  def setupNeighbors(self):
    """ Create the links between Cell neighbors - overridden by child classes""" 
    pass
  
  def toList(self):
    """ convert the CellNet to one dimensional list of the constituent cells -  overridden by child classes""" 
    return self.cells
    
  def fromList(self, cells):
    """ convert a list of Cells to create a new CellNet of this class -  overridden by child classes""" 
    return cells
  
  def tick(self):
    """ regenerate the Cells of the entire grid """                             
    cellList = self.toList()                        # Convert the grid to a one dimensional list
    newList = [ cell.nextGen() for cell in cellList ]   # Create a list of cells based on old one

    for cell in newList:                                # the neighbors of every new cell need to be the descendants of old neighbors
      cell.neighbors = [ n.descendant for n in cell.neighbors ]
    
    self.cells = self.fromList(newList)               # Convert it back to a grid and overwrite the original list
    self.generation += 1

  def dump(self):
    cellList = self.toList()
    return 'Gen %i:\n' % self.generation + \
           "%s\n"*len(cellList) % tuple ([ str(cell) for cell in cellList ])



class simpleCellTriangle(CellNet):
  """ a triangle of three Cells
      - which are mutual neighbors
      - which are IntegerCells 
          - state is an integer
          - next generation cell has a state which is the sum of the current neighbor cells sate 
  Usage:
  import Cell
  cn = Cell.simpleCellTriangle([ Cell.IntegerCell('Cell A', 1), 
                                 Cell.IntegerCell('Cell B', 5), 
                                 Cell.IntegerCell('Cell C', 7) ])
  [cell.state for cell in cn.cells]
  [1, 5, 7]
  cn.tick()
  [cell.state for cell in cn.cells]
  [12, 8, 6]
  
  """
  def __init__(self, listOfCells):
    self.cells = listOfCells
    super(simpleCellTriangle, self).__init__()
  
  def setupNeighbors(self):
    self.cells[0].neighbors = [ self.cells[1], self.cells[2] ]
    self.cells[1].neighbors = [ self.cells[0], self.cells[2] ]
    self.cells[2].neighbors = [ self.cells[0], self.cells[1] ]



class CellGrid(CellNet):
  """ A specific arrangement of Cells where:
      - cells are contained in a 2-D array (rows, columns)
      - the neighbors of each cell are those which are immediately adjacent (i.e the 8 cells of the compass points for non-edge, non-corner cells) 
  """  
  def __init__(self, rows=10, cols=10):     
    self.rows = rows
    self.cols = cols
    self.cells = [ [ self.makeCell( (row,col) ) for col in range(self.cols) ] for row in range(self.rows) ]
    super(CellGrid, self).__init__()
        
  def setupNeighbors(self):
    for row in range(self.rows):
      for col in range(self.cols):
        nw = (row-1, col-1) if (row>0 and col>0) else None      # vars named after compass points
        n = (row-1, col) if (row>0) else None
        ne = (row-1, col+1) if (row>0 and col<self.cols-1) else None
        e = (row, col+1) if (col<self.cols-1) else None
        se = (row+1, col+1) if (row<self.rows-1 and col<self.cols-1) else None
        s = (row+1, col) if (row<self.rows-1) else None
        sw = (row+1, col-1) if (row<self.rows-1 and col>0) else None
        w = (row, col-1) if (col>0) else None
    
        self.cells[row][col].neighbors = [ self.cells[ ncell[0] ][ ncell[1] ] for ncell in (n, ne, e, se, s, sw, w, nw) if ncell ]
  
  def fromList(self, cells):
    """ Create a 2D array of cells from a list of cells (same rows, cols as this instance) """  
    cells.reverse()
    newCells  = [ [ cells.pop() for col in range(self.cols) ] for row in range(self.rows) ]
    return newCells 

  def toList(self):
    """ returns a 1 dimensional list of the cells of the grid """
    return [ self.cells[row][col] for row in range(self.rows) for col in range(self.cols) ]



class BooleanCellGrid(CellGrid):
  """ Specialist CellGrid consisting of BooleanCells """

  def makeCell(self, rowColTupleIdentity ):
    return BooleanCell( rowColTupleIdentity )

  def __str__(self):
    cols = self.cols
    s =  '---' * (cols + 1) + '\n'
    s += '   ' +  (' %i ' * cols) % tuple(range(cols)) + '\n'
      
    i = 0
    for row in self.cells:
      j = 0
      s += ' %i ' % i
      for col in row:
        s += ' * ' if self.cells[i][j].state else ' - '
        j += 1
      s += '\n'
      i += 1
    s += '---' * (cols + 1)
    return s
  
  
  
if __name__ == '__main__':
  print "For tests use module 'testCell'"

