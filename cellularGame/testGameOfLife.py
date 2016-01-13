
import time
from cell.gameOfLife import GameOfLifeGrid
from cell.cellNet import CellGrid_VC 

# Glider sequence 
g = GameOfLifeGrid(6, 6)
vc = CellGrid_VC(g)

print 'An initial glider: ', time.clock()
# Initial glider
vc.updateCell(0,1); vc.updateCell(1,2);  vc.updateCell(2,0);  vc.updateCell(2,1);  vc.updateCell(2,2)
print vc 

print 'After 4 generations'
vc.setPeriod(0.1)
for i in range(4):
  vc.play()
print vc

print 'After 8 generations'
vc.setPeriod(0.1)
for i in range(4):
  vc.play()
print vc
