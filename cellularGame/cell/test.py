import cell, cellNet, time

cn = cellNet.SimpleCellTriangle([ cell.IntegerCell('Cell A', 1), 
                                  cell.IntegerCell('Cell B', 5), 
                                  cell.IntegerCell('Cell C', 7) ])
cnvc = cellNet.CellNet_VC(cn)
print cnvc

cnvc.play()
time.sleep(10)
print cnvc
cnvc.pause()
