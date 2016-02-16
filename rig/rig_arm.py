''' 
Arthur Klein 
Week2
rig_arm.py

This script builds an arm rig with IK and FK controls and a color blend 
utility to switch or blend. There is an IK, FK, and RIG bone chain with 
the IK and FK driving the rotations of the rig bones. 

'''


import maya.cmds as cmds



#Create all joints
#Create IK arm joints
cmds.joint(name='ik_shoulder_jnt', p=(-8, 0, 0))
cmds.joint(name='ik_elbow_jnt', p=(0, 0, -2))
cmds.joint(name='ik_wrist_jnt', p=(8, 0, 0))
cmds.joint(name='ik_wristEnd_jnt', p=(10, 0, 0))

cmds.select('ik_shoulder_jnt')
cmds.joint( 'ik_shoulder_jnt', e=True, oj='xyz', secondaryAxisOrient='yup', ch=True)
cmds.select(d=True)


#Create FK arm joints
cmds.joint(name='fk_shoulder_jnt', p=(-8, 0, 0))
cmds.joint(name='fk_elbow_jnt', p=(0, 0, -2))
cmds.joint(name='fk_wrist_jnt', p=(8, 0, 0))
cmds.joint(name='fk_wristEnd_jnt', p=(10, 0, 0))

cmds.select('fk_shoulder_jnt')
cmds.joint( 'fk_shoulder_jnt', e=True, oj='xyz', secondaryAxisOrient='yup', ch=True)
cmds.select(d=True)


#Create rig arm joints
cmds.joint(name='rig_shoulder_jnt', p=(-8, 0, 0))
cmds.joint(name='rig_elbow_jnt', p=(0, 0, -2))
cmds.joint(name='rig_wrist_jnt', p=(8, 0, 0))
cmds.joint(name='rig_wristEnd_jnt', p=(10, 0, 0))

cmds.select('rig_shoulder_jnt')
cmds.joint( 'rig_shoulder_jnt', e=True, oj='xyz', secondaryAxisOrient='yup', ch=True)
cmds.select(d=True)






#Get positions and rotations of all joints and assign to variables
shoulderPos = cmds.xform('rig_shoulder_jnt', q=True, ws=True, t=True)
elbowPos = cmds.xform('rig_elbow_jnt', q=True, ws=True, t=True)
wristPos = cmds.xform('rig_wrist_jnt', q=True, ws=True, t=True)

shoulderRot = cmds.xform('rig_shoulder_jnt', q=True, ws=True, ro=True)
elbowRot = cmds.xform('rig_elbow_jnt', q=True, ws=True, ro=True)
wristRot = cmds.xform('rig_wrist_jnt', q=True, ws=True, ro=True)






#Create IK Handle
cmds.ikHandle( name='ikh_arm', sj='ik_shoulder_jnt', ee='ik_wrist_jnt', sol='ikRPsolver')




#Create IK Controls and Pole Vector
#IK wrist control and zero group
cmds.circle( n='ikh_ctrl_arm', normal=(1, 0, 0), radius=1.5)
cmds.group('ikh_ctrl_arm', n='grp_ikh_ctrl_arm', world=True)
cmds.xform('grp_ikh_ctrl_arm', ws=True, t=wristPos, ro=wristRot)

#parent ik handle to ik control shape
cmds.parent( 'ikh_arm', 'ikh_ctrl_arm' )




#Pole Vector
#Create control and zero group
cmds.spaceLocator( name='ctrl_pv_arm')
cmds.group( 'ctrl_pv_arm', n='grp_ctrl_pv_arm', world=True)
cmds.xform('grp_ctrl_pv_arm', ws=True,  t=(elbowPos[0], elbowPos[1], (elbowPos[2]-6.0)))

#Apply pole vector contraint
cmds.poleVectorConstraint( 'ctrl_pv_arm', 'ikh_arm' )






#Create FK Controls
#Create control shapes and zero groups 
#Add Loop here:
cmds.circle( n='fk_ctrl_shoulder', normal=(1, 0, 0))
cmds.circle( n='fk_ctrl_elbow', normal=(1, 0, 0))
cmds.circle( n='fk_ctrl_wrist', normal=(1, 0, 0))

cmds.group('fk_ctrl_shoulder', n='grp_fk_ctrl_shoulder', world=True)
cmds.group('fk_ctrl_elbow', n='grp_fk_ctrl_elbow', world=True)
cmds.group('fk_ctrl_wrist', n='grp_fk_ctrl_wrist', world=True)

cmds.xform('grp_fk_ctrl_shoulder', ws=True, t=shoulderPos, ro=shoulderRot)
cmds.xform('grp_fk_ctrl_elbow', ws=True, t=elbowPos, ro=elbowRot)
cmds.xform('grp_fk_ctrl_wrist', ws=True, t=wristPos, ro=wristRot)


#Connect rotations of ctrl shapes to rotations of fk bones
cmds.connectAttr( 'fk_ctrl_shoulder.rotate', 'fk_shoulder_jnt.rotate' )
cmds.connectAttr( 'fk_ctrl_elbow.rotate', 'fk_elbow_jnt.rotate' )
cmds.connectAttr( 'fk_ctrl_wrist.rotate', 'fk_wrist_jnt.rotate' )







#Create IK/FK Blend and attach rotations of ik and fk skeletons to rig skeleton
cmds.shadingNode('blendColors', asShader=True, n='bldNode_shoulderikfk')
cmds.shadingNode('blendColors', asShader=True, n='bldNode_elbowikfk')
cmds.shadingNode('blendColors', asShader=True, n='bldNode_wristikfk')


#Connect IK controls to color1
#Add more loops here:
cmds.connectAttr( 'ik_shoulder_jnt.rotate', 'bldNode_shoulderikfk.color1', force=True )
cmds.connectAttr( 'ik_elbow_jnt.rotate', 'bldNode_elbowikfk.color1', force=True )
cmds.connectAttr( 'ik_wrist_jnt.rotate', 'bldNode_wristikfk.color1', force=True )


#Connect FK controls to color2
cmds.connectAttr( 'fk_shoulder_jnt.rotate', 'bldNode_shoulderikfk.color2', force=True )
cmds.connectAttr( 'fk_elbow_jnt.rotate', 'bldNode_elbowikfk.color2', force=True )
cmds.connectAttr( 'fk_wrist_jnt.rotate', 'bldNode_wristikfk.color2', force=True )







#Loop to connect RGB output of colorblend to rotate XYZ of rig bones 
arm_bones = ['shoulder', 'elbow', 'wrist']
colors = ['R', 'G', 'B']
axes = ['X', 'Y', 'Z']

for bone in arm_bones:
	for color in colors:
		for axis in axes:
			cmds.connectAttr('bldNode_' + bone + 'ikfk.output' + color, 'rig_' + bone + '_jnt.rotate' + axis, force=True)
					



#Set all blends to IK by default
cmds.setAttr('bldNode_shoulderikfk.blender', 0)
cmds.setAttr('bldNode_elbowikfk.blender', 0)
cmds.setAttr('bldNode_wristikfk.blender', 0)













