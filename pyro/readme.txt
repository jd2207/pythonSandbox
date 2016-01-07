To execute / test
======================

Open 4 command windows then these steps in each:

1. Start a pyro name server:

pyro4-ns

2. Start the remoteModel server 

python remoteModelServer.py

3. Interactive python console
python

>>> rs = Pyro4.Proxy("PYRONAME:remoteServer")
>>> rs.query()
>>> rs.addController()
>>> rs.modify( 'shell', name='xxx' )


4. Start a remoteModelViewer
python remoteModelViewer.py



To Do
======

* units tests for testing remoteModelServer 
	(need to be able to start server is a separate thread then perform a sequence like:
	 rs = Pyro4.Proxy("PYRONAME:remoteServer")
	 rs.query()
	 rs.addController()
	 rs.modify( <testClass>, name='xxx' )
	 rs.query()
	 rs.modify( <testClass>, value=99 )
	 rs.query()
	 rs.modify( <testClass>, name='yyy', value=1 )
	 rs.query()
	 
    can also add remoteViewer thread too
      redirect the output of remoteViewer to a file and check this
      redirect the output of remoteModelServer to a file and check this

 * how to remove/unregister a viewer from the list of viewers in the remote server if the viewer exits (leaves the daemon.requestLoop)
 
 
 Longer term
 ===============
 
*  Research the HMAC key thing to whitelist server access (at least for controllers).