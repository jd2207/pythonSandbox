""" simple Classes for viewing/controlling Cells and CellNets """

from pubsub import pub


class CellViewerController(object):
    """ Super simpler 'viewer' - used to test pubsub functionality on a Cell"""
    def __init__(self, cell):
      """ Associate this viewer with a Cell """
      self.setCell(cell)
      pub.subscribe(self.refresh, 'Cell-Modified')    # register to listen for Cell-Mutation events, and bind to a view refresh 
      self.refresh()
    
    def setCell(self, cell):
      """ Point the viewer to a (different) cell """
      self.cell = cell
      self.refresh()
          
    def modify(self, **kwargs):
      """ Make a change to the underlying Cell """
      self.cell.modify(**kwargs)

    def refresh(self):
      """ Overridden by subclasses """
      self.strValue = 'X'
      
    def __str__(self):
      return self.strValue



class IntegerCellViewerController(CellViewerController):
    """ Simple viewer/controller specific for IntegerCell"""
          
    def refresh(self):
      self.strValue = str(self.cell.state)



class BooleanCellViewerController(CellViewerController):
    """ Simple viewer/controller specific for BooleanCell"""
          
    def refresh(self):
      self.strValue = '*' if self.cell.state else '-'



class CellGridViewerController(object):
  """ Generic viewer/controller for CellGrid objects 
  
  Usage:  see example of BooleanGridViewerController class
  
  """
  
  def __init__ (self, cellGrid):
    self.cellGrid = cellGrid
    self.setViewers()
    pub.subscribe(self.refreshOnTick, 'CellNet-Ticked')   # register to listen for tick() events, and bind to refreshOnTick() 
    
  def getcellViewerControllerClass(self):
    return 'CellViewerController'

  def setViewers(self):
    cellViewerControllerClass = self.getcellViewerControllerClass()
    self.viewers = [ [ getattr(__import__('CellViewerController'), cellViewerControllerClass)(cell) for cell in row ] for row in self.cellGrid.cells ]
    return 
    
  def modifyCell(self, row, col, **kwargs):
    self.cellGrid.cells[row][col].modify(**kwargs)    
  
  def play(self, generations=1):
    """ tick() the underlying grid object a given number of times """
    self.cellGrid.play(generations)
    
  def refreshOnTick(self):
    """ recreate the viewers """
    for vrow in self.viewers:
      for v in vrow:
          v.setCell(v.cell.descendant)
    
    
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
    
  def getcellViewerControllerClass(self):
    return 'BooleanCellViewerController'



  
if __name__ == '__main__':
  print "For tests use module 'testCellViewerController'"