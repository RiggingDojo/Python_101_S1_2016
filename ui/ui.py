import maya.cmds as cmds
import os
from functools import partial
import system.utils as utils
reload(utils)

# The UI class
class RDojo_UI:

    def __init__(self, *args):
        print 'In RDojo_UI'
        mi = cmds.window('MayaWindow', ma=True, q=True)
        for m in mi:
            if m == 'RDojo_Menu':
                cmds.deleteUI('RDojo_Menu', m=True)

        mymenu = cmds.menu('RDojo_Menu', label='RDMenu', to=True, p='MayaWindow')
        cmds.menuItem(label='Rig Arm', parent=mymenu, command=self.ui)

        """ Create a dictionary to store UI elements.
        This will allow us to access these elements later. """
        self.UIElements = {}

        # This dictionary will store all of the available rigging modules.
        self.rigmodlst = []
        rigcontents = os.listdir(os.environ["RDOJO_DATA"]+ 'rig/')
        for mod in rigcontents:
            if '.pyc' not in mod or 'init' not in mod:
                self.rigmodlst.append(mod)

        # An empty list to store information collected from the ui.
        self.uiinfo = []

    def ui(self, *args):
        """ Check to see if the UI exists """
        windowName = "Window"
        if cmds.window(windowName, exists=True):
            cmds.deleteUI(windowName)
        """ Define width and height for buttons and windows"""    
        windowWidth = 240
        windowHeight = 120
        buttonWidth = 55
        buttonHeight = 22

        self.UIElements["window"] = cmds.window(windowName, width=windowWidth, height=windowHeight, title="RDojo_UI", sizeable=True)

        self.UIElements["mainColLayout"] = cmds.columnLayout( adjustableColumn=True )
        self.UIElements["guiFrameLayout1"] = cmds.frameLayout( label='rigging', borderStyle='in', p=self.UIElements["mainColLayout"] )
        self.UIElements["guiFlowLayout1"] = cmds.flowLayout(v=False, width=windowWidth, height=windowHeight/2, wr=False, bgc=[0.2, 0.2, 0.2], p=self.UIElements["guiFrameLayout1"])
        
        cmds.separator(w=10, hr=True, st='none', p=self.UIElements["guiFlowLayout1"])
        self.UIElements["rigMenu"] = cmds.optionMenu('Rig_Install', label='Rig', p= self.UIElements["guiFlowLayout1"]) 
        
        # Dynamically make a menu item for each rigging module.
        for mod in self.rigmodlst:
            itemname = mod.replace('.py', '')    
            #cmds.menuItem(label=itemname, p=self.UIElements["rigMenu"], c=partial(self.rigmod, itemname))

 
  
