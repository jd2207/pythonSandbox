import model
import Pyro4

class remoteServer(object):
  def __init__(self, model):
    self.model = model
    self.clients = []

# Methods used by remote controllers (active clients)
  def addClient(self, client):
    print 'adding a new client', client
    self.clients.append(client)
    print 'list of clients now: ', self.clients
  
  def increment(self, client):
    if self.validateClient(client):
      self.model.increment()
      return True
    else:
      return False

  def decrement(self, client):
    if self.validateClient(client):
      self.model.decrement()
      return True
    else:
      return False

# Methods used by remote controllers (passive clients)
  def query(self):
    return self.model.value

# Internal methods
  def validateClient(self, client):
    print 'validating client', client
    if self.clients.count(client) > 0:
      print 'Validated'
      return True
    else:
      print 'Client invalid'
      return False
    

def serverApp():
    m = model.model()
    rs = remoteServer(m)
    Pyro4.Daemon.serveSimple(
                             {
              rs: "remoteServer"
            },
            ns = True)

if __name__=="__main__":
    serverApp()
    
    