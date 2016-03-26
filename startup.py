import maya.cmds as cmds
import os
<<<<<<< HEAD
import system.utils as utils
reload(utils)

print "Startup"

=======

#print ("Hello Its Me")
print "Startup"
'''
>>>>>>> origin/master
# Change the current time unit to ntsc
cmds.currentUnit( time='ntsc' )

# Change the current linear unit to inches
cmds.currentUnit( linear='cm' )
<<<<<<< HEAD

# Set a system path to files.  We can do this with the os module
os.environ["RDOJO_DATA"] = 'C:/Users/Griffy/Documents/GitHub/Python_101_S2_2015/'


import ui.ui as ui
reload(ui)
ui.RDojo_UI()

utils.setupMatchScripts()
=======
'''
# set a system path to data files. WE can do this with the os module
os.environ["RDOJO_DATA"] = 'C:/Users/blam/Documents/GitHub/Python_101_S1_2016/data'

#import  ui from ui folder
import ui.ui as ui
#get rid after finishing development, used for test cases
reload(ui)
ui.RDojo_UI()
>>>>>>> origin/master
