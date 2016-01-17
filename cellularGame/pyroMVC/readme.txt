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

3. Edit and run startRemoteViewer.py (or indeed multiple viewer consoles)
=> Observe that the server console confirms that a new viewer is added

4. Open an interactive python console (acting as a Controller)

Example 1. remoteServer is ExampleRemoteModelServer and remoteViewer is ExampleRemoteModelViewer   
>>> import Pyro4
>>> rm = Pyro4.Proxy("PYRONAME:remoteServer")
>>> rm.query()
{u'name': u'xxx', u'value': 0}
>>> rm.doModify( { 'name' : 'newname', 'value' : 99} )
On viewer console(s) now see:
	Received a refresh notification from the server
	Model values now: {u'name': u'newname', u'value': 99}


Example 2. remoteServer is RemoteTickerServer and remoteViewer is RemoteTickerViewer   
Follow steps 1-3 above then..

>>> import Pyro4
>>> rm = Pyro4.Proxy("PYRONAME:remoteServer")
>>> rm.query()
{u'tickNo': 0, u'playing?': False, u'period': 1}
>>> rm.play()
<some seconds go by ...>
>>> rm.query()
{u'tickNo': 10, u'playing?': True, u'period': 1}
<some seconds go by ...>
>>> rm.pause()
>>> rm.query()
{u'tickNo': 16, u'playing?': False, u'period': 1}
On viwer console see: 
Received a refresh notification from the server
State of ticker {u'tickNo': 1, u'playing?': True, u'period': 1}
Received a refresh notification from the server
State of ticker {u'tickNo': 2, u'playing?': True, u'period': 1}
Received a refresh notification from the server
State of ticker {u'tickNo': 3, u'playing?': True, u'period': 1}
...
Received a refresh notification from the server
State of ticker {u'tickNo': 16, u'playing?': True, u'period': 1}

Example 3. remoteServer is SimpleRemoteTickerServer and remoteViewer is SimpleRemoteTickerViewer   
Follow steps 1-3 above then..

>>> import Pyro4
>>> rm = Pyro4.Proxy("PYRONAME:remoteServer")
>>> rm.query()
({u'tickNo': 0, u'playing?': False, u'period': 1}, u'Value:', 0)
>>> rm.play()
>>> rm.pause()
On viewer console see:
Received a refresh notification from the server
Model values now: ({u'tickNo': 1, u'playing?': True, u'period': 1}, u'Value:', 1)
Received a refresh notification from the server
Model values now: ({u'tickNo': 2, u'playing?': True, u'period': 1}, u'Value:', 2)
Received a refresh notification from the server
Model values now: ({u'tickNo': 3, u'playing?': True, u'period': 1}, u'Value:', 3)
... 



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

