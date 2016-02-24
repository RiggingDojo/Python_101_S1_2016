import maya.cmds as cmds

print "This is UI"

def rigarm(*args):
	print "Rig_Arm test again"


mymenu = cmds.menu( 'RDojo_Menu', label='RD Menu', to=True, p='MayaWindow')
cmds.menuItem(label='Rig_Arm', p=mymenu, command=rigarm)



