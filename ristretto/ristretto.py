#!/usr/bin/env python
#Boa:App:BoaApp
# -*- coding: utf-8 -*-

# In order to handle Unicode, string must be prefixed by u'

import wx, os, sys

set_base_path = True
if hasattr(sys, 'frozen'):
    fullexepath = os.path.join(os.getcwd(), sys.argv[0])
    if os.path.isfile(fullexepath):
        ristrettopath = fullexepath
    else:
        ristrettopath = sys.argv[0]
    if 'ICERA_SW_PATH' in os.environ:
        set_base_path = False
    os.chdir(os.path.dirname(ristrettopath))
else:
    ristrettopath = __file__

if set_base_path:
    base_path = os.path.abspath(os.path.join(os.path.dirname(ristrettopath), os.path.pardir))
    if os.path.join(base_path, 'modem-utils') not in sys.path:
        sys.path.append(os.path.join(base_path, 'modem-utils'))
    os.environ['ICERA_SW_PATH'] = base_path
    
import RistrettoFrame

modules ={'Frame': [1, 'Main frame of Application', u'RistrettoFrame.py'],
 'Ristretto User Guide': [0, '', u'UserGuideFrame.py'],
}

class BoaApp(wx.App):
    def OnInit(self):
        self.main = RistrettoFrame.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)

        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
