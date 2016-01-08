import Pyro4 

#import remoteModel
#if __name__=="__main__":
#  rs = remoteModel.ExampleRemoteModelServer()
#  Pyro4.Daemon.serveSimple( { rs: "remoteServer" }, ns = True)

import remoteTicker
if __name__=="__main__":
  rs = remoteTicker.RemoteTickerServer()
  Pyro4.Daemon.serveSimple( { rs: "remoteServer" }, ns = True)
