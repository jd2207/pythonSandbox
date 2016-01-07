
class SimpleModel:
  def __init__(self):
    print 'created a new model'
    self.value = 0
    self.name = ''
  
  def modify(self, **kwargs):
    modified = False
    print 'model being modified. Input is', kwargs
    for key in kwargs:
      if key == 'value':
        self.value = kwargs[key]; modified = True
         
      if key == 'name':
        self.name = kwargs[key]; modified = True
    
    return modified 
      

if __name__=="__main__":
  m = SimpleModel()
  print '"'+m.name+'"', m.value 
  m.modify(value=5)
  print '"'+m.name+'"', m.value 
  m.modify(name='hello')
  print '"'+m.name+'"', m.value 

    