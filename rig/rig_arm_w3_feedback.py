""" It looks like you are off to a good start here.  
You seem to be overcomplicating a few things, so try to go back and 
simplify.  I like that you are using dictionaries.  Try to hone
in on the information you realy need to create joints, groups, controls
and so on.  Enter all that information into a dictionary and build from there. 
For example, you have names['joints'].  All the name information you need 
to name things is in there. """
# Example
# assign names for the dictionary items
names = {'translation': ['.tx', '.ty', '.tz'],
         'rotation': ['.rx', '.ry', '.rz'],
         'scale': ['.sx', '.sy', '.sz'],
         'name': ['ik_', 'fk_', 'rig_'],
         'group':'grp_',
         'control': 'ctrl_',
         'jointSuffix':'_jnt',
         'pv': 'polev_',
         'joints': ['shoulder', 'elbow', 'wrist', 'wristEnd'],
         'pos': [[-0.2, 0.0, 8.5], [-4.0, 0.0, 0.04], [0.15, 0, -4.7], [-0.07, 0, -7.4]],
         }

# You can make a new dictionary to store all of your newly created nodes.
rig_info = {}
for each in names['name']:
    cmds.select(d=True)
    for i in range(len(names['joints'])):
        newdictkey = each + names['jointSuffix']
        rig_info[newdictkey] = cmds.joint(n=each + names['jointSuffix'] + names['joints'][i], p=names['pos'][i])
print rig_info







import maya.cmds as cmds

# CREATE TEMP LISTS
tmp_lst = []
add_jnt = []

# assign names for the dictionary items
names = {'translation': ['.tx', '.ty', '.tz'],
         'rotation': ['.rx', '.ry', '.rz'],
         'scale': ['.sx', '.sy', '.sz'],
         'name': ['ik_', 'fk_', 'rig_'],
         'group':'grp_',
         'control': 'ctrl_',
         'jointSuffix':'_jnt',
         'pv': 'polev_',
         'joints': ['shoulder', 'elbow', 'wrist', 'wristEnd'],
         'pos': [[-0.2, 0.0, 8.5], [-4.0, 0.0, 0.04], [0.15, 0, -4.7], [-0.07, 0, -7.4]],
         }

posA = names['pos'][0]
posB = names['pos'][1]
posC = names['pos'][2]
posD = names['pos'][3]

# JOINT INFO

joint_names = [[names['joints'][0] + names['jointSuffix'],posA],
              [names['joints'][1] + names['jointSuffix'],posB],
              [names['joints'][2] + names['jointSuffix'],posC], 
              [names['joints'][3] + names['jointSuffix'],posD]]


# print joint_names[0][1]

# JOINT CHAINS
joint_chains = (names['name'][0],
                names['name'][1],
                names['name'][2])


# MAKE FULL JOINT DICTIONARY
joint_dict = {}
  
for value in joint_chains:
    for i in range(len(joint_names[0][1])):
        new_name = value + joint_names[0][0]
        tmp_lst.append([new_name])
        
    joint_dict[value] = tmp_lst
    
for b in range(len(tmp_lst)):
    """ When you use for b in range(len(tmp_lst)), b is = to an index number. """
    # TypeError: unsupported operand type(s) for +: 'int' and 'list' #
    print b
    print tmp_lst[i]
    #you can print the data type of a variable
    print type(b) #<type 'int'>
    #new_nameb = str(b) + tmp_lst[i]
    # You probably meant to use tpm_list[b]

    new_nameb = str(b) + tmp_lst[b][0]
    tmp_lst.append([new_name])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

grp_ctrl_dict = {}
name_prefix = ('grp_ctrl_ikj_', 'grp_ctrl_fkj_')
for p in name_prefix:
    tmpgrp_lst = []
    #for i in range(len(joint_info[0:3][0][0])):
    for i in range(len(joint_info[0:3])):
        print i
        #   File "<maya console>", line 73, in <module>
        # IndexError: list index out of range #
        print joint_info
        new_name = p + joint_info[i][0]
        print new_name
        tmpgrp_lst.append([new_name, joint_info[i][1]])
     
    grp_ctrl_dict[p] = tmpgrp_lst
# create the groups from the ctrl_grp_dict  
# NameError: name 'x' is not defined # 
""" It looks like you are defining group names above, so why not use those?"""
print grp_ctrl_dict 
cmds.group( em=True, name="grp_ctrl_" + str(x))

# Joints
joint_info = [['shoulder_jnt', [-0.2, 0.0, 8.5]], ['elbow_jnt', [-4.0, 0.0, 0.04]], ['wrist_jnt', [0.15, 0, -4.7]], ['wristEnd_jnt', [-0.07, 0, -7.4]]]
joint_dict = {}

name_prefix = ('ikj_', 'fkj_', 'rigj_')
for p in name_prefix:
    tmpjnt_lst = []
    for i in range(len(joint_info)):
        new_name = p + joint_info[i][0]
        print new_name
        tmpjnt_lst.append([new_name, joint_info[i][1]])
     
    joint_dict[p] = tmpjnt_lst
     
print joint_info
# Controller objects for 3 fk joints and one for ik wrist joint

# get ws xforms for 

# set wrist end joints to 360 for ik, fk, rig
cmds.setAttr( 'ikj_wristEnd_jnt.jointOrientY', 360)

# Create all joints
for key, value in joint_dict.iteritems():
    for i in range(len(value)):
        cmds.joint(n =value[i][0], p =value[i][1])
 
    cmds.select(d = True)

# Loop through joints and Orient to xyz
for key, value in joint_dict.iteritems():
     
    for i in range(len(value)):
        joint_name = value[i][0]
        print joint_name
        joint_pos = value[i][1]
        print joint_pos
        cmds.joint( (joint_name), edit=True, zso=True, oj='xyz', sao='yup')
     
    cmds.select(d = True)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Get elbow xform
ikpos = cmds.xform('ikj_elbow_jnt', query=True, translation=True, worldSpace=True)
# Move ikpos x -2 in x
k = [ -2, 0, 0] 
zipped = [sum(i) for i in zip(ikpos,k)]
ikpos = zipped
cmds.spaceLocator( n='ik_poleVector')
cmds.xform('ik_poleVector', ws=True, t=(ikpos))
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# IK RIG
# Create Ik Handle
cmds.ikHandle( name="ikh_arm", startJoint=joint_dict['ikj_'][0][0], endEffector=joint_dict['ikj_'][2][0], solver="ikRPsolver", priority=2, weight=1 )
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Create the ik Controller
# Get ws position of wrist joint
'''
pos = cmds.xform("ikj_wrist_jnt", query=True, translation=True, worldSpace=True)
'''
# Create group
cmds.group( em=True, name="grp_ctrl_ikjWrist" )

# Create a circle control object
cmds.circle( name="ctrl_ikWrist", normal=(0, 0, 1), center=(0, 0, 0), sweep=360, radius=2 )

# Delete history on circle
cmds.delete( 'ctrl_ikWrist', constructionHistory=True )

# Parent the control to the group
cmds.parent("ctrl_ikWrist", "grp_ctrl_ikWrist")
rot = cmds.xform('ik_wrist_jnt', q=True, ro=True, ws=True)
cmds.xform('grp_ctrl_ikWrist', ro=rot, ws=True)
cmds.xform( r=True, ro=(0, 90, 0) )

# Move the group to the joint
cmds.xform("grp_ctrl_ikWrist", translation=pos, a=True)

# Parent ikh to ctrl
cmds.parent("ikh_arm", "ctrl_ikWrist")

# Orient constraint ctrl to joint
cmds.orientConstraint( 'ctrl_ikWrist', 'ik_wrist_jnt', mo = True)

# Attach pole vector to IK
cmds.poleVectorConstraint( 'ik_poleVector', 'ikh_arm' )

# Lock ctrl_ikWrist scale
cmds.setAttr( 'ctrl_ikWrist.sx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_ikWrist.sy', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_ikWrist.sz', edit=True,  lock=True, keyable=False, channelBox=False )

# Deselect
cmds.select(d=True)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create Fk Rig
# Create fk Control
# Store the name of the fkjoints in list
fkjointNames = ["Fk_shoulder", "Fk_elbow", "Fk_wrist"]

# Store the grp control in list
fkgrpjointNames = ["grp_ctrl_Fk_shoulder", "grp_ctrl_Fk_elbow", "grp_ctrl_Fk_wrist"]

# Create an empty group named by the joint
""" Empty loop causes an error """
#for x in fkjointNames:


# Create a circle for each control object
for y in fkjointNames:
    cmds.circle( name="ctrl_" + str(y), normal=(0, 0, 1), center=(0, 0, 0), sweep=360, radius=2 )

# Parent the control to the control group
cmds.parent("ctrl_Fk_shoulder", "grp_ctrl_Fk_shoulder")
cmds.parent("ctrl_Fk_elbow", "grp_ctrl_Fk_elbow")
cmds.parent("ctrl_Fk_wrist", "grp_ctrl_Fk_wrist")

# Parent the control group to the joint
cmds.parent("grp_ctrl_Fk_shoulder", "Fk_shoulder_jnt")
cmds.parent("grp_ctrl_Fk_elbow", "Fk_elbow_jnt")
cmds.parent("grp_ctrl_Fk_wrist", "Fk_wrist_jnt")

# Zero xforms on jointNames
for w in fkgrpjointNames:
    cmds.setAttr( w + ".translateX", 0)
    cmds.setAttr( w + ".translateY", 0)
    cmds.setAttr( w + ".translateZ", 0)
    cmds.setAttr( w + ".rotateX", 0)
    cmds.setAttr( w + ".rotateY", 90)
    cmds.setAttr( w + ".rotateZ", 0)


# freeze xforms
cmds.select("grp_ctrl_Fk_shoulder", "grp_ctrl_Fk_elbow", "grp_ctrl_Fk_wrist")
cmds.makeIdentity( apply=True, translate=1, rotate=1, scale=1, normal=0, preserveNormals=1)


# Unparent control group from joint
for item in fkgrpjointNames:
    cmds.parent( item, w=True)

# Parent ctrl
cmds.parent("grp_ctrl_Fk_wrist", "ctrl_Fk_elbow")
cmds.parent("grp_ctrl_Fk_elbow", "ctrl_Fk_shoulder")

# Connect rotation xform of ctrl to the joint
cmds.connectAttr("ctrl_Fk_shoulder.rotate", "Fk_shoulder_jnt.rotate", force=True)
cmds.connectAttr("ctrl_Fk_elbow.rotate", "Fk_elbow_jnt.rotate", force=True)
cmds.connectAttr("ctrl_Fk_wrist.rotate", "Fk_wrist_jnt.rotate", force=True)

# Lock fk ctrl xforms




# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create blend ctrl on rig arm
# Get ws position of wrist end joint
pos = cmds.xform('rig_wristEnd_jnt', q=True, t=True, ws=True)

# Create an empty group
cmds.group( em=True, name='grp_switch_ikfk' )

# Orient grp to joint
rot = cmds.xform('rig_wristEnd_jnt', q=True, ro=True, ws=True)
cmds.xform('grp_switch_ikfk', ro=rot, ws=True)

# Create circle control object
cmds.circle( n='switch_ikfk', center=(0, 0, 0), radius=2, normal=(1, 0, 0) )

# Delete history
cmds.delete( 'switch_ikfk', constructionHistory=True )

# Parent ctrl to group and group to wrist end joint
cmds.parent('switch_ikfk', 'grp_switch_ikfk')
cmds.setAttr( "switch_ikfk.rotateY", 0 )
cmds.setAttr( "switch_ikfk.rotateZ", 90 )
# Move the group to the joint
cmds.xform('grp_switch_ikfk', t=pos, ws=True)
cmds.parent('grp_switch_ikfk', 'rig_wristEnd_jnt')

# Lock and hide ctrl attributes
cmds.setAttr( 'switch_ikfk.tx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'switch_ikfk.ty', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'switch_ikfk.tz', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'switch_ikfk.rx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'switch_ikfk.ry', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'switch_ikfk.rz', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'switch_ikfk.sx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'switch_ikfk.sy', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'switch_ikfk.sz', edit=True,  lock=True, keyable=False, channelBox=False )

# Create blend attribute
cmds.select( d=True )
cmds.select( 'switch_ikfk' )
cmds.addAttr( 'switch_ikfk', longName='IKFKBlend', attributeType='double', min=0, max=1, defaultValue=1 )
cmds.setAttr( 'switch_ikfk.IKFKBlend', edit=True, keyable=True )
cmds.setAttr( 'switch_ikfk.IKFKBlend', 0 )

# Create 3 blend color nodes
cmds.shadingNode( 'blendColors', name="blend_shoulder", asUtility=True )
cmds.shadingNode( 'blendColors', name="blend_elbow", asUtility=True )
cmds.shadingNode( 'blendColors', name="blend_wrist", asUtility=True )

# Connect blends to rig joints
cmds.connectAttr( 'blend_shoulder.outputR', 'rig_shoulder_jnt.rotateX')
cmds.connectAttr( 'blend_shoulder.outputG', 'rig_shoulder_jnt.rotateY')
cmds.connectAttr( 'blend_shoulder.outputB', 'rig_shoulder_jnt.rotateZ')

cmds.connectAttr( 'blend_elbow.outputR', 'rig_elbow_jnt.rotateX')
cmds.connectAttr( 'blend_elbow.outputG', 'rig_elbow_jnt.rotateY')
cmds.connectAttr( 'blend_elbow.outputB', 'rig_elbow_jnt.rotateZ')

cmds.connectAttr( 'blend_wrist.outputR', 'rig_wrist_jnt.rotateX')
cmds.connectAttr( 'blend_wrist.outputG', 'rig_wrist_jnt.rotateY')
cmds.connectAttr( 'blend_wrist.outputB', 'rig_wrist_jnt.rotateZ')

# Connect ik and fk to drive the blender nodes
cmds.connectAttr( 'ik_shoulder_jnt.rotateX', 'blend_shoulder.color1R')
cmds.connectAttr( 'ik_shoulder_jnt.rotateY', 'blend_shoulder.color1G')
cmds.connectAttr( 'ik_shoulder_jnt.rotateZ', 'blend_shoulder.color1B')
cmds.connectAttr( 'ik_elbow_jnt.rotateX', 'blend_elbow.color1R')
cmds.connectAttr( 'ik_elbow_jnt.rotateY', 'blend_elbow.color1G')
cmds.connectAttr( 'ik_elbow_jnt.rotateZ', 'blend_elbow.color1B')
cmds.connectAttr( 'ik_wrist_jnt.rotateX', 'blend_wrist.color1R')
cmds.connectAttr( 'ik_wrist_jnt.rotateY', 'blend_wrist.color1G')
cmds.connectAttr( 'ik_wrist_jnt.rotateZ', 'blend_wrist.color1B')


cmds.connectAttr( 'Fk_shoulder_jnt.rotateX', 'blend_shoulder.color2R')
cmds.connectAttr( 'Fk_shoulder_jnt.rotateY', 'blend_shoulder.color2G')
cmds.connectAttr( 'Fk_shoulder_jnt.rotateZ', 'blend_shoulder.color2B')
cmds.connectAttr( 'Fk_elbow_jnt.rotateX', 'blend_elbow.color2R')
cmds.connectAttr( 'Fk_elbow_jnt.rotateY', 'blend_elbow.color2G')
cmds.connectAttr( 'Fk_elbow_jnt.rotateZ', 'blend_elbow.color2B')
cmds.connectAttr( 'Fk_wrist_jnt.rotateX', 'blend_wrist.color2R')
cmds.connectAttr( 'Fk_wrist_jnt.rotateY', 'blend_wrist.color2G')
cmds.connectAttr( 'Fk_wrist_jnt.rotateZ', 'blend_wrist.color2B')

cmds.connectAttr( 'switch_ikfk.IKFKBlend', 'blend_shoulder.blender')
cmds.connectAttr( 'switch_ikfk.IKFKBlend', 'blend_elbow.blender')
cmds.connectAttr( 'switch_ikfk.IKFKBlend', 'blend_wrist.blender')
