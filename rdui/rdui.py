'''
Create menuItem functions here and call them after assembling the menu
at the bottom. 
'''


import maya.cmds as cmds
import rig.rig_arm as rig

print "This is RDUI\n"

arm_obj = rig.Rig_Arm()



'''
# The UI class
class RDojo_UI:

   def __init__(self, *args):
        print 'In RDojo_UI'
'''


##############
# Menu Items #
##############


#Creates an arm rig and controls by performing all 
def rig_arm_full_menu(*args):
    arm_obj.rig_arm()





#define which arm joints will be built and where they will be placed. 
def define_arm_joints_menu(*args):
    arm_obj.define_arm_joints(rig.jnt_arm_info, rig.jnt_prefix, rig.jnt_dict)


    




#Create all joints
def create_joints_menu(*args):
    arm_obj.create_joints(rig.jnt_dict, rig.jnt_rot)
    





# ---- IK Controls ----
# creates ik controls to drive the rotation values of the ik rig joints
def make_ik_controls_menu(*args):
    arm_obj.make_ik_controls(rig.jnt_arm_info, rig.jnt_dict, rig.jnt_rot)







# ---- FK Controls ----
# creates fk controls to drive the rotation values of the fk rig joints
def make_fk_controls_menu(*args):
    arm_obj.make_fk_controls(rig.jnt_arm_info, rig.jnt_dict, rig.jnt_rot)






# ---- Blend Nodes ----
# Use the color blend attribute to connect ik and fk rotational values to drive rig joints
def connect_blend_nodes_menu(*args):
    arm_obj.connect_blend_nodes(rig.jnt_arm_info, rig.jnt_dict)






#Create menu and menu items for creating arm rig.
if 'RDojo_Menu' not in (cmds.window('MayaWindow', q=True, ma=True)):
    rdojo_menu = cmds.menu( 'RDojo_Menu', label='RD Menu', to=True, p='MayaWindow')
    cmds.menuItem(label='Rig Arm Full', p=rdojo_menu, command=rig_arm_full_menu)
    cmds.menuItem(p=rdojo_menu, divider=True)
    cmds.menuItem(label='Define Arm Joints', p=rdojo_menu, command=define_arm_joints_menu)
    cmds.menuItem(label='Create Arm Joints', p=rdojo_menu, command=create_joints_menu)
    cmds.menuItem(label='Make IK Controls', p=rdojo_menu, command=make_ik_controls_menu)
    cmds.menuItem(label='Make FK Controls', p=rdojo_menu, command=make_fk_controls_menu)
    cmds.menuItem(label='Connect Blend Nodes', p=rdojo_menu, command=connect_blend_nodes_menu)
else:
    print('menu already exists')




