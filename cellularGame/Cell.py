""" Defines two related abstract classes, Cell and CellGrid and simple descendants. 
    Each cell may be a member of a parent object (e.g. a CellGrid object)
    Each cell is typically given a defined identity which is a tuple: (row, column)
    Each cell class must define a method makeDescendant() which creates and returns a new object of the same class (but attributes may be different) 
"""

# -----------------------------------------------------------------------------------
class AbstractCell(object):
  """ Parent class of all Cell classes """
  
  ROW    = 0
  COLUMN = 1
  
  def __init__(self, identity=(0,0), parentGrid=None):
    self.parentGrid = parentGrid
    self.identity = identity

  def makeDescendant(self):
    """ Must be overridden by descendant classes """

  def __str__ (self):
    return 'Cell @ (%i, %i) is a child of %s.' % (self.identity[AbstractCell.ROW], self.identity[AbstractCell.COLUMN], str(self.parentGrid))


# -----------------------------------------------------------------------------------
class BooleanCell(AbstractCell):
  """ A simple cell that has a boolean state which can be toggled 

Usage:
>>> import Cell
>>> c = Cell.BooleanCell( (1,1), state=True)        # new cell set to True
>>> c.state                                        
True
>>> c.toggle()                                      # toggle it
>>> c.state
False
>>> str(c)
'Cell @ (1, 1) is a child of None. State = 0'
  """ 
  
  def __init__(self, identity, parentGrid=None, state=False):
    self.state = state
    super(BooleanCell,self).__init__(identity, parentGrid)

  def toggle(self):
    """ flips the state """
    self.state = not self.state
    
  def makeDescendant(self):
    """ creates a new BooleanCell with a toggled state """
    return BooleanCell(self.identity, parentGrid=self.parentGrid, state = not self.state)  

  def __str__(self):
    return super(BooleanCell,self).__str__() + ' State = %i' % self.state


      

# -----------------------------------------------------------------------------------
class CellGrid(list):     # list of rows
  """ parent class of all CellGrids. 
        Represents a 2D matrix of cells. 
        Implements a nextState() method such that the entire system state (state of all cells) discretely transitions to a new state, dependent on the current state   

Usage:
>>> 
   """
    
  def __init__(self, rows, cols):     
    self.rows = rows
    self.cols = cols

    for i in range(self.rows):
      row = []
      for j in range(self.cols):
        row.append(self.createCell( (i,j) ))
      self.append(row)

  def createCell(self, identity):     
    return BooleanCell(identity, self)

  def nextState(self):                            
    new = self.__class__(self.rows, self.cols)
      
    i = 0                                       # loop through existing cells, calculating the new cell values based on the old grid
    for row in self:
      for j in range(len(row)):
        new[i][j] = self[i][j].makeDescendant()
      i += 1
  
    i = 0 
    for row in self:                            #  overwrite the old cells with the new ones 
      for j in range(len(row)):
        self[i][j] = new[i][j]
      i += 1
        
  def neighbors(self, row, col):     # return a list of cells which are the neighbors of the cell at the given row, col
    neighbors = []
    nw = (row-1, col-1) if (row>0 and col>0) else None      # vars named after compass points
    n = (row-1, col) if (row>0) else None
    ne = (row-1, col+1) if (row>0 and col<self.cols-1) else None
    e = (row, col+1) if (col<self.cols-1) else None
    se = (row+1, col+1) if (row<self.rows-1 and col<self.cols-1) else None
    s = (row+1, col) if (row<self.rows-1) else None
    sw = (row+1, col-1) if (row<self.rows-1 and col>0) else None
    w = (row, col-1) if (col>0) else None
    
    for cell in (n, ne, e, se, s, sw, w, nw):   # clock-wise from "north"
      if cell:
        neighbors.append(cell)
          
    return neighbors  # list of tuples
    
  def __str__(self):
    cols = self.cols
    s =  '---' * (cols + 1) + '\n'
    s += '   ' +  (' %i ' * cols) % tuple(range(cols)) + '\n'
      
    i = 0
    for row in self:
      j = 0
      s += ' %i ' % i
      for col in row:
        s += ' * ' if self[i][j].state else ' - '
        j += 1
      s += '\n'
      i += 1
    s += '---' * (cols + 1)
    return s


      
if __name__ == '__main__':
  print "For tests use module 'testCell'"
