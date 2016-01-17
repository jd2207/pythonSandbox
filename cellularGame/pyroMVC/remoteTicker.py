import cell.ticker, remoteModel
from pubsub import pub

class RemoteTickerServer(remoteModel.RemoteModelServer):
  """ An implementation of a remoteModelServer that provides access to a remote ticker.Tickable object """
  
  def __init__(self):
    super(RemoteTickerServer, self).__init__()
    pub.subscribe(self.updateViewers, 'Tock')   # register to listen for tick() of underlying model and bind to updateViewers() 

  def setModel(self):
    """ Usually overridden by subclasses """
    return cell.ticker.Tickable()

  def play(self):
    self.model.play()
    
  def pause(self):
    self.model.pause()

  def query(self):
    return self.model.toDict()



class RemoteTickerViewer(remoteModel.RemoteModelViewer):
  """ An implementation of a remoteModelViewer that provides access to a RemoteTickerServer """
  
  def refresh(self):
    super(RemoteTickerViewer, self).refresh()
    print 'State of ticker', self.remoteServer.query()



class SimpleRemoteTickerServer(RemoteTickerServer):
  """ Example subclass of RemoteTicketServer """
  def setModel(self):
    return cell.ticker.SimpleTicker()

  def query(self):
    return super(SimpleRemoteTickerServer, self).query(), 'Value:', self.model.getValue()



class SimpleRemoteTickerViewer(RemoteTickerViewer):
  """ Example subclass of RemoteTicketViewer """
  def refresh(self):
    print 'Received a refresh notification from the server\n','Model values now:', self.remoteServer.query()
