# --------------------------------------------------------------------------------------------------
#  remoteModelServer and remoteModelViewer that uses a simpl ticker object as the underlying model 
#  c.f. remoteModel.py
# -----------------------------------------------------------------------------------------

import cell.ticker, remoteModel
from pubsub import pub

class RemoteTickerServer(remoteModel.RemoteModelServer):

  def setModel(self):
    self.model = cell.ticker.SimpleTicker()
    pub.subscribe(self.updateViewers, 'Tock')   # register to listen for tick() of underlying model and bind to updateViewers() 

  def play(self):
    self.model.play()
    
  def pause(self):
    self.model.pause()

  def query(self):
    return { 'value' : self.model.value }


class RemoteTickerViewer(remoteModel.RemoteModelViewer):
  def refresh(self):
    print 'Received a refresh notification from the server\n','Model values now:', self.remoteServer.query()

      