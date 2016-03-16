import os
import maya.cmds as cmds
import platform


print "Startup with rdui"


#Define if the user is using Mac or PC
#Set a system path to the data files. 
if platform.system() == 'Windows':
    os.environ["RD_DATA"] = 'C:/Users/arklein/Documents/GitHub/Python_101_S1_2016/data/'
else:
    os.environ["RD_DATA"] = '/Users/AK_Projects/Python101/Python_101_S1_2016/data/'



import rdui.rdui as rdui
reload(rdui)
rdui.RDojo_UI()

