import model, Pyro4

class remoteModelServer(object):
  """ Provides access to remote viewers/controllers of an underlying model via Pyro4 
      
      Controllers may modify the model via the modify() after first adding themselves to the list of Controllers 
      using addController(). The model must implement a modify() method.  
      
      Viewers register for updates using addViewer() and must then implement a refresh() method to receive 
      update notifications.
      
      Subclasses implement a query method to return a dictionary of data to the viewer
  """ 
  
  def __init__(self, model):  
    self.model = model
    self.controllers = []
    self.viewers = []

  def addController(self, controller):
    print 'adding a new controller:', controller
    self.controllers.append(controller)
    print 'list of controllers now:', self.controllers
  
  def addViewer(self, viewer):
    print 'adding a new viewer', viewer
    self.viewers.append(viewer)
    print 'list of viewers now: ', self.viewers
  
  def updateViewers(self):
    for v in self.viewers:
      v.refresh()
  
  def modify(self, controller, **kwargs):
    if self.validateController(controller):
      if self.model.modify(**kwargs):
        self.updateViewers()
   
  def query(self):
    """ Overridden by subclasses - used by remote viewers to see serializable model data """
    return {}
    
# Internal methods
  def validateController(self, controller):
    print 'validating controller', controller
    if self.controllers.count(controller) > 0:
      print 'Validated'
      return True
    else:
      print 'Controller invalid'
      return False



class exampleRemoteModelServer(remoteModelServer):
  def query(self):
    """ Return a dictionary of data from the underlying model """
    return { 'name'  : self.model.name, 
             'value' : self.model.value } 


if __name__=="__main__":
  rs = exampleRemoteModelServer( model.SimpleModel() )
  Pyro4.Daemon.serveSimple( { rs: "remoteServer" }, ns = True)
    
    