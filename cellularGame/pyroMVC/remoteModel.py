import Pyro4

class RemoteModelServer(object):
  """ Provides access to remote viewers/controllers of an underlying model via Pyro4 
      
      Controllers may modify the model data via the modify() after first adding themselves to the list of Controllers 
      using addController(). 
      
      For each method of the model that **modifies** any model data, the ModelServer needs to implement
      a corresponding method which passes the controller identity, so that the controller maybe recorded and validated  
      
      Viewers register for updates using addViewer() and must then implement a refresh() method to receive 
      update notifications.
      
      Subclasses implement a query method to return a dictionary of data to the viewer
      
      See exampleRemoteModelServer.
  """ 
  
  def __init__(self):  
    self.controllers = []
    self.viewers = []
    self.setModel()

  def setModel(self):
    pass

  def addViewer(self, viewer):
    print 'adding a new viewer', viewer
    self.viewers.append(viewer)
    print 'list of viewers now: ', self.viewers

  def updateViewers(self):
    print 'flagging refresh to all viewers'
    for v in self.viewers:
      v.refresh()

  def query(self):
    """ Overridden by subclasses """
    return {}
 
  '''    
  def addController(self, controller):
    print 'adding a new controller:', controller
    self.controllers.append(controller)
    print 'list of controllers now:', self.controllers
  
  def validateController(self, controller):
    print 'validating controller', controller
    if self.controllers.count(controller) > 0:
      print 'Validated'
      return True
    else:
      print 'Controller invalid'
      return False

  def modify(self, controller, dictObj):
    """ Cause the model data to change """
    if self.validateController(controller):
      self.doModify(dictObj)
      self.updateViewers()
  '''
    
class RemoteModelViewer(object):
  """ An object which uses Pyro4 to register with, and then continually listen to, a RemoteModelServer.
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
    """ Overridden by subclasses """


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
    self.model = ExampleRemoteModel()

  def doModify(self, dictObj):
    print 'doModify in progress'
    for key in dictObj:
      setattr(self.model, key, dictObj[key])
    self.updateViewers()

  def query(self):
    return { 'name' : self.model.name, 
             'value' : self.model.value }


class ExampleRemoteModelViewer(RemoteModelViewer):
  def refresh(self):
    print 'Received a refresh notification from the server\n','Model values now:', self.remoteServer.query()

  