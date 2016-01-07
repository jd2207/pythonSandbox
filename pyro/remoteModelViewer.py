import Pyro4

class remoteModelViewer(object):
  """ An object which registers with, and then continually listens to, a remote pyroServer.
      Sub-classes must implement a refresh() method to react to server notifications
  """
  
  def __init__(self, remoteServerName):
    self.remoteServer = Pyro4.Proxy('PYRONAME:' + remoteServerName)
    
    daemon = Pyro4.Daemon()
    daemon.register(self)
    print 'Register with the server...'
    self.remoteServer.addViewer(self)

    print 'Listening for notifications...'
    daemon.requestLoop()

  
  def refresh(self):
    print 'Received a refresh notification from the server'
    print 'Model values returned:', self.remoteServer.query()

    
if __name__ == "__main__":
  viewer = remoteModelViewer('remoteServer')
