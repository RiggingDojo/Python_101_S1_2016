import os
import maya.cmds as cmds
import rdui.rdui as rdui
reload(rdui)

os.environ["RDODJO_DATA"] = '/Users/AK_Projects/Python101/Python_101_S1_2016'

print "Startup with ui"
cmds.currentUnit( time='ntsc')

