import os
import sys
import maya.cmds as cmds

print "In user setup"

sys.path.append('Users/BackboneLabs/Documents/Python_101_S1_2016')
cmds.evalDeferred('import startup')