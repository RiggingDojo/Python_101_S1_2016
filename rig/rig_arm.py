# Create IK rig
cmds.joint(n='ik_shoulder_jnt', p=[2.1, 0, 5.0])
cmds.joint(n='ik_elbow_jnt', p=[-0.1, 0, 0.0])
cmds.joint(n='ik_wrist_jnt', p=[1.0, 0, -5.0])
cmds.joint(n='ik_wristEnd_jnt', p=[1.0, 0, -8.0])

# Orient IK arm joints
cmds.joint( 'ik_shoulder_jnt', edit=True, zso=True, oj='xyz', sao='yup' )  
cmds.joint( 'ik_elbow_jnt', edit=True, zso=True, oj='xyz', sao='yup' )
cmds.joint( 'ik_wrist_jnt', edit=True, zso=True, oj='xyz', sao='yup' )
cmds.setAttr( 'ik_wristEnd_jnt.jointOrientY', 360 )
 
# Ik handle
cmds.ikHandle( n='ikh_arm', sj='ik_shoulder_jnt', ee='ik_wrist_jnt', sol='ikRPsolver', p=2, w=1 )
 
# Create ik control
# Get ws position of wrist joint
pos = cmds.xform('ik_wrist_jnt', q=True, t=True, ws=True)

# Create an empty group
cmds.group( em=True, name='grp_ctrl_ikWrist' )

# Create circle control object
cmds.circle( n='ctrl_ikWrist', nr=(0, 0, 1), c=(0, 0, 0) )

# Parent the control to the group
cmds.parent('ctrl_ikWrist', 'grp_ctrl_ikWrist')

# Move the group to the joint
cmds.xform('grp_ctrl_ikWrist', t=pos, ws=True)

# Parent ikh to ctrl
cmds.parent('ikh_arm', 'ctrl_ikWrist')

# Create pole vector
pos = cmds.xform('ik_elbow_jnt', q=True, t=True, ws=True)
pos[0] -= 2
cmds.spaceLocator( n='ik_pv_arm', p=pos, a=True)

# Attach pole vector to IK
cmds.poleVectorConstraint( 'ik_pv_arm', 'ikh_arm' )

# Lock and hide ctrl attributes
cmds.setAttr( 'ctrl_ikWrist.sx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_ikWrist.sy', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_ikWrist.sz', edit=True,  lock=True, keyable=False, channelBox=False )

# Deselect to avoid parenting
cmds.select(d=True)

# Create FK rig
# Create FK arm joints
cmds.joint( n='fk_shoulder_jnt', p=[2.1, 0, 5.0] )
cmds.joint( n='fk_elbow_jnt', p=[-0.1, 0, 0.0] )
cmds.joint( n='fk_wrist_jnt', p=[1.0, 0, -5.0] )
cmds.joint( n='fk_wristEnd_jnt', p=[1.0, 0, -8.0] )

# Orient FK arm joints
cmds.joint( 'fk_shoulder_jnt', edit=True, zso=True, oj='xyz', sao='yup' )  
cmds.joint( 'fk_elbow_jnt', edit=True, zso=True, oj='xyz', sao='yup' )
cmds.joint( 'fk_wrist_jnt', edit=True, zso=True, oj='xyz', sao='yup' )
cmds.setAttr( 'fk_wristEnd_jnt.jointOrientY', 360 )

# Get ws position of wrist joint
pos = cmds.xform('fk_wrist_jnt', q=True, t=True, ws=True)

# Create an empty group
cmds.group( em=True, name='grp_ctrl_fkWrist' )

# Orient grp to joint
rot = cmds.xform('fk_wrist_jnt', q=True, ro=True, ws=True)
cmds.xform('grp_ctrl_fkWrist', ro=rot, ws=True)

# Create circle control object
cmds.circle( n='ctrl_fkWrist', nr=(1, 0, 0), c=(0, 0, 0) )

# Parent the control to the group
cmds.parent('ctrl_fkWrist', 'grp_ctrl_fkWrist')
cmds.setAttr( "ctrl_fkWrist.rotateY", 0 )

# Move the group to the joint
cmds.xform('grp_ctrl_fkWrist', t=pos, ws=True)

# Get ws position of elbow joint
pos = cmds.xform('fk_elbow_jnt', q=True, t=True, ws=True)

# Create an empty group
cmds.group( em=True, name='grp_ctrl_fkElbow' )

# Orient grp to joint
rot = cmds.xform('fk_elbow_jnt', q=True, ro=True, ws=True)
cmds.xform('grp_ctrl_fkElbow', ro=rot, ws=True)

# Create circle control object
cmds.circle( n='ctrl_fkElbow', nr=(1, 0, 0), c=(0, 0, 0) )


# Parent the control to the group
cmds.parent('ctrl_fkElbow', 'grp_ctrl_fkElbow')
cmds.setAttr( "ctrl_fkElbow.rotateY", 0 )

# Move the group to the joint
cmds.xform('grp_ctrl_fkElbow', t=pos, ws=True)

# Get ws position of shoulder joint
pos = cmds.xform('fk_shoulder_jnt', q=True, t=True, ws=True)

# Create an empty group
cmds.group( em=True, name='grp_ctrl_fkShoulder' )

# Orient grp to joint
rot = cmds.xform('fk_shoulder_jnt', q=True, ro=True, ws=True)
cmds.xform('grp_ctrl_fkShoulder', ro=rot, ws=True)

# Create circle control object
cmds.circle( n='ctrl_fkShoulder', nr=(1, 0, 0), c=(0, 0, 0) )

# Parent the control to the group
cmds.parent('ctrl_fkShoulder', 'grp_ctrl_fkShoulder')
cmds.setAttr( "ctrl_fkShoulder.rotateY", 0 )


# Move the group to the joint
cmds.xform('grp_ctrl_fkShoulder', t=pos, ws=True)

# Parent cntrls
cmds.parent('grp_ctrl_fkElbow', 'ctrl_fkShoulder')
cmds.parent('grp_ctrl_fkWrist', 'ctrl_fkElbow')

# Orient constrain joints to ctrls
cmds.orientConstraint( 'ctrl_fkShoulder', 'fk_shoulder_jnt' )
cmds.orientConstraint( 'ctrl_fkElbow', 'fk_elbow_jnt' )
cmds.orientConstraint( 'ctrl_fkWrist', 'fk_wrist_jnt' )

# Lock and hide ctrl attributes
cmds.setAttr( 'ctrl_fkWrist.tx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkWrist.ty', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkWrist.tz', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkWrist.sx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkWrist.sy', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkWrist.sz', edit=True,  lock=True, keyable=False, channelBox=False )

cmds.setAttr( 'ctrl_fkElbow.tx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkElbow.ty', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkElbow.tz', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkElbow.sx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkElbow.sy', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkElbow.sz', edit=True,  lock=True, keyable=False, channelBox=False )

cmds.setAttr( 'ctrl_fkShoulder.tx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkShoulder.ty', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkShoulder.tz', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkShoulder.sx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkShoulder.sy', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_fkShoulder.sz', edit=True,  lock=True, keyable=False, channelBox=False )

# Deselect to avoid parenting
cmds.select(d=True)

# Create bind arm
# Create bind arm joints
cmds.joint( n='bn_shoulder_jnt', p=[2.1, 0, 5.0] )
cmds.joint( n='bn_elbow_jnt', p=[-0.1, 0, 0.0] )
cmds.joint( n='bn_wrist_jnt', p=[1.0, 0, -5.0] )
cmds.joint( n='bn_wristEnd_jnt', p=[1.0, 0, -8.0] )

# Orient rig arm joints
cmds.joint( 'bn_shoulder_jnt', edit=True, zso=True, oj='xyz', sao='yup' )  
cmds.joint( 'bn_elbow_jnt', edit=True, zso=True, oj='xyz', sao='yup' )
cmds.joint( 'bn_wrist_jnt', edit=True, zso=True, oj='xyz', sao='yup' )
cmds.setAttr( 'bn_wristEnd_jnt.jointOrientY', 360 )

# Connect Ik and Fk to bind joints
cmds.parentConstraint( 'ik_shoulder_jnt', 'bn_shoulder_jnt', weight = 0.0 )
cmds.parentConstraint( 'fk_shoulder_jnt', 'bn_shoulder_jnt' )

cmds.parentConstraint( 'ik_elbow_jnt', 'bn_elbow_jnt', weight = 0.0 )
cmds.parentConstraint( 'fk_elbow_jnt', 'bn_elbow_jnt' )

cmds.parentConstraint( 'ik_wrist_jnt', 'bn_wrist_jnt', weight = 0.0 )
cmds.parentConstraint( 'fk_wrist_jnt', 'bn_wrist_jnt' )


