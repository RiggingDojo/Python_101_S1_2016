import os
import sys
import maya.cmds as cmds

print ("In User Setup")

sys.path.append('C:/Users/Bears/Documents/GitHub/Python_101_S1_2016')
cmds.evalDeferred('import startup')
