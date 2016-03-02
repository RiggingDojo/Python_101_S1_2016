import maya.cmds as cmds

# Create Ik joints
# Create Ik joints variable
jointInfo = (["ik_shoulder_jnt", [-0.2, 0, 8.5]], ["ik_elbow_jnt", [-4.0, 0, 0.04]], ["ik_wrist_jnt", [0.15, 0, -4.7]], ["ik_wristEnd_jnt", [-0.07, 0, -7.4]])
print jointInfo[0][0]
cmds.select(deselect=True)

# Create joints in loop
for item in jointInfo:
    cmds.joint(n=item[0], p=item[1])

# Orient joints
joints = [row[0] for row in jointInfo]
orientJoints = joints[0:3]
for item in orientJoints:
    cmds.joint( (joints), edit=True, zso=True, oj='xyz', sao='yup')
cmds.setAttr( 'ik_wristEnd_jnt.jointOrientY', 360)

# Get elbow xform
ikpos = cmds.xform('ik_elbow_jnt', query=True, translation=True, worldSpace=True)
# Move ikpos x -2 in x
k = [ -2, 0, 0] 
zipped = [sum(i) for i in zip(ikpos,k)]
ikpos = zipped
cmds.spaceLocator( n='ik_poleVector')
cmds.xform('ik_poleVector', ws=True, t=(ikpos))

# Create Ik Rig
# Create Ik Handle
cmds.ikHandle( name="ikh_arm", startJoint="ik_shoulder_jnt", endEffector="ik_wrist_jnt", solver="ikRPsolver", priority=2, weight=1 )

# Create the ik Controller
# Get ws position of wrist joint
pos = cmds.xform("ik_wrist_jnt", query=True, translation=True, worldSpace=True)

# Create group
cmds.group( em=True, name="grp_ctrl_ikWrist" )

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

# Create Fk joints
# Create Fk joints variable
jointInfo = (["Fk_shoulder_jnt", [-0.2, 0, 8.5]], ["Fk_elbow_jnt", [-4.0, 0, 0.04]], ["Fk_wrist_jnt", [0.15, 0, -4.7]], ["Fk_wristEnd_jnt", [-0.07, 0, -7.4]])
cmds.select(deselect=True)

# Create joints in loop
for item in jointInfo:
    cmds.joint(n=item[0], p=item[1])

# Orient joints
joints = [row[0] for row in jointInfo]
orientJoints = joints[0:3]
for item in orientJoints:
    cmds.joint( (joints), edit=True, zso=True, oj='xyz', sao='yup')
cmds.setAttr( 'Fk_wristEnd_jnt.jointOrientY', 360)

# Create rig joints
# Create rig joints variable
jointInfo = (["rig_shoulder_jnt", [-0.2, 0, 8.5]], ["rig_elbow_jnt", [-4.0, 0, 0.04]], ["rig_wrist_jnt", [0.15, 0, -4.7]], ["rig_wristEnd_jnt", [-0.07, 0, -7.4]])
cmds.select(deselect=True)

# Create joints in loop
for item in jointInfo:
    cmds.joint(n=item[0], p=item[1])

# Orient joints
joints = [row[0] for row in jointInfo]
orientJoints = joints[0:3]
for item in orientJoints:
    cmds.joint( (joints), edit=True, zso=True, oj='xyz', sao='yup')
cmds.setAttr( 'rig_wristEnd_jnt.jointOrientY', 360)
cmds.select(deselect=True)







# Create Fk Rig

# Create fk Control
# Store the name of the fkjoints in list
fkjointNames = ["Fk_shoulder", "Fk_elbow", "Fk_wrist"]

# Store the grp control in list
fkgrpjointNames = ["grp_ctrl_Fk_shoulder", "grp_ctrl_Fk_elbow", "grp_ctrl_Fk_wrist"]


# Create an empty group named by the joint
for x in fkjointNames:
    cmds.group( em=True, name="grp_ctrl_" + str(x))


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

cmds.setAttr( 'ctrl_Fk_shoulder.tx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_shoulder.ty', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_shoulder.tz', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_shoulder.sx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_shoulder.sy', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_shoulder.sz', edit=True,  lock=True, keyable=False, channelBox=False )

cmds.setAttr( 'ctrl_Fk_elbow.tx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_elbow.ty', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_elbow.tz', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_elbow.sx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_elbow.sy', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_elbow.sz', edit=True,  lock=True, keyable=False, channelBox=False )

cmds.setAttr( 'ctrl_Fk_wrist.tx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_wrist.ty', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_wrist.tz', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_wrist.sx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_wrist.sy', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_Fk_wrist.sz', edit=True,  lock=True, keyable=False, channelBox=False )

# Create blend ctrl on rig arm
# Get ws position of wrist end joint
pos = cmds.xform('rig_wristEnd_jnt', q=True, t=True, ws=True)

# Create an empty group
cmds.group( em=True, name='grp_switch_ikfk' )
'''
# Orient grp to joint
rot = cmds.xform('rig_wristEnd_jnt', q=True, ro=True, ws=True)
cmds.xform('grp_switch_ikfk', ro=rot, ws=True)
'''
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
