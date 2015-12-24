import Cell, CellViewerController


class GameOfLifeCell(Cell.BooleanCell):
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


class GameOfLifeGrid(Cell.BooleanCellGrid):
  def makeCell(self, rowColTupleIdentity ):
    return GameOfLifeCell( rowColTupleIdentity )
      

import time

if __name__ == '__main__':

  # Glider sequence 
  g = GameOfLifeGrid(100, 100)
  v = CellViewerController.BooleanGridViewerController(g)

  print 'An initial glider: ', time.clock()
  # Initial glider
  v.updateCell(0,1); v.updateCell(1,2);  v.updateCell(2,0);  v.updateCell(2,1);  v.updateCell(2,2)
  print v 

  generationLeaps = 40
  for i in range(3):
    v.play(generationLeaps)
    print 'Glider after %i generations:' % ((i+1)*generationLeaps)
    print time.clock(),'\n',v
