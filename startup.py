import maya.cmds as cmds
import os

#print ("Hello Its Me")
print "Startup"
'''
# Change the current time unit to ntsc
cmds.currentUnit( time='ntsc' )

# Change the current linear unit to inches
cmds.currentUnit( linear='cm' )
'''
# set a system path to data files. WE can do this with the os module
os.environ["RDOJO_DATA"] = 'C:/Users/blam/Documents/GitHub/Python_101_S1_2016/data'

#import  ui from ui folder
import ui.ui as ui
#get rid after finishing development, used for test cases
reload(ui)
ui.RDojo_UI()
