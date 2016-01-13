
- Cell classes now independent of pypubsub (vc's use instead)
   - Remove modify() method
   - Changes to dump() and _str__
   
- Cellnet classes now independent of pypubsub (vc's use instead)
   - tick() becomes nextGen()
   
 - BooleanCellGrid has a str method()
 
 - Major changes to ticker/testTicket
   - tickable object may be play()ed a finite number of times (but no longer indefinite)

 - CellNet_VC now implements ticker.Tickable()



In progress
============

- gameOfLifeApp is currently broken   


Soon
===========



Then...
- CellGrid / CellNet or subclass to implement ticker.Tickable interface
  - class CellNet(object):  >>> class CellNet(ticker.Tickable)
  - CellNet.tick() becomes doTick()
  - need a new CellNet_VC class 
  - CellNet_VC becomes a subclass of CellNet_VC class
  - need to adjust testCellNet


Next-up
===========
- add debug logging 
- review all comments / usage and tests

Later
============
- add a Clear menu item
- inheritance diagram ??
- why do I need test.doPlay() and why the extra parameter ?

