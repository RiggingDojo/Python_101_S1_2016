import maya.cmds as cmds

print ("Hello Its Me")

# Change the current time unit to ntsc
cmds.currentUnit( time='ntsc' )

# Change the current linear unit to inches
cmds.currentUnit( linear='cm' )

#import  ui from ui folder
import ui.ui as ui
#get rid after finishing development, used for test cases
reload(ui)
