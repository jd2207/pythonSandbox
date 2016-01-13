import cell, cellNet


class GameOfLifeCell(cell.BooleanCell):
  """ Behaves as per Conway's Game of Life """
  
  def mutate(self, state=None):
    """ update cell state according to conway's rules: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules """
    s = sum ( n.state for n in self.neighbors )   # number of alive neighbors
    if self.state:                          # if alive
      if s > 3 or s < 2:                    #    and 2 or 3 neighbors
        self.state = False                  #      kill the alive cell as by over population
    else:                                   # if dead
      if s == 3:                            #    and there are exactly 3 neighbors
        self.state = True                   #      cell comes alive, as by reproduction


class GameOfLifeGrid(cellNet.BooleanCellGrid):
  def makeCell(self, rowColTupleIdentity ):
    return GameOfLifeCell( rowColTupleIdentity )
      

if __name__ == '__main__':

  print "For tests use module 'testGameOfLife'"
