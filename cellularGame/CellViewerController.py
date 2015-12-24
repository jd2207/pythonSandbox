""" simple Classes for viewing/controlling Cells and CellNets """

from pubsub import pub


class CellViewerController(object):
    """ Super simpler 'py' - used to test pubsub functionality on a Cell"""
    def __init__(self, cell):
      """ Associate this py with a Cell """
      self.setCell(cell)
      pub.subscribe(self.refresh, 'Cell-Modified')    # register to listen for Cell-Modified events, and bind to a view refresh 
      self.refresh()
    
    def setCell(self, cell):
      """ Point the py to a (different) cell """
      self.cell = cell
      self.refresh()
          
    def mutateCell(self):
      """ Make a change to the underlying Cell """
      self.cell.modify(True)
      
    def updateCell(self, **kwargs):
      self.cell.modify(False, **kwargs)

    def refresh(self):
      """ Default refresh simply updated the string associated with the CellVC """
      self.updateStr()
    
    def updateStr(self):
      """ Overridden by subclasses """
      self.strValue = self.cell.identity

    def __str__(self):
      """ Overridden by subclasses """
      return self.strValue 



class IntegerCellViewerController(CellViewerController):
    """ Simple py/controller specific for IntegerCell"""
    
    def updateStr(self):
      self.strValue = str(self.cell.state)



class BooleanCellViewerController(CellViewerController):
    """ Simple py/controller specific for BooleanCell"""
          
    def updateStr(self):
      self.strValue = '*' if self.cell.state else '-'
      



# ==================================================================================================
# Grid Viewer Controllers 
# ==================================================================================================


class CellGridViewerController(object):
  """ Generic viewer/controller for CellGrid objects 
  
  Usage:  see example of BooleanGridViewerController class
  
  """
  
  def __init__ (self, cellGrid):
    self.cellGrid = cellGrid
    self.setViewers()
    pub.subscribe(self.refreshOnTick, 'CellNet-Ticked')   # register to listen for tick() events, and bind to refreshOnTick() 
    
  def setViewers(self):
    """ Overridden by subclasses - creates a list of CellViewerController objects for the grid"""
    self.viewers = [ [ CellViewerController.CellViewerController(cell) for cell in row ] for row in self.cellGrid.cells ]
    
  def mutateCell(self, row, col):
    cell = self.cellGrid.cells[row][col]
    cell.mutate()
    self.viewers[row][col].refresh()    
    
  def updateCell(self, row, col, **kwargs):
    cell = self.cellGrid.cells[row][col]
    cell.update(**kwargs)
    self.viewers[row][col].refresh()    
  
  def play(self, generations=1):
    """ tick() the underlying grid object a given number of times """
    self.cellGrid.tick(generations)
    
  def refreshOnTick(self):
    """ recreate the viewers """
    for vrow in self.viewers:
      for v in vrow:
          v.setCell(v.cell.descendant)
    
  def refresh(self):
    """ Overridden by subclasses """
    pass
    
  def __str__(self):
    """ Display a textual view of the grid state"""
    cols = self.cellGrid.cols
    s =  '---' * (cols + 1) + '\n' 
    s += '   ' +  (' %i ' * cols) % tuple(range(cols)) + '\n'
    i = 0
    for row in self.viewers:
      s += ' %i ' % i
      for viewer in row:
        s += ' ' + str(viewer) + ' ' 
      s += '\n'
      i += 1
    s += '---' * (cols + 1)
    return s


class BooleanGridViewerController(CellGridViewerController):
  """ Generic viewer/controller for BooleanCellGrid objects 
  
  Usage: 
  >>> import Cell, CellViewerController
  >>> g = Cell.BooleanCellGrid(3,3)
  >>> vc = CellViewerController.BooleanGridViewerController(g)
  >>> vc.modifyCell(0,1,state=1)
  >>> vc.modifyCell(1,1,state=1)
  >>> vc.modifyCell(2,1,state=1)
  
  >>> print vc
------------
    0  1  2
 0  -  *  -
 1  -  *  -
 2  -  *  -
------------
  >>> vc.tick()
  >>> print vc
------------
    0  1  2
 0  *  -  *
 1  *  -  *
 2  *  -  *
------------
  """
    
  def setViewers(self):
    """ Overridden by subclasses - creates a list of CellViewerController objects for the grid"""
    self.viewers = [ [ BooleanCellViewerController(cell) for cell in row ] for row in self.cellGrid.cells ]


  
if __name__ == '__main__':
  print "For tests use module 'testCellViewerController'"