#! /usr/bin/python3.3
"""       turtle-example-suite:

            tdemo_yinyang.py

Another drawing suitable as a beginner's
programming example.

The small circles are drawn by the circle
command.

"""

class yingyang:
    
    def __init__(self,radius):
        self.radius = radius
           
    def render(self,turtle,colors,width=3):    
        self.turtle = turtle
        self.turtle.width = width
        
        r = self.turtle.pos()
        self.halfyy(self.radius,colors[0],colors[1])
        self.turtle.goto(r)
        self.turtle.setheading(180) 
        self.halfyy(self.radius,colors[1],colors[0])
        
    def halfyy(self,radius,color1,color2):
    
# Outer part    
        self.turtle.color(color1, color2)
        self.turtle.begin_fill()
        self.turtle.circle(radius/2., 180)
        self.turtle.circle(radius, 180)
        self.turtle.left(180)
        self.turtle.circle(-radius/2., 180)
        self.turtle.end_fill()

# Move    
        self.turtle.left(90)
        self.turtle.up()
        self.turtle.forward(radius*0.35)
        self.turtle.right(90)
        self.turtle.down()
 
# Inner circle   
        self.turtle.color(color2, color1)
        self.turtle.begin_fill()
        self.turtle.circle(radius*0.15)
        self.turtle.end_fill()
    
# Main 
import turtle

t = turtle.Turtle()
t.reset()
t.ht()
   
yy = yingyang(200)
yy.render(t,['black','white'])
turtle.done()

