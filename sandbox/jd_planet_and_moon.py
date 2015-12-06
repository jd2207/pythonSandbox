#! /usr/bin/python3.3
"""       turtle-example-suite:

        tdemo_planets_and_moon.py

Gravitational system simulation using the
approximation method from Feynman-lectures,
p.9-8, using turtlegraphics.

Example: heavy central body, light planet,
very light moon!
Planet has a circular orbit, moon a stable
orbit around the planet.

"""
from turtle import Turtle, Vec2D as Vec
from time import sleep

G = 8
DT = 0.01

class GravSys(object):
    def __init__(self,system=[]):
        self.orbs = system
        self.timestamp = 0
   
    def acc(self,obj):
        a = Vec(0,0)
        for o in self.orbs:
            if o != obj:
                r = o.position - obj.position
                a += (G*o.mass/abs(r)**3)*r
        return a

    def tick(self):
        for o in self.orbs:
            o.move()              # move the orb to new position
            acc = gs.acc(o)       # calc the acceleration due to gravity on a given orb
            o.accelerate(acc)        # change the orb speed 
        self.timestamp += DT

    def debug(self):
        print ("Time:", self.timestamp)
        for o in self.orbs:
            print (o.position,o.velocity)

class Orb:
    def __init__(self,name,mass,pos,vel):
        self.name = name
        self.mass = mass
        self.position = pos
        self.velocity = vel
        
    def move(self):
        self.position += DT * self.velocity

    def accelerate(self,acc):
        self.velocity += DT * acc

class OrbTurtle(Turtle):
    def __init__(self, orb, color, size):
        Turtle.__init__(self, shape="circle")
  
        self.color(color)
        self.shapesize(size)
        self.resizemode("user")

        self.pu()
        self.orb = orb
        self.setpos(self.orb.position)
        self.pd()

    def move(self):
        self.setpos(self.orb.position)
        
# Main --------------------------------------------------------------------------
  
## Setup gravitational system
sun = Orb("Sun",1000000, Vec(0,0), Vec(0.01,-2.5))
earth = Orb("Earth",12500, Vec(210,0), Vec(-0.91,195))
moon = Orb("Moon",1, Vec(220,0), Vec(-5.83,295))
gs = GravSys([sun,earth,moon])

s = Turtle()
s.reset()
s.getscreen().tracer(0,0)
s.ht()
s.pu()
s.fd(6)
s.lt(90)
s.getscreen().tracer(1,0)

    
## Turtles associated with each object
sunTurtle = OrbTurtle(sun,"yellow",1.8)
earthTurtle = OrbTurtle(earth,"blue",0.5)
moonTurtle = OrbTurtle(moon,"black",0.3)

sunTurtle.move()
    

while True: 
    gs.tick()
    for t in ([sunTurtle,earthTurtle,moonTurtle]):
        t.move()
        
        



