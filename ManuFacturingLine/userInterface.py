'''
   Provides common menu and screen printing 
'''

import sys

# ----------------------------------------------
#  Specialist screen printing functions
# ----------------------------------------------

'''
ESC [ 0 m       # reset all (colors and brightness)
ESC [ 1 m       # bright
ESC [ 2 m       # dim (looks same as normal brightness)
ESC [ 22 m      # normal brightness

# FOREGROUND:
ESC [ 30 m      # black
ESC [ 31 m      # red
ESC [ 32 m      # green
ESC [ 33 m      # yellow
ESC [ 34 m      # blue
ESC [ 35 m      # magenta
ESC [ 36 m      # cyan
ESC [ 37 m      # white
ESC [ 39 m      # reset

# BACKGROUND
ESC [ 40 m      # black
ESC [ 41 m      # red
ESC [ 42 m      # green
ESC [ 43 m      # yellow
ESC [ 44 m      # blue
ESC [ 45 m      # magenta
ESC [ 46 m      # cyan
ESC [ 47 m      # white
ESC [ 49 m      # reset

# cursor positioning
ESC [ y;x H     # position cursor at x across, y down

# clear the screen
ESC [ mode J    # clear the screen. Only mode 2 (clear entire screen)
                # is supported. It should be easy to add other modes,
                # let me know if that would be useful.
'''

class screen:
  ECHO_STDOUT_ALL = True

  HEADER = '\033[35m'
  BLUE = '\033[34m'
  GREEN = '\033[32m'
  WARNING = '\033[33m'
  CYAN = '\033[36m'
  YELLOW = '\033[33m'
  RED = '\033[31m'
  ENDC = '\033[0m'
  DEFAULT = '\033[22m'    
  CLEAR = chr(27) + "[2J"
    
  OK = GREEN + "OK" + ENDC
  NOK = RED + "NOK" + ENDC
  PASS = GREEN + "!!!!PASS!!!!" + ENDC
  FAIL = RED + "!!!!FAIL!!!!" + ENDC

  def printText (self, text):
    print text
    
  def printColor (self, text, color):
    print color + text + self.ENDC
        
  def clear (self):
    print self.CLEAR
    
  def printOK( self, text ):
    self.printColor(text,self.GREEN)

  def printNOK( self, text ):
    self.printColor(text,self.RED)

  def printWarn( self, text ):
    self.printColor('WARNING: '+text,self.RED)

  def printUser( self, text ): # Used to indicate user actions
    self.printColor(text,self.YELLOW)

  def prompt( self, text ): # Uses color input to prompt user for action
    return raw_input( self.YELLOW + text + self.ENDC )

  def promptYN (self, text, yes=False):
    a = None
    if yes:
      text += ' [Y,n]'
    else:
      text += ' [y,N]'
        
    while (True):
      a = self.prompt(text)
      if a in ['y','n','Y','N','']: break

    if a in ['y', 'Y'] or (a == '' and yes): 
      return True 
    else:
      return False
        
                
# ---------------------------------------------------------------
# For menu selection
# ---------------------------------------------------------------

class menu (list):
# This menu class is a specialist List for presenting and selecting 
# from arbitrary items which have an 'id' and an optional 'description'

  def __init__ (self, screen, title, name):
    self.screen = screen
    self.header = title
    self.name = name
    self.all = False
        
  def allowAll(self, all=True):
    self.all = all
           
  def append(self, id, description, item):
    super(menu,self).append ({ 'id' : id, 
                               'description' : description,
                               'item' : item
                             })
        
  def appendFromDict(self, menuDict):
    for id in menuDict.iterkeys():
      self.append( id, menuDict[ id ] [ 'description' ], menuDict [ id] [ 'subItem' ] )
        
    
  def printSelection(self, index):
    self.screen.printText (" '%s' selected\n" % (self[index]['id'] ))


  def printMenu(self):  # Show all menu choices (including "all" if all=True)
    format1 = "  [ %s ] %-20s -- %s"
    format2 = "  [ %s ] %-20s"
        
    if self.all: 
      i = 0 
      self.screen.printText ( (format1+'\n') % ( str(i), 'ALL', 'Execute all'))
      
    i = 1
    for item in self:
      id = item [ 'id' ]
      desc = item [ 'description' ]
      if desc == '':
        self.screen.printText ( format2 % ( i, id ))
      else:
        self.screen.printText ( format1 % ( i, id, desc))
        
      i += 1
           
  def select (self):   # returns the chosen menu item
    while True:
      self.screen.printText(self.header+'\n')
      self.screen.printUser( "Select "+self.name+":\n"  )
      self.printMenu()
            
      choices = []
      if self.all: choices.append('0') 
      for i in range(len(self)):
        choices.append(str(i+1))
            
      sel = self.screen.prompt( '\nEnter: '+ str(choices) + " or 'q' to quit" )

      if sel.lower() == 'q':
        sys.exit()

      if sel.isdigit():
        sel = int( sel )
                
        if sel == 0:
          if self.all == True:
            return self             # return the list of ALL menu items
                
        if sel > 0 and sel < len(self) + 1:
          self.printSelection( sel - 1)
          return self[ sel - 1 ]      # return a single selected item
        else:
          self.screen.printWarn( "Selection '%s' is invalid\n" % sel )
      else:
        self.screen.printWarn( "Selection '%s' is invalid\n" % sel )     
            
            
            