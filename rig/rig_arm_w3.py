# Label names for the objects
names = {'ikPrefix': 'ik', 
         'fkPrefix': 'fk',
         'groupPrefix': 'grp',
         'controlPrefix': 'ctrl',
         'jointSufix': 'jnt',
         'bindPrefix': 'bn',
         'poleVector': 'pv',
         'shoulder': 'shoulder',
         'elbow': 'elbow',
         'wrist': 'wrist',
         'wristEnd': 'wristEnd',
         'ikHandle': 'ikh',
         'armSufix': 'arm',
         'plusMinusPrefix': 'plusminus',
         'multiplyDividePrefix': 'multdiv',
         'blendingNode': 'FKIK_Blender'
         }
         
# Lists with joints data
joint_info = [['shoulder', [2.1, 0.0, 5.0]], 
              ['elbow', [-0.1, 0.0, 0.0]], 
              ['wrist', [-0.1, 0.0, -5.0]], 
              ['wristEnd', [1.0, 0.0, -8.0]]]
             
joint_chains = (names['ikPrefix'],
                names['fkPrefix'], 
                names['bindPrefix'])

joint_dict = {}
  
for i in joint_chains:
    tmpjnt_lst = []
    for j in range(len(joint_info)):
        new_name = j + joint_info[j][0]
        print new_name
        tmpjnt_lst.append([new_name, joint_info[j][1]])
     
    joint_dict[i] = tmpjnt_lst
     
print joint_dict



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

# Delete history
cmds.delete( 'ctrl_ikWrist', constructionHistory=True )

# Parent the control to the group
cmds.parent('ctrl_ikWrist', 'grp_ctrl_ikWrist')

# Move the group to the joint
cmds.xform('grp_ctrl_ikWrist', t=pos, ws=True)

# Parent ikh to ctrl
cmds.parent('ikh_arm', 'ctrl_ikWrist')

# Orient constraint ctrl to joint
cmds.orientConstraint( 'ctrl_ikWrist', 'ik_wrist_jnt', mo = True)

# Create pole vector
pos = cmds.xform('ik_elbow_jnt', q=True, t=True, ws=True)
pos[0] -= 2
cmds.spaceLocator( n='ik_pv_arm')
print cmds.xform('ik_pv_arm', q=True, ws=True, t=True)
cmds.xform('ik_pv_arm', ws=True, t=pos)

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

# Delete history
cmds.delete( 'ctrl_fkWrist', constructionHistory=True )

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

# Delete history
cmds.delete( 'ctrl_fkElbow', constructionHistory=True )

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

# Delete history
cmds.delete( 'ctrl_fkShoulder', constructionHistory=True )

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

# Deselect to avoid parenting
cmds.select(d=True)

# Create blend ctrl
# Get ws position of wrist end joint
pos = cmds.xform('bn_wristEnd_jnt', q=True, t=True, ws=True)

# Create an empty group
cmds.group( em=True, name='grp_ctrl_arm' )

# Orient grp to joint
rot = cmds.xform('bn_wristEnd_jnt', q=True, ro=True, ws=True)
cmds.xform('grp_ctrl_arm', ro=rot, ws=True)

# Create circle control object
cmds.circle( n='ctrl_arm', nr=(1, 0, 0), c=(0, 0, 0) )

# Delete history
cmds.delete( 'ctrl_arm', constructionHistory=True )

# Parent ctrl to group and group to wrist end joint
cmds.parent('ctrl_arm', 'grp_ctrl_arm')
cmds.setAttr( "ctrl_arm.rotateY", 0 )
cmds.setAttr( "ctrl_arm.rotateZ", 90 )
# Move the group to the joint
cmds.xform('grp_ctrl_arm', t=pos, ws=True)
cmds.parent('grp_ctrl_arm', 'bn_wristEnd_jnt')

# Lock and hide ctrl attributes
cmds.setAttr( 'ctrl_arm.tx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_arm.ty', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_arm.tz', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_arm.rx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_arm.ry', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_arm.rz', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_arm.sx', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_arm.sy', edit=True,  lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'ctrl_arm.sz', edit=True,  lock=True, keyable=False, channelBox=False )

# Create blend attribute
cmds.select( d=True )
cmds.select( 'ctrl_arm' )
cmds.addAttr( 'ctrl_arm', ln='FKIKBlend', at='long', min=0, max=10, dv=0 )
cmds.setAttr( 'ctrl_arm.FKIKBlend', edit=True, keyable=True )
cmds.setAttr( 'ctrl_arm.FKIKBlend', 0 )

# Create nodes to perform the blend
cmds.createNode( 'multiplyDivide', n='multDiv_FKIKBlender' )
cmds.connectAttr( 'ctrl_arm.FKIKBlend', 'multDiv_FKIKBlender.input1X')
cmds.setAttr( 'multDiv_FKIKBlender.input2X', 10 )

cmds.createNode( 'plusMinusAverage', n='plusMinus_FKIKBlender' )
cmds.setAttr( 'plusMinus_FKIKBlender.operation', 2 )
cmds.setAttr( 'plusMinus_FKIKBlender.input1D[0]', 100 )
cmds.connectAttr( 'multDiv_FKIKBlender.output.outputX', 'plusMinus_FKIKBlender.input1D[1]')

cmds.connectAttr( 'multDiv_FKIKBlender.output.outputX', 'bn_shoulder_jnt_parentConstraint1.ik_shoulder_jntW0')
cmds.connectAttr( 'plusMinus_FKIKBlender.output1D', 'bn_shoulder_jnt_parentConstraint1.fk_shoulder_jntW1')

cmds.connectAttr( 'multDiv_FKIKBlender.outputX', 'bn_elbow_jnt_parentConstraint1.ik_elbow_jntW0')
cmds.connectAttr( 'plusMinus_FKIKBlender.output1D', 'bn_elbow_jnt_parentConstraint1.fk_elbow_jntW1')

cmds.connectAttr( 'multDiv_FKIKBlender.output.outputX', 'bn_wrist_jnt_parentConstraint1.ik_wrist_jntW0')
cmds.connectAttr( 'plusMinus_FKIKBlender.output1D', 'bn_wrist_jnt_parentConstraint1.fk_wrist_jntW1')




