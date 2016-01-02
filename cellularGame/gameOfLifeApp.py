import wx 
import Cell, CellNet
import gameOfLife


class GameFrame(wx.Frame, CellNet.BooleanGrid_VC):
  def __init__(self, parent, title, cellGrid):
    wx.Frame.__init__(self, parent, title=title, size=(500, 500))
    CellNet.BooleanGrid_VC.__init__(self, cellGrid)
            
    self.setTickTime()          
            
    menubar = wx.MenuBar()
    fileMenu = wx.Menu()
    self.playMenuItem = fileMenu.Append(wx.ID_ANY, '&Play')

    self.pauseMenuItem = fileMenu.Append(wx.ID_ANY, 'P&ause')
    self.pauseMenuItem.Enable(False)
    
    menubar.Append(fileMenu, '&Menu')
    self.SetMenuBar(menubar)
    
    self.timer = wx.Timer(self)
        
    self.Bind(wx.EVT_MENU, self.doPlay, self.playMenuItem)
    self.Bind(wx.EVT_MENU, self.doPause, self.pauseMenuItem)
    self.Bind(wx.EVT_TIMER, self.doPlay, self.timer)
        
    self.InitUI()
    self.Centre()
    self.Show()     
       
  def setTickTime(self, period=5000):
    self.period = period                 # seconds between autonomous ticks, default = 5 seconds
     
  # override setViewers() fromCellGridViewerController       
  def setViewers(self):
    self.viewers =  [ [ BooleanCellPanel(self, cell) for cell in row ] for row in self.cellGrid.cells ]

  def doPlay(self, evt):
    self.playMenuItem.Enable(False)
    self.pauseMenuItem.Enable(True)
    self.timer.Start(self.period)
    self.play()

  def doPause(self, evt):
    self.pauseMenuItem.Enable(False)
    self.playMenuItem.Enable(True)
    self.timer.Stop()
    
  def onTimer(self, evt):
    self.doPlay()

  def InitUI(self):
    self.gs = wx.GridSizer(self.cellGrid.rows, self.cellGrid.cols, 1, 1)

    # Add a panels for each CellViewerController of the grid
    [ [ self.gs.Add( v, 0, wx.EXPAND ) for v in row ] for row in self.viewers ]
        
    self.SetSizer(self.gs)
    self.statusbar = self.CreateStatusBar()
  
        

class BooleanCellPanel(wx.Panel, Cell.BooleanCell_VC):
  def __init__(self, parent, cell):
    wx.Panel.__init__(self, parent)
    Cell.BooleanCell_VC.__init__(self, cell)
    self.Bind(wx.EVT_LEFT_UP, self.toggleCell)
          
  def toggleCell(self, e):
    self.updateCell()

  def refresh(self):   
    clr = wx.Colour(0,0,0) if self.cell.state else wx.Colour(255,255,255)  
    self.SetBackgroundColour( clr )
    Cell.BooleanCell_VC.refresh(self)
    wx.Panel.Refresh(self) 

      

class GameOfLifeApp(wx.App):
  
  def OnInit(self):
    model = gameOfLife.GameOfLifeGrid(10,10)
    self.frame = GameFrame(parent=None, title="Interactive Game of Life", cellGrid=model)
    self.frame.Show()
    self.SetTopWindow(self.frame)
    return True


if __name__ == '__main__':
  app = GameOfLifeApp()
  app.MainLoop()
