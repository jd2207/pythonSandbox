'''
A class to define a 2D space and
 - the trigger of touching a space boundary (trigger method)
 - what to do when boundary is touched (apply method)

Usage:

b = boundary(width,height)

if b.trigger((x1,y1)):
    (x2,y2) = b.apply((x1,y1)
'''

from turtle import Vec2D

class RectangularBoundary(object):
    
    def __init__(self,width,height):
        self.width = width
        self.height = height
    
    def trigger(self,(x,y)):
        return abs(x) > self.width/2 or abs(y) > self.height/2
        
    def apply(self,(x,y)):
        return  Vec2D ( (x + self.width /2) % self.width  - self.width/2,  
                        (y + self.height/2) % self.height - self.height/2 
                      )
        
        
class CircularBoundary(object):
    
    def __init__(self,radius):
        self.radius = radius

    def trigger(self,pos):
        return abs(pos) > self.radius
        
    def apply(self,(x,y)):
        return None