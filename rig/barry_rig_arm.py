import maya.cmds as cmds



#Create Ik Joints
cmds.joint( n='ik_shoulder_jnt', p=[2.1, 0, 5.0])
cmds.joint( n='ik_elbow_jnt', p=[-0.1, 0, 0.0])
cmds.joint( n='ik_wrist_jnt', p=[-0.1, 0, -5.0])
cmds.joint( n='ik_wristEnd_jnt', p=[1.0, 0, -8.0])

#de-select
cmds.select(d=True)


#Create Fk Joints
cmds.joint( n='fk_shoulder_jnt', p=[2.1, 0, 5.0])
cmds.joint( n='fk_elbow_jnt', p=[-0.1, 0, 0.0])
cmds.joint( n='fk_wrist_jnt', p=[-0.1, 0, -5.0])
cmds.joint( n='fk_wristEnd_jnt', p=[1.0, 0, -8.0])

#de-select
cmds.select(d=True)

#Create rig Joints
cmds.joint( n='rig_shoulder_jnt', p=[2.1, 0, 5.0])
cmds.joint( n='rig_elbow_jnt', p=[-0.1, 0, 0.0])
cmds.joint( n='rig_wrist_jnt', p=[-0.1, 0, -5.0])
cmds.joint( n='rig_wristEnd_jnt', p=[1.0, 0, -8.0])

#de-select
cmds.select(d=True)

#Create Ik Rig

#orientation for ik joints
cmds.joint( "ik_shoulder_jnt", edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True)


#Ik Handle
cmds.ikHandle( n='ikh_arm', sj='ik_shoulder_jnt', ee='ik_wrist_jnt', sol='ikRPsolver', p=2, w=1)

#Create Ik control

#create ws position of wrist joint
pos = cmds.xform('ik_wrist_jnt', q=True, t=True, ws=True)

#Create an empty group
cmds.group( em=True, name='grp_ctrl_ikWrist')

#create circle contorl object
cmds.circle( n='ctrl_ikWrist', nr=(0,0,1), c=(0,0,0))

#Parent the control to the group
cmds.parent('ctrl_ikWrist', 'grp_ctrl_ikWrist')

#move the gorup to the joint
cmds.xform('grp_ctrl_ikWrist',t=pos, ws=True)

#Parent ikh to ctrl
cmds.parent('ikh_arm', 'ctrl_ikWrist')

#Create Controller for Pole vector function
cmds.textCurves(f='Times-Roman', t='E', n="ctrl_ikElbow")

#Store world space location of elbow joint
pos_elbow = cmds.xform('ik_elbow_jnt', q=True, t=True, ws=True)

#Move and rotate 'E'
cmds.move(-5,0,0, 'ctrl_ik_elbow' )
cmds.rotate(0, 90, 0, 'ctrl_ik_elbow', r=True)
cmds.move(-5,0,1, 'ctrl_ik_elbow' )

#Freeze transformations on elbow Ctrol
cmds.makeIdentity( apply=True, t=1, r=1, s=1, n=0, pn=1 )

#Connect Controller to ikHandle via pole-Vector
cmds.poleVectorConstraint( 'ctrl_ik_elbow' ,'ikh_arm')




############################################################################################################

#Create Fk rig

#orientation for fk joints
cmds.joint( "rig_shoulder_jnt", edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True)

#create control circle
for i in range(3):
    cmds.circle(n='ctrl_fk_shoulder', nr=(0,0,1), c=(0,0,0))
   
#rename ctrls
cmds.select( 'ctrl_fk_shoulder1', r=True)
cmds.rename( 'ctrl_fk_elbow')

cmds.select( 'ctrl_fk_shoulder2', r=True)
cmds.rename( 'ctrl_fk_wrist')

#store world space coordinates in pos variable
pos_fk_wrist = cmds.xform('fk_wrist_jnt', q=True, t=True, ws=True)
pos_fk_shoulder = cmds.xform('fk_shoulder_jnt', q=True, t=True, ws=True)

#Create an empty group for fkWrist
cmds.group( em=True, name='grp_ctrl_fkWrist')

#Parent the fkWrist control to the group
cmds.parent('ctrl_fkWrist', 'grp_ctrl_fkWrist')

#move the group to the joint
cmds.xform('grp_ctrl_kWrist',t=pos_fk_wrist, ws=True)

#Freeze transformations on elbow Ctrl
cmds.select('grp_ctrl_fkWrist')
cmds.makeIdentity( apply=True, t=1, r=1, s=1, n=0, pn=1 )

#Create an empty group for fkShoulder
cmds.group( em=True, name='grp_ctrl_fkShoulder')

#Parent the fk shoulder control to the group
cmds.parent('ctrl_fk_shoulder', 'grp_ctrl_fkShoulder')


#Create an empty group for fkelbow
cmds.group( em=True, name='grp_ctrl_fkElbow')

#Parent the fk elbow control to the group
cmds.parent('ctrl_fk_elbow', 'grp_ctrl_fkElbow')

#move the group to the joint
cmds.xform('grp_ctrl_fkShoulder',t=pos_fk_shoulder, ws=True)

#Freeze transformations on elbow Ctrl
cmds.select('grp_ctrl_fkShoulder')
cmds.makeIdentity( apply=True, t=1, r=1, s=1, n=0, pn=1 )

#Orient Constrain the wrist and shoulder ctrls to the jnts
cmds.select('grp_ctrl_fkShoulder')
cmds.orientConstraint('grp_ctrl_fkShoulder', 'fk_shoulder_jnt', mo=True)


#Orient Constrain the wrist and shoulder ctrls to the jnts
cmds.select('grp_ctrl_fkWrist')
cmds.orientConstraint('grp_ctrl_fkWrist', 'fk_wrist_jnt', mo=True)


#Orient Constrain the wrist and shoulder ctrls to the jnts
cmds.select('grp_ctrl_fkElbow')
cmds.orientConstraint('grp_ctrl_fkElbow', 'fk_elbow_jnt', mo=True)

#Parent Constraint Wrist to Elbow, Elbow to Shoulder
cmds.parent('grp_ctrl_fkWrist','grp_ctrl_fkElbow')
cmds.parent('grp_ctrl_fkElbow','grp_ctrl_fkShoulder')



############################################################################################################

#Connect ik and fk to rig joints


#orientation for rig joints 
cmds.joint( "rig_shoulder_jnt", edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True)

#Orient constrain to the rig joints
cmds.orientConstraint('ik_shoulder_jnt', 'rig_shoulder_jnt', mo=True)
cmds.orientConstraint('fk_shoulder_jnt', 'rig_shoulder_jnt', mo=True)

cmds.orientConstraint('ik_elbow_jnt', 'rig_elbow_jnt', mo=True)
cmds.orientConstraint('fk_elbow_jnt', 'rig_elbow_jnt', mo=True)

cmds.orientConstraint('ik_wrist_jnt', 'rig_wrist_jnt', mo=True)
cmds.orientConstraint('fk_wrist_jnt', 'rig_wrist_jnt', mo=True)



