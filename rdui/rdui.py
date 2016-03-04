'''
Create menuItem functions here and call them after assembling the menu
at the bottom. 

These need to be imported into this file. 

In rd_rig_arm.py, the functions are actually called. 

'''


import maya.cmds as cmds
import rig.rd_rig_arm as rig
reload(rig)

print "This is RDUI"



#define which arm joints will be built and where they will be placed.
jnt_arm_info = [['shoulder', [-8.0, 0.0, 0.0]], ['elbow', [0.0, 0.0, -2.0]], 
       ['wrist', [8.0, 0.0, 0.0]], ['wristEnd',[10.0, 0.0, 0.0]]]
jnt_prefix = ['ikj_', 'fkj_', 'rigj_']
jnt_dict = {}
jnt_rot = []




# The UI class
class RDojo_UI:

   def __init__(self, *args):
        print 'In RDojo_UI'




##############
# Menu Items #
##############


#Creates an arm rig and controls by performing all 
def rig_arm_full_menu(*args):
    rig.define_arm_joints(jnt_arm_info, jnt_prefix, jnt_dict)
    rig.create_joints(jnt_dict, jnt_rot)
    rig.create_joints(jnt_dict, jnt_rot)
    rig.make_ik_controls(jnt_arm_info, jnt_dict, jnt_rot)
    rig.make_fk_controls(jnt_arm_info, jnt_dict, jnt_rot)
    rig.connect_blend_nodes(jnt_arm_info, jnt_dict)





#define which arm joints will be built and where they will be placed. 
def define_arm_joints_menu(*args):
    rig.define_arm_joints(jnt_arm_info, jnt_prefix, jnt_dict)
    print('from rdui: ', jnt_dict)


    




#Create all joints
def create_joints_menu(*args):
    rig.create_joints(jnt_dict, jnt_rot)
    print('from rdui: ', jnt_rot)
    





# ---- IK Controls ----
# creates ik controls to drive the rotation values of the ik rig joints
def make_ik_controls_menu(*args):
    rig.make_ik_controls(jnt_arm_info, jnt_dict, jnt_rot)







# ---- FK Controls ----
# creates fk controls to drive the rotation values of the fk rig joints
def make_fk_controls_menu(*args):
    rig.make_fk_controls(jnt_arm_info, jnt_dict, jnt_rot)






# ---- Blend Nodes ----
# Use the color blend attribute to connect ik and fk rotational values to drive rig joints
def connect_blend_nodes_menu(*args):
    rig.connect_blend_nodes(jnt_arm_info, jnt_dict)






#Create menu and menu items for creating arm rig.
rdojo_menu = cmds.menu( 'RDojo_Menu', label='RD Menu', to=True, p='MayaWindow')
cmds.menuItem(label='Rig Arm Full', p=rdojo_menu, command=rig_arm_full_menu)
cmds.menuItem(p=rdojo_menu, divider=True)
cmds.menuItem(label='Define Arm Joints', p=rdojo_menu, command=define_arm_joints_menu)
cmds.menuItem(label='Create Arm Joints', p=rdojo_menu, command=create_joints_menu)
cmds.menuItem(label='Make IK Controls', p=rdojo_menu, command=make_ik_controls_menu)
cmds.menuItem(label='Make FK Controls', p=rdojo_menu, command=make_fk_controls_menu)
cmds.menuItem(label='Connect Blend Nodes', p=rdojo_menu, command=connect_blend_nodes_menu)




