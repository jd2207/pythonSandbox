'''
  Module used to display the simulation of a pSystem.ParticleSystem using turtle graphics
'''

import turtle, time, boundary
from turtle import Vec2D

UPDATE_FREQ = 10      # screen refresh rate in Hz

class Viewer():
    
    def __init__(self,ps):

        self.ps = ps
        
        # Initialize the display
        self.defaultTurtle = turtle.Turtle()
        self.screen = self.defaultTurtle.getscreen()

        # Draw boundary
        self.drawBoundary()
        self.screen.tracer(0)

        self.turtles = []
        self.lastUpdateTime = 0

    def drawBoundary(self):
        
        if (self.ps.boundary):
            b = self.ps.boundary
        else:
            return None
        
        t = self.defaultTurtle
        
        t.pu();t.ht()
        if isinstance(b,boundary.RectangularBoundary):
            (w,h) = Vec2D(b.width,b.height) * 0.5
            t.setpos(-w,-h)
            t.pd()
            t.setpos( w,-h)
            t.setpos( w, h)
            t.setpos(-w, h)
            t.setpos(-w,-h)

            t.pu()                                      # x axis
            t.setpos(-w,0)
            t.pd()
            t.setpos(+w, 0)

            t.pu()                                      # y-axis
            t.setpos(0,-h)
            t.pd()
            t.setpos(0,+h)

        elif isinstance(b,boundary.CircularBoundary):
            r = b.radius
            t.setpos(Vec2D(0,r))
            t.pd()
            t.circle(r)

            t.pu()                                      # x axis
            t.setpos(-r,0)
            t.pd()
            t.setpos(+r, 0)

            t.pu()                                      # y-axis
            t.setpos(0,-r)
            t.pd()
            t.setpos(0,+r)

    def update(self):

        tnow = time.time()

        if (tnow - self.lastUpdateTime) > (1.0 / UPDATE_FREQ):
            for p in self.ps:
                if p.status == 1:               # if a new one has been added
                    p.status = 2
                    self.turtles.append(OrbTurtle(p))
    
                for t in self.turtles:        
                    if t.particle.status == 0:      # if one has been removed, remove the turtle
                        self.screen.tracer(1)
                        t.ht()
                        t.clear()
                        self.screen.tracer(0)
                        self.screen.turtles().remove(t)
                        self.turtles.remove(t)
                    else:
                        t.update()
    
            self.screen.update()
            self.offset = Vec2D(0,0)
            self.lastUpdateTime = tnow

    def debug(self):
        for t in self.turtles:
            print "Turtle position is now ",t.pos()



class OrbTurtle(turtle.Turtle):                 # view corresponding to a pSystem.Paricle instance

    def __init__(self,particle):
        
        super(OrbTurtle,self).__init__()
        self.particle = particle
        self.ht(); self.pu()
    
        self.shape("circle")
        self.st()
        self.color("black")
                
    def update(self):
        self.setpos(self.particle.position)
        
