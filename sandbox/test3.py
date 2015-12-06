
import ticker, tickable, time
    
a = tickable.tickable(5)
b = tickable.tickable(500)
t = ticker.ticker([a,b])

# Query values 
'Tick #, (a,b)', t.tickNo, (a.prop(), bprop())
        
# Reset values
a.prop(0), b.prop(10)

# Finally
    
t.end()
    
    
