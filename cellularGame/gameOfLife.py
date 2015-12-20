import Cell, CellViewerController


class GameOfLifeCell(Cell.BooleanCell):
  """ Behaves as per Conway's Game of Life """
  
  def modify(self, state=None):
    """ update cell state according to conway's rules: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules """

    if state:
      self.state = state
    else:
      s = sum ( n.state for n in self.neighbors )   # number of alive neighbors
      if self.state:                          # if alive
        if s > 3 or s < 2:                    #    and 2 or 3 neighbors
          self.state = False                  #      kill the alive cell as by over population
      else:                                   # if dead
        if s == 3:                            #    and there are exactly 3 neighbors
          self.state = True                   #      cell comes alive, as by reproduction



class GameOfLifeGrid(Cell.BooleanCellGrid):
  def makeCell(self, rowColTupleIdentity ):
    return GameOfLifeCell( rowColTupleIdentity )
      


if __name__ == '__main__':

  # Glider sequence 
  g = GameOfLifeGrid(10, 10)
  v = CellViewerController.BooleanGridViewerController(g)

  print 'An initial glider:'
  # Initial glider
  v.modifyCell(0,1,state=1)
  v.modifyCell(1,2,state=1)
  v.modifyCell(2,0,state=1)
  v.modifyCell(2,1,state=1)
  v.modifyCell(2,2,state=1)
  print v
  
  print 'Glider after 20 generations:'
  v.tick(20)
  print v