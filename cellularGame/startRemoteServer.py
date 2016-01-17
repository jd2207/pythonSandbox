import Pyro4 

#import pyroMVC.remoteModel
#if __name__=="__main__":
#  rs = pyroMVC.remoteModel.ExampleRemoteModelServer()
#  Pyro4.Daemon.serveSimple( { rs: "remoteServer" }, ns = True)

'''
import pyroMVC.remoteTicker
if __name__=="__main__":
  rs = pyroMVC.remoteTicker.RemoteTickerServer()
  Pyro4.Daemon.serveSimple( { rs: "remoteServer" }, ns = True)
'''

import pyroMVC.remoteTicker
if __name__=="__main__":
  rs = pyroMVC.remoteTicker.SimpleRemoteTickerServer()
  Pyro4.Daemon.serveSimple( { rs: "remoteServer" }, ns = True)
