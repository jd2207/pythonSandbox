
import Cell


# -----------------------------------------------------------------------------------
class GameOfLifeCell(Cell.BooleanCell):
  """ Behaves as per Conway's Game of Life 
      Must define a parent grid 
  """
  
  def __init__(self, identity, parentGrid, state=False):          
    super(GameOfLifeCell,self).__init__(identity, parentGrid, state)
  
  def makeDescendant(self):
    g = self.parentGrid
    
    # Calculate the sum of the neighbors
    n = g.neighbors(self.identity[Cell.AbstractCell.ROW], self.identity[Cell.AbstractCell.COLUMN])
    s = 0
    for i in n:
      m = g[ i[0] ] [ i[1] ].state
      s += m
    
    # Conway's rules: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules
    newState = self.state
    if self.state:                          # if alive
      if s > 3 or s < 2:
        newState = not newState             # kill the alive cell
    else:                                   # if dead
      if s == 3:
        newState = not newState             # cell comes alive
        
    return GameOfLifeCell(self.identity, parentGrid=self.parentGrid, state=newState)  


# -----------------------------------------------------------------------------------
class GameOfLifeGrid(Cell.CellGrid):
  def createCell(self, identity):     
    return GameOfLifeCell(identity, self)
      

if __name__ == '__main__':

  g = GameOfLifeGrid(3,3)
  print str(g)
  
  # Blinker sequence
  g[0][1].state = True
  g[1][1].state = True
  g[2][1].state = True

  for i in range(5):
    print str(g)
    g.nextState()
