import os
import maya.cmds as cmds
import rdui.rdui as rdui
reload(rdui)

#Define if the user is using Mac or PC
if platform.system() == 'Windows':
    os.environ["RDODJO_DATA"] = 'C:/Users/arklein/Documents/GitHub/Python_101_S1_2016/'
else:
    os.environ["RDODJO_DATA"] = '/Users/AK_Projects/Python101/Python_101_S1_2016'


print "Startup with rdui"

