import maya.cmds as cmds

print ("UI")

def create_jnts(*args):
	#print ("Rig_Arm_Is_Cool")
	import rig.rig_arm_functions as rig_arm
	reload(rig_arm)

def rename(*args):
	import rig.rig_arm_rename as rename
	reload(rename)

def orient_jnts(*args):
	import rig.rig_arm_orient as orient_j
	reload(orient_j)


#Create menu on the Main Maya window
mymenu  = cmds.menu('RDojo_Menu', label='RDMenu', to=True, p='MayaWindow')
cmds.menuItem(label='Create_Jnts', p=mymenu, command=create_jnts)
cmds.menuItem(label='Rename_Jnt', p=mymenu, command=rename)
cmds.menuItem(label='Orient_Jnt', p=mymenu, command=orient_jnts)

