
import pSystem, pSystemViewer, time

# Setup a particle system
# ps = pSystem.firstExample()
ps = pSystem.random1()
#ps = pSystem.earthMoonSun()

# Do the simulation 
v = pSystemViewer.Viewer(ps)
while len(ps) > 0:
    ps.tickSimulation()  
    ps.debug()
    v.update()   
    time.sleep(0.001)
    

