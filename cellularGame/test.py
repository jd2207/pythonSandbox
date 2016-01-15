
import Pyro4, time

rm = rm = Pyro4.Proxy("PYRONAME:remoteServer")
print rm.query()
rm.play()
print 'waiting 10 seconds ...'
time.sleep(10)
print rm.query()
rm.pause()
print rm.query()



'''
import cell.ticker, pyroMVC.remoteModel
from pubsub import pub

class RemoteCellTriangleServer(pyroMVC.remoteTicker):

  def setModel(self):
    self.model = cell.ticker.SimpleTicker()
    pub.subscribe(self.updateViewers, 'Tock')   # register to listen for tick() of underlying model and bind to updateViewers() 

  def play(self):
    self.model.play()
    
  def pause(self):
    self.model.pause()

  def query(self):
    return { 'value' : self.model.value }
  '''