
import turtle

class tl(list):
    
    def append(self,x,y):
        t = turtle.Turtle()
        t.ht(); t.pu()
        t.setpos(x,y)
        t.st()
        super(tl,self).append(t)
        
        
    def remove(self,p):
        p.ht()
        p.clear()
        super(tl,self).remove(p)
        p.getscreen().turtles().remove(p)

    def motion(self,steps):
        for i in range(steps):
            for o in self:
                o.setpos( o.pos() + turtle.Vec2D (1,1))

ps = tl()
ps.append(0,0)
ps.append(-20,30)
ps.append(40,60)
ps.append(100,-50)

