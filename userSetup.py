import os
import sys
import maya.cmds as cmds

# Close ports if they were already open under another configuration
try:
    cmds.commandPort(name=":7001", close=True)
except:
    cmds.warning('Could not close port 7001 (maybe it is not opened yet...)')
try:
    cmds.commandPort(name=":7002", close=True)
except:
    cmds.warning('Could not close port 7002 (maybe it is not opened yet...)')
# Open new ports
cmds.commandPort(name=":7001", sourceType="mel")
cmds.commandPort(name=":7002", sourceType="python")
# Append Rig Dojo path
sys.path.append('Users/BackboneLabs/Documents/Python_101_S1_2016')
cmds.evalDeferred('import startup')