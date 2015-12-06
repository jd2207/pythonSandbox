'''
Module representing a mathematical model of a system of particles and their mutual interaction (e.g via gravity, collisions)

Class ParticleSystem extends standard 'list' and represents the system as a whole

Class Particle allows instantiation of individual particles with physical properties  

Usage (see also example subcl

import pSystem
ps = pSystem.ParticleSystem()
ps.setBoundary(b)                    # optionally add a boundary

p1 = pSystem.Particle()              # add particles to the system (with position, speed, mass etc...)
p2 = pSystem.Particle()
...
ps.append(p1)
ps.remove(p2)
..

Then simulation via:
    for i in range(iterations):
        ps.tickSimulation()  
OR 
    while condition:
        ps.tickSimulation(iterations)
'''


import boundary 
from turtle import Vec2D


# System wide globals 
GRAVITY = 8
DELTA_T = 0.01
ROCHE = 4

# ---------------------------------------------------------
# Module functions 
# ---------------------------------------------------------

def collision(p1, p2):
    if not p1 is p2 and abs(p2.position - p1.position) < ROCHE:
        return True
    else:
        return False

def combine(p1,p2):
    mass = p1.mass + p2.mass
    pos = (p1.mass * p1.position + p2.mass * p2.position) * (1.0/mass)
    vel = ((p1.mass * p1.velocity) + (p2.mass * p2.velocity)) * (1.0/mass) 

    p3 = Particle(pos,vel,mass)
    return p3 

# ---------------------------------------------------------
# Class Particle  
# ---------------------------------------------------------
class Particle(object):
    def __init__(self,pos=Vec2D(0,0),vel=Vec2D(0,0),mass=1.0):
        self.mass = mass
        self.position = pos
        self.velocity = vel
        self.status = 1
        
    def move(self,dt): 
        self.position += dt * self.velocity

    def accelerate(self,acc,dt):
        self.velocity += dt * acc

    def debug(self):
        print self.position


# ---------------------------------------------------------
# Class ParticleSystem  
# ---------------------------------------------------------
class ParticleSystem(list):
    
    def __init__(self):
        self.collisions = 0
        self.tick = 0
        self.boundary = None

    def append(self,p):
        super(ParticleSystem,self).append(p)

    def remove(self,p):
        super(ParticleSystem,self).remove(p)
        p.status = 0

    def tickSimulation(self,iterations=1):
        for i in range(iterations):
            self.tick += 1
            for p in self:                 
                p.move(DELTA_T)
                g = self.acc(p)                        # calc the acceleration due to gravity on a given particle
                p.accelerate(g,DELTA_T)                # change the particle speed 

                self.applyBoundary()                   # apply boundary to the particles                   
                self.applyCollisions()                 # deal with collisions

    def addBoundary(self,b):
        self.boundary = b

# Internal methods

    def applyBoundary(self):

        if self.boundary:
            for p in self:
                if self.boundary.trigger(p.position):
                    p.position = self.boundary.apply(p.position)
#                    self.remove(p)


    def applyCollisions(self):
    
        toBeRemoved = []
        copy1 = list(self)
    
        while len(copy1) > 0:
            i = copy1.pop(0)
            copy2 = list(copy1)

            collisionHappened = False

            while (len(copy2)) > 0 and not collisionHappened:
                j = copy2.pop(0)
                if collision(i,j):
                    k = combine(i,j)
                    collisionHappened = True
                    self.collisions += 1
                    copy1.remove(j)
                
                    copy1.append(k)
                    self.append(k)
                    toBeRemoved.extend([i,j])
    
        for i in toBeRemoved:
            self.remove(i)


    def acc(self,p):
        a = Vec2D(0,0)
        for o in self:
            if o != p:                            # apply law of gravity
                r = o.position - p.position
                a += ( GRAVITY * o.mass / abs(r)**3) * r
        return a

# --- Debug only ----------------------------------------------------------
    
    def totMomentum(self):
        pT = Vec2D(0,0)
        for p in self:
            pT += p.mass * p.velocity
        return pT

    def debug(self):
        print self.tick, len(self), self.collisions, self.totMomentum()


# -------------------------------------------------------------------------
# Example systems as subclasses
# -------------------------------------------------------------------------

class firstExample(ParticleSystem):
    def __init__(self):
        super(firstExample,self).__init__()
        self.addBoundary(boundary.RectangularBoundary(300,300))
        self.append( Particle( Vec2D(0,0),     Vec2D(1,0.5))    )
        self.append( Particle( Vec2D(-20,-30), Vec2D(-1.2,0.7)) )
        self.append( Particle( Vec2D(40,60),   Vec2D(-1,-0.35)) )
        self.append( Particle( Vec2D(100,-50), Vec2D(-2,0.61))  )


import random
class random1(ParticleSystem):                      # Some random turtles, square boundary 
    def __init__(self):
        super(random1,self).__init__()
        self.addBoundary(boundary.RectangularBoundary(500,500))
        for i in range(10):
            pos = Vec2D( random.randrange(-200,200)  , random.randrange(-200,200)   )
            vel = Vec2D( random.randrange(-100,100,1), random.randrange(-100,100,1) )  * 0.005
            self.append(Particle(pos,vel))

class earthMoonSun(ParticleSystem):
    def __init__(self):
        super(earthMoonSun,self).__init__()
        sun = Particle(Vec2D(0,0), Vec2D(0.01,-2.5), 1000000); self.append(sun)
        earth = Particle(Vec2D(210,0), Vec2D(-0.91,195), 12500); self.append(earth)
        moon = Particle(Vec2D(220,0), Vec2D(-5.83,295), 1); self.append(moon)

