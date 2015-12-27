import wx 
import Cell, CellNet
import gameOfLife


class testFrame(wx.Frame, CellNet.BooleanGrid_VC):
  def __init__(self, parent, title, cellGrid):
    wx.Frame.__init__(self, parent, title=title, size=(500, 500))
    CellNet.BooleanGrid_VC.__init__(self, cellGrid)
            
    menubar = wx.MenuBar()
    fileMenu = wx.Menu()
    playMenuItem = fileMenu.Append(wx.ID_ANY, '&Play')
    menubar.Append(fileMenu, '&Menu')
    self.SetMenuBar(menubar)
        
    self.Bind(wx.EVT_MENU, self.doPlay, playMenuItem)
        
    self.InitUI()
    self.Centre()
    self.Show()     
        
  # override setViewers() fromCellGridViewerController       
  def setViewers(self):
    self.viewers =  [ [ BooleanCellPanel(self, cell) for cell in row ] for row in self.cellGrid.cells ]

  def doPlay(self, xxx):
    self.play()

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

      

class testPanelApp(wx.App):
  
  def OnInit(self):
    model = gameOfLife.GameOfLifeGrid(10,10)
#    model = Cell.BooleanCellGrid(10,10)
    self.frame = testFrame(parent=None, title="test frame", cellGrid=model)
    self.frame.Show()
    self.SetTopWindow(self.frame)
    return True


if __name__ == '__main__':
  app = testPanelApp()
  app.MainLoop()
