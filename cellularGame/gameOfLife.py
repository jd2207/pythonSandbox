import Cell


# -----------------------------------------------------------------------------------
class GameOfLifeCell(Cell.BooleanCell):
  """ Behaves as per Conway's Game of Life """
  
  def mutate(self):
    """ update cell state according to conway's rules: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules """

    s = sum ( n.state for n in self.neighbors )   # number of alive neighbors
    if self.state:                          # if alive
      if s > 3 or s < 2:                    #    and 2 or 3 neighbors
        self.toggle()                       #      kill the alive cell as by over population
    else:                                   # if dead
      if s == 3:                            #    and there are exactly 3 neighbors
        self.toggle()                       #      cell comes alive, as by reproduction


class GameOfLifeGrid(Cell.BooleanCellGrid):
  def makeCell(self, rowColTupleIdentity ):
    return GameOfLifeCell( rowColTupleIdentity )
      

if __name__ == '__main__':

  # Glider sequence 
  g = GameOfLifeGrid(10, 10)
  g.cells[0][1].state = True
  g.cells[1][2].state = True
  g.cells[2][0].state = True
  g.cells[2][1].state = True
  g.cells[2][2].state = True
  
  for i in range(20):
    print str(g)
    g.tick()
