import Pyro4

class RemoteModelServer(object):
  """ Provides access to remote viewers/controllers of an underlying model via Pyro4 
        
      Subclasses must: 

      * Define setModel() to create an instance of the model
      
      * Define an arbitrary number of 'controller' methods which *may* ultimately call updateViewers()
      
      * Define an arbitrary number of "viewer" methods which read data from the underlying modem 
      and return serializable data
      
     See exampleRemoteModelServer and exampleRemoteModelViewer

  """ 
  def __init__(self):  
    self.controllers = []
    self.viewers = []
    self.model = self.setModel()

  def setModel(self):
    """ Overridden by subclasses - returns an instance of the model associated with this server"""
    return None

  def addViewer(self, viewer):
    print 'adding a new viewer', viewer
    self.viewers.append(viewer)

  def updateViewers(self):
    print 'flagging refresh to all viewers'
    for v in self.viewers:
      v.refresh()



class RemoteModelViewer(object):
  """ An object which uses Pyro4 to register with, and then continually listen to, a RemoteModelServer.

      On creation, RemoteModelViewers register for updates with the RemoteServerModel by calling the 
      RemoteModelServers addViewer() method and must then implement a refresh() method to receive
      update notifications.

      Sub-classes may implement a refresh() method to react to server notifications
      Sub-classes may also call the 'viewer' methods of the RemoteModelServer (to query the RemoteModel)

  """
  def __init__(self, remoteServerName):
    self.remoteServer = Pyro4.Proxy('PYRONAME:' + remoteServerName)
    
    daemon = Pyro4.Daemon()
    daemon.register(self)
    print 'Registering with the server...'
    self.remoteServer.addViewer(self)

    print 'Listening for notifications...'
    daemon.requestLoop()
  
  def refresh(self):
    """ Overridden by subclasses """
    print 'Received a refresh notification from the server'


# ----------------------------------------------------------------------
# Example of a server, a viewer and underlying model 
# ----------------------------------------------------------------------

class ExampleRemoteModel(object):
  """ Simple class which stores two values """
  def __init__(self):
    self.value = 0
    self.name = 'xxx'


class ExampleRemoteModelServer(RemoteModelServer):

  def setModel(self):
    """ Creates the specific model used by this server """
    return ExampleRemoteModel()

  def doModify(self, dictObj):
    """ An example 'Controller' method """
    print 'doModify in progress'
    for key in dictObj:
      setattr(self.model, key, dictObj[key])
    self.updateViewers()

  def query(self):
    """ An example 'Viewer' method """
    return { 'name' : self.model.name, 
             'value' : self.model.value }


class ExampleRemoteModelViewer(RemoteModelViewer):
  def refresh(self):
    super(ExampleRemoteModelViewer, self).refresh()
    print 'Model values now:', self.remoteServer.query()
