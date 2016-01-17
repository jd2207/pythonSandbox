
import time
from cell.gameOfLife import GameOfLifeGrid
from cell.cellNet import CellGrid_VC 

'''
# Glider sequence not using tickable.Ticker function
g = GameOfLifeGrid(6, 6)
vc = CellGrid_VC(g)

print 'An initial glider: ', time.clock()
# Initial glider
vc.updateCell(0,1); vc.updateCell(1,2);  vc.updateCell(2,0);  vc.updateCell(2,1);  vc.updateCell(2,2)
print vc 

for i in range(4):
  vc.doTick()
  vc.refreshOnTock()
print vc 
'''

# Glider sequence using tickable.Ticker function
# Glider sequence not using tickable.Ticker function
g = GameOfLifeGrid(6, 6)
vc = CellGrid_VC(g)

print 'An initial glider: ', time.clock()
# Initial glider
vc.updateCell(0,1); vc.updateCell(1,2);  vc.updateCell(2,0);  vc.updateCell(2,1);  vc.updateCell(2,2)
print vc 

vc.play()
time.sleep(vc.cellNet.period * 3 * 1.1)     # wait a bit more than 3 periods = 4 generations 
vc.pause()
print vc 



'''
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
'''