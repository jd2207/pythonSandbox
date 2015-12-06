'''
Usage:

import ticker, tickable, time
    
a = tickable.tickable(5)
b = tickable.tickable(500)
t = ticker.ticker([a,b])

# Query values 
'Tick #, (a,b)', t.tickNo, (a.prop(), b.prop())
        
# Reset values
a.prop(0), b.prop(10)

# Finally
    
t.end()
'''

import threading

THREAD_TIMER = 5

class ticker:
 
    def __init__(self,tickables):

        self.tickables = tickables
        self.tickNo = 0
        self.clock()         # Keeps updating the list of tickables

    def clock(self):
        self.tickNo += 1
        self.recalculate()
        self.t = threading.Timer(THREAD_TIMER, ticker.clock,[self])    # restart the timer
        self.t.start()
        
    def recalculate(self):
        for i in self.tickables:
            i.tick()
            
    def end(self):
        print 'Stopping the timer and ending the program...'
        self.t.cancel()
 
   

class tickable:
    
    def __init__(self,value=0):
        self.value = value
    
    def tick(self):
        self.value += 1
                
    def prop(self,newValue=None):
        if newValue != None:
            self.value = newValue
        return self.value  
        