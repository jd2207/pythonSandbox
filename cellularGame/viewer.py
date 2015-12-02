import wx
import model

class myPanel(wx.Panel):
    def __init__(self, parent, unitArea):
        super(myPanel, self).__init__(parent) 
            
        self.unitArea = unitArea
        self.Bind(wx.EVT_LEFT_UP, self.toggleState)
        self.Refresh()

    def toggleState(self, e):
        self.unitArea.state = False if self.unitArea.state else True
        self.Refresh()
        self.Parent.statusbar.SetStatusText('state toggled to %i' %  self.unitArea.state)
        
    def Refresh(self):
        clr = wx.Colour(0,0,0) if self.unitArea.state else wx.Colour(255,255,255)  
        self.SetBackgroundColour( clr )
        super(myPanel, self).Refresh() 


class gridFrame(wx.Frame):
    def __init__(self, parent, title, gridModel):
        super(gridFrame, self).__init__(parent, title=title, size=(500, 500))

        self.gridModel = gridModel    
            
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        tickMenuItem = fileMenu.Append(wx.ID_ANY, '&Tick')
        menubar.Append(fileMenu, '&Menu')
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.performTick, tickMenuItem)
        
        self.InitUI()
        self.Centre()
        self.Show()     
        
        
    def InitUI(self):

        width = self.gridModel.width
        height = self.gridModel.height
        gs = wx.GridSizer(width, height, 1, 1)
        for row in range(width):
          for col in range(height):
            gs.Add(myPanel(self, self.gridModel.getArea(row, col)), 0, wx.EXPAND)
        
        self.SetSizer(gs)
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText(str(self.gridModel.tickNo))
      
    def performTick(self, e):
      self.gridModel.tick()
      
      
if __name__ == '__main__':

    m = model.Grid(20,20)
  
    app = wx.App()
    gridFrame(None, 'Grid Frame', m)
    app.MainLoop()