Notes for pyro package 
=======================

Summary and Usage
==================

Now have a remoteModel module containing RemoteModelServer and RemoteModelViewer
The module also has simple example subclasses: ExampleRemoteModel, ExampleRemoteModelServer, ExampleRemoteModelViewer
Also startRemoteViewer.py and startRemoteViewer.py for starting viewer and server respectively. 
See also remoteTicker module containing remoteTickerServer and RemoteTickerViewer (using ticker as the underlying model).

To execute / test
======================

Open 4 command windows then these steps in each:

1. Start a pyro name server:

pyro4-ns

2. Edit and run startRemoteServer.py

3. Edit and run startRemoteViewer.py 
=> Observe that the server console confirms that a new viewer is added

4. Open an interactive python console (acting as a Controller)

Example where remoteServer is ExampleRemoteModelServer and remoteViewer is ExampleRemoteModelViewer   
>>> import Pyro4
>>> rm = Pyro4.Proxy("PYRONAME:remoteServer")
>>> rm.query()
{u'name': u'xxx', u'value': 0}
>>> rm.doModify( { 'name' : 'newname', 'value' : 99} )
On viewer console now see:
	Received a refresh notification from the server
	Model values now: {u'name': u'blah', u'value': -5}


To Do
======

- Put on hold the idea of validating who is a valid controller. For now only have python shell as the controller (or at worst, a single test script)
- But ultimately, for all controller actions (any method that is not purely "read-only"), the controller needs to be validated, recorded and the viewers flagged of need to refresh.

* add proper logging with timestamps

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

