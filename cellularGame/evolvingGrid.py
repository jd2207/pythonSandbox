import CellGrid

class EvolvingGrid(object):
  def __init__(self, cellGrid):
    self.tickNo = 0
    self.grid = cellGrid

  def tick(self):
    self.tickNo += 1
    self.grid.nextState()     # create new grid based on the old one and overwrite old one
    
  def dump(self):
    print 'Tick: %i' % self.tickNo
    self.grid.dump()


if __name__ == '__main__':

  '''
  print '\nAn evolving grid, initial state:'
  g1 = CellGrid.BooleanGrid(20, 20)
  
  eg = EvolvingGrid(g1)
  eg.dump()

  for i in range(5):
    eg.tick()
    eg.dump()
  '''

  print '\nA glider!:'
  g1 = CellGrid.GameOfLifeGrid(20, 20)
  g1[5][1].state = True
  g1[5][2].state = True
  g1[5][3].state = True
  g1[4][3].state = True
  g1[3][2].state = True
  g1.dump()

  eg = EvolvingGrid(g1)
  eg.dump()

  for i in range(10):
    eg.tick()
    eg.dump()
  