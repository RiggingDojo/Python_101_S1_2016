import maya.cmds as cmds

print ("UI")

def rigarm(*args):
	print "Rig_Arm"
	import rig.rig_arm_classes as rig_arm
	reload(rig_arm)
	#create instance for class
	rig_arm = rig_arm.Rig_Arm()
	rig_arm.rig_arm



#Create menu on the Main Maya window
mymenu  = cmds.menu('RDojo_Menu', label='RDMenu', to=True, p='MayaWindow')
cmds.menuItem(label='Rig_Arm', p=mymenu, command=create_jnts)


