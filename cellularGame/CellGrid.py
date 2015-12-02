import sys, Cell, random, time

class CellGrid(list):     # list of rows
    def __init__(self, rows, cols):     
        
        self.rows = rows
        self.cols = cols

        for i in range(self.rows):
          row = []
          for j in range(self.cols):
            row.append(self.createCell( (i,j) ))
          self.append(row)

    def createCell(self):     # overridden by descendants
      pass

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
    
      for cell in (nw, n, ne, e, se, s, sw, w):
        if cell:
          neighbors.append(cell)
          
      return neighbors  # list of tuples
    
    def dump(self):
      cols = self.cols
      print '---' * (cols + 1)
      print '   ' +  ' %i ' * cols % tuple(range(cols))
      
      i = 0
      for row in self:
        j = 0
        sys.stdout.write (' %i ' % i)
        for col in row:
          sys.stdout.write(' * ' if self[i][j].state else ' - ')
          j += 1
        print
        i += 1
        
      print '---' * (cols + 1)


class BooleanGrid(CellGrid):  
  def createCell(self, identity):     
    return Cell.BooleanCell(identity, self)



class RandomBooleanGrid(CellGrid):
  def createCell(self, identity):     
    return Cell.RandomBooleanCell(identity, self)



class GameOfLifeGrid(CellGrid):
  def createCell(self, identity):     
    return Cell.GameOfLifeCell(identity, self)



if __name__ == '__main__':

  '''
# Tests for Boolean Grid    
  print "Empty 10 x 10 grid:"
  g1 = BooleanGrid(cols=10, rows=10)
  g1.dump()
  
  print "Diagonal set"      # tests getCell() method
  for i in range(size):
    g1[i][i] = Cell.BooleanCell( (i,i), state=True)
  g1.dump()

  for i in range(10):
    print "Next state"    
    g1.nextState()
    g1.dump()
  '''
  
  '''
  # Tests for Random Boolean Grid    
  print "Empty 10 x 5 grid:"
  g1 = RandomBooleanGrid(10, 5)
  g1.dump()
  
  for i in range(10):
    print "Next state ..."    
    g1.nextState()
    g1.dump()
  
    # choose a cell at random
    row = random.randint(0, g1.rows - 1)
    col = random.randint(0, g1.cols - 1)
    print 'random cell chosen is (%i,%i)' % (row, col)
    n = g1.neighbors(row, col)
    print 'Neighbors of %i, %i are: ' % (row, col), n 
    # sum the neighbors
    s = 0
    for i in n:
      m = g1[ i[0] ] [ i[1] ].state
      s += m
    print 'Sum of neighbors is ', s
  '''
 
  print "Empty 7 x 8 grid:"
  g1 = GameOfLifeGrid(7, 8)
  g1.dump()
  time.sleep(1)
  
  g1[3][5].state = True
  g1[4][5].state = True
  g1[5][5].state = True
  g1.dump()
  time.sleep(1)

  for i in range(10):
    g1.nextState()
    g1.dump()
    time.sleep(1)
