""" Defines abstract and child cells. 
    Each cell may be a member of a parent object (e.g. CellGrid) but in any case must have a defined identity (row, column)
    Each cell class must define a method makeDescendant() which creates and returns a new cell object 
"""

import random

class AbstractCell(object):
  """ Parent class of all Cell classes """
  
  ROW    = 0
  COLUMN = 1
  
  def __init__(self, identity, parentGrid=None):
    self.parentGrid = parentGrid
    self.identity = identity

  def makeDescendant(self):
    """ Must be overridden by descendant classes """
    pass

  def __str__ (self):
    return 'Cell @ (%i, %i) is a child of %s.' % (self.identity[AbstractCell.ROW], self.identity[AbstractCell.COLUMN], str(self.parentGrid))


class BooleanCell(AbstractCell):
  """ A simple cell that has a boolean state which can be toggled """ 
  
  def __init__(self, identity, parentGrid=None, state=False):
    self.state = state
    super(BooleanCell,self).__init__(identity, parentGrid)

  def toggle(self):
    """ flips the state """
    self.state = not self.state
    
  def makeDescendant(self):
    """ creates a new BooleanCell with a toggled state """
    newState = self.toggle()
    return BooleanCell(self.identity, parentGrid=self.parentGrid, state = newState)  

  def dump(self):
    """ prints a string of the instance """
    return str(self) + ' State =  %i' % self.state


class RandomBooleanCell(BooleanCell):
  """ A boolean cell whose descendant has a random state """
  def makeDescendant(self):
    return RandomBooleanCell(self.identity, parentGrid=self.parentGrid, state = random.randint(0,1))  

'''
class GameOfLifeCell(BooleanCell):
  
  def __init__(self, identity, parentGrid, state=False):          # unlike BooleanCell, GameOfLifeCell must have a parentGrid
    super(GameOfLifeCell,self).__init__(identity, parentGrid, state)
  
  def makeDescendant(self):
    
    g = self.parentGrid
    
    # Calculate the sum of the neighbors
    n = g.neighbors(self.identity[AbstractCell.ROW], self.identity[AbstractCell.COLUMN])
    s = 0
    for i in n:
      m = g[ i[0] ] [ i[1] ].state
      s += m
    
    # Conway's rules: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules
    newState = self.state
    if self.state:                          # if alive
      if s > 3 or s < 2:
        newState = not newState             # kill the alive cell
    else:                                   # if dead
      if s == 3:
        newState = not newState             # cell comes alive
        
    return GameOfLifeCell(self.identity, parentGrid=self.parentGrid, state=newState)  
''' 
      
      
if __name__ == '__main__':

  print 'Create a default boolean cell -----------------------------------------------'  
  a = BooleanCell( (1,1) )
  a.dump()
  
  '''

  Need to test that abstratCell cannot be instantiated
  
  print 'State toggled'
  a.toggle()
  a.dump()
  
  print 'Create a chain of descendants of the boolean cell  -------------------------------------------'
  for i in range(5):
    a = a.makeDescendant() 
    a.dump()

  print 'Create a chain of descendants of random boolean cell -----------------------------------------------'  
  r = RandomBooleanCell( (5,5) )
  for i in range(5):
    r = r.makeDescendant() 
    r.dump()
  '''