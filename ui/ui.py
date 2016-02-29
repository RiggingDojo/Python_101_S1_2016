import maya.cmds as cmds

print "This is UI"

def rigarm(*args):
	print "Rig_Arm. This is a test. Files in Python_101_S1_2016 folder"


def testbutton(*args):
	cmds.circle( n='ikh_ctrl_arm', normal=(1, 0, 0), radius=1.5)
	cmds.group('ikh_ctrl_arm', n='grp_ikh_ctrl_arm', world=True)


# The UI class
class RDojo_UI:

   def __init__(self, *args):
       print 'In RDojo_UI'


mymenu = cmds.menu( 'RDojo_Menu', label='RD Menu', to=True, p='MayaWindow')
cmds.menuItem(label='Rig_Arm', p=mymenu, command=rigarm)
cmds.menuItem(label='Circle Test', p=mymenu, command=testbutton)



