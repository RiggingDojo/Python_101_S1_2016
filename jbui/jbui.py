import maya.cmds as cmds
import rig.rig_arm_w5 as rig

def rigarm(*args):
	rig.rigArm()	
	
myMenu = cmds.menu('RDojo_Menu', label='RDMenu', to=True, p='MayaWindow')
cmds.menuItem(label='Rig Arm', p=myMenu, command=rigarm)
