
import time
from cell.gameOfLife import GameOfLifeGrid
from cell.CellNet import BooleanGrid_VC 

# Glider sequence 
g = GameOfLifeGrid(6, 6)
vc = BooleanGrid_VC(g)

print 'An initial glider: ', time.clock()
# Initial glider
vc.updateCell(0,1); vc.updateCell(1,2);  vc.updateCell(2,0);  vc.updateCell(2,1);  vc.updateCell(2,2)
print vc 

generationLeaps = 4
for i in range(3):
  vc.play(generationLeaps)
  print 'Glider after %i generations:' % ((i+1)*generationLeaps)
  print time.clock(),'\n',vc
