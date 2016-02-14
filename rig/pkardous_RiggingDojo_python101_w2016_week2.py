# ------------------------------------------ #
# --- Rigging Dojo ------------------------- #
# ------------------------------------------ #
# ------------------------------------------ #
# --- Python Scripting 101 | Winter 2016 --- #
# ------------------------------------------ #
# ------------------------------------------ #
# --- Teacher : Ryan Griffin --------------- #
# --- Student : Philippe Kardous ----------- #
# ------------------------------------------ #

"""
Hi M. Griffin,

First of all I apologize for the late assignment handout and for not pushing it very far yet; I'll do better in the weeks to come.

I know there's much MUCH more to be done, but here's my very basic arm rig code, I'm really looking forward to better understanding
loops to loop through all those recurring commands. I tried to do loops to create my joints from locators, but I also wanted them
to be renamed as the locators and since I'm still struggling to fully understand how to do efficient loops, I kept my code for our week 3
as it also meant doing the connections and everything in loops.

In this exercice I made it easy on me by placing the joints with a logical physical "preferred angle" but I had as a question
how do we set a preferred angle to a straight chain in code? I know manually you can rotate the chain in the direction
you want it to bend by defaut and then 'set preferred angle', but I didn't find that you could give a value;
all I found in the python documentation for Maya is that you need to be in edit mode, but I'm not quite sure I understand that
as basic as it might be.
"""

# ----------------------------------- #
# -------- Week 2 Assignment -------- #
# ----------------------------------- #
# --- Hard coding a basic arm rig --- #
# ----------------------------------- #

import maya.cmds as mc

# --- Creating the basic rig joints
mc.joint(name='L_shoulder_rigJnt', position=[2, 44.5, -1.5], radius=1)
mc.joint(name='L_forearm_rigJnt', position=[12.25, 44.5, -1.8], radius=1)
mc.joint(name='L_wrist_rigJnt', position=[22.5, 44.5, -1.5], radius=1)
mc.joint(name='L_palm_rigJnt', position=[25, 44.5, -1.5], radius=1)
mc.select(clear=True)

# --- Creating the IK driving joints
mc.joint(name='L_shoulder_IkJnt', position=[2, 44.5, -1.5], radius=1.5)
mc.joint(name='L_forearm_IkJnt', position=[12.25, 44.5, -1.8], radius=1.5)
mc.joint(name='L_wrist_IkJnt', position=[22.5, 44.5, -1.5], radius=1.5)
mc.joint(name='L_palm_IkJnt', position=[25, 44.5, -1.5], radius=1.5)
mc.select(clear=True)

# --- Creating the FK driving joints
mc.joint(name='L_shoulder_FkJnt', position=[2, 44.5, -1.5], radius=1.25)
mc.joint(name='L_forearm_FkJnt', position=[12.25, 44.5, -1.8], radius=1.25)
mc.joint(name='L_wrist_FkJnt', position=[22.5, 44.5, -1.5], radius=1.25)
mc.joint(name='L_palm_FkJnt', position=[25, 44.5, -1.5], radius=1.25)
mc.select(clear=True)

# --- Creating the IK Handle and rename effector
mc.ikHandle(name='L_arm_IkHdl', startJoint='L_shoulder_IkJnt', endEffector='L_wrist_IkJnt', solver='ikRPsolver', p=2, w=1)
mc.rename('effector1', 'L_armIk_eff')

# --- Creating the IK Ctrl
# --- Get world space position of wrist joint
wristPos = mc.xform('L_wrist_IkJnt', query=True, translation=True, worldSpace=True)
# --- Create and empty group
mc.group(empty=True, name='L_Ik_CtrlGrp')
# --- Create IK ctrl
mc.circle(name='L_arm_IkCtrl', normal=[1, 0, 0], center=[0, 0, 0], radius=2)
# --- Match the ctrl grp to the position of the wrist
mc.delete(mc.parentConstraint('L_wrist_IkJnt', 'L_Ik_CtrlGrp', maintainOffset=False))
mc.duplicate('L_Ik_CtrlGrp')
mc.rename('L_Ik_CtrlGrp1', 'L_Ik_CtrlAbsGrp')
mc.parent('L_Ik_CtrlGrp', 'L_Ik_CtrlAbsGrp')
# --- Parent the shape of the ctrl to the handle
mc.parent(['L_arm_IkCtrlShape', 'L_arm_IkHdl'], relative=True, shape=True)
# --- Parent the ctrl to the grp
mc.parent(['L_arm_IkHdl', 'L_Ik_CtrlGrp']) # relative=True, shape=True
# --- Delete leftover transform node after the shape parenting
mc.delete('L_arm_IkCtrl')
# --- creating pole vector
mc.spaceLocator(name='L_arm_poleVector', p=[0, 0, 0])
mc.delete(mc.parentConstraint('L_forearm_IkJnt', 'L_arm_poleVector', mo=False))
mc.setAttr("L_arm_poleVector.translateZ", (-1.8 -10))
mc.makeIdentity('L_arm_poleVector', apply=True)
cmds.poleVectorConstraint( 'L_arm_poleVector', 'L_arm_IkHdl' )
# --- Creating the FK rig
# --- Creating our shoulder FK ctrl
mc.circle(name='L_shoulder_FkCtrl', normal=[0, 1, 0], center=[5, 0, 0], radius=5)
mc.parent(['L_shoulder_FkCtrlShape', 'L_shoulder_FkJnt'], relative=True, shape=True)
mc.delete('L_shoulder_FkCtrl')
mc.circle(name='L_forearm_FkCtrl', normal=[0, 1, 0], center=[5, 0, 0], radius=5)
mc.parent(['L_forearm_FkCtrlShape', 'L_forearm_FkJnt'], relative=True, shape=True)
mc.delete('L_forearm_FkCtrl')
mc.circle(name='L_wrist_FkCtrl', normal=[0, 1, 0], center=[3, 0, 0], radius=3)
mc.parent(['L_wrist_FkCtrlShape', 'L_wrist_FkJnt'], relative=True, shape=True)
mc.delete('L_wrist_FkCtrl')

# --- Connecting the IK and FK driving chains to the rigSkinChain
# --- create all necessary blend color nodes
# ---
# --- Translation blends
mc.shadingNode('blendColors', asUtility=True, name='L_shoulder_trans_IKFK_choice') # shoulder
mc.shadingNode('blendColors', asUtility=True, name='L_forearm_trans_IKFK_choice') # forearm
mc.shadingNode('blendColors', asUtility=True, name='L_wrist_trans_IKFK_choice') # wrist
mc.shadingNode('blendColors', asUtility=True, name='L_palm_trans_IKFK_choice') # palm
# --- Rotation blends
mc.shadingNode('blendColors', asUtility=True, name='L_shoulder_rot_IKFK_choice') # shoulder
mc.shadingNode('blendColors', asUtility=True, name='L_forearm_rot_IKFK_choice') # forearm
mc.shadingNode('blendColors', asUtility=True, name='L_wrist_rot_IKFK_choice') # wrist
mc.shadingNode('blendColors', asUtility=True, name='L_palm_rot_IKFK_choice') # palm
# ---
# --- connecting the shoulder IKFK blend to Rig
mc.connectAttr('L_shoulder_IkJnt.rotate', 'L_shoulder_rot_IKFK_choice.color1', force=True)
mc.connectAttr('L_shoulder_FkJnt.rotate', 'L_shoulder_rot_IKFK_choice.color2', force=True)
mc.connectAttr('L_shoulder_IkJnt.translate', 'L_shoulder_trans_IKFK_choice.color1', force=True)
mc.connectAttr('L_shoulder_FkJnt.translate', 'L_shoulder_trans_IKFK_choice.color2', force=True)
mc.connectAttr('L_shoulder_trans_IKFK_choice.output', 'L_shoulder_rigJnt.translate', force=True)
mc.connectAttr('L_shoulder_rot_IKFK_choice.output', 'L_shoulder_rigJnt.rotate', force=True)
# ---
# --- connecting the forearm IKFK blend to Rig
mc.connectAttr('L_forearm_IkJnt.rotate', 'L_forearm_rot_IKFK_choice.color1', force=True)
mc.connectAttr('L_forearm_FkJnt.rotate', 'L_forearm_rot_IKFK_choice.color2', force=True)
mc.connectAttr('L_forearm_IkJnt.translate', 'L_forearm_trans_IKFK_choice.color1', force=True)
mc.connectAttr('L_forearm_FkJnt.translate', 'L_forearm_trans_IKFK_choice.color2', force=True)
mc.connectAttr('L_forearm_trans_IKFK_choice.output', 'L_forearm_rigJnt.translate', force=True)
mc.connectAttr('L_forearm_rot_IKFK_choice.output', 'L_forearm_rigJnt.rotate', force=True)
# ---
# --- connecting the wrist IKFK blend to Rig
mc.connectAttr('L_wrist_IkJnt.rotate', 'L_wrist_rot_IKFK_choice.color1', force=True)
mc.connectAttr('L_wrist_FkJnt.rotate', 'L_wrist_rot_IKFK_choice.color2', force=True)
mc.connectAttr('L_wrist_IkJnt.translate', 'L_wrist_trans_IKFK_choice.color1', force=True)
mc.connectAttr('L_wrist_FkJnt.translate', 'L_wrist_trans_IKFK_choice.color2', force=True)
mc.connectAttr('L_wrist_trans_IKFK_choice.output', 'L_wrist_rigJnt.translate', force=True)
mc.connectAttr('L_wrist_rot_IKFK_choice.output', 'L_wrist_rigJnt.rotate', force=True)
# ---
# --- connecting the palm IKFK blend to Rig
mc.connectAttr('L_palm_IkJnt.rotate', 'L_palm_rot_IKFK_choice.color1', force=True)
mc.connectAttr('L_palm_FkJnt.rotate', 'L_palm_rot_IKFK_choice.color2', force=True)
mc.connectAttr('L_palm_IkJnt.translate', 'L_palm_trans_IKFK_choice.color1', force=True)
mc.connectAttr('L_palm_FkJnt.translate', 'L_palm_trans_IKFK_choice.color2', force=True)
mc.connectAttr('L_palm_trans_IKFK_choice.output', 'L_palm_rigJnt.translate', force=True)
mc.connectAttr('L_palm_rot_IKFK_choice.output', 'L_palm_rigJnt.rotate', force=True)

# --- Creating option ctrl with attribute to switch IK/FK
mc.circle(name='L_arm_settings_Ctrl', normal=[0, 1, 0], center=[0, 0, 0], radius=1)
mc.curve(name='L_arm_settings_crvShape1', d=1, p=[(0, 0, -1), (0, 0, 4)], k=[0,1])
mc.curve(name='L_arm_settings_crvShape2', d=1, p=[(-1, 0, 0), (1, 0, 0)], k=[0,1])
mc.rename('curveShape1', 'L_arm_settings_crvShape1Shape')
mc.rename('curveShape2', 'L_arm_settings_crvShape2Shape')
mc.parent(['L_arm_settings_crvShape1Shape', 'L_arm_settings_crvShape2Shape'], 'L_arm_settings_Ctrl', relative=True, shape=True)
mc.delete(['L_arm_settings_crvShape1', 'L_arm_settings_crvShape2'])
# --- Grouping the ctrl under cstr grp constrainted to the wrist
mc.xform('L_arm_settings_Ctrl', piv=[0, 0, 4])
mc.group(empty=True, name='L_arm_settings_CstrGrp')
mc.xform('L_arm_settings_CstrGrp', piv=[0, 0, 4])
mc.parent('L_arm_settings_Ctrl', 'L_arm_settings_CstrGrp')
mc.parentConstraint('L_wrist_rigJnt', 'L_arm_settings_CstrGrp', maintainOffset=False)
# --- Adding the attribute IK/FK switch onto the settings control
mc.addAttr(['L_arm_settings_Ctrl'], longName='IkFkSwitch', niceName='Ik Fk Switch', attributeType='float', min=0, max=1, defaultValue=0, keyable=True)
# --- Connect attribute so that IkFkSwitch 0 be the IK and 1 be the FK
mc.connectAttr('L_arm_settings_Ctrl.IkFkSwitch', 'L_shoulder_trans_IKFK_choice.blender', force=True)
mc.connectAttr('L_arm_settings_Ctrl.IkFkSwitch', 'L_shoulder_rot_IKFK_choice.blender', force=True)
mc.connectAttr('L_arm_settings_Ctrl.IkFkSwitch', 'L_forearm_trans_IKFK_choice.blender', force=True)
mc.connectAttr('L_arm_settings_Ctrl.IkFkSwitch', 'L_forearm_rot_IKFK_choice.blender', force=True)
mc.connectAttr('L_arm_settings_Ctrl.IkFkSwitch', 'L_wrist_trans_IKFK_choice.blender', force=True)
mc.connectAttr('L_arm_settings_Ctrl.IkFkSwitch', 'L_wrist_rot_IKFK_choice.blender', force=True)
mc.connectAttr('L_arm_settings_Ctrl.IkFkSwitch', 'L_palm_trans_IKFK_choice.blender', force=True)
mc.connectAttr('L_arm_settings_Ctrl.IkFkSwitch', 'L_palm_rot_IKFK_choice.blender', force=True)

# --- Creating a mesh and skinning for the sake of it
mc.polyCube(name='L_arm_skn_mesh', width=23, height=2, depth=2, subdivisionsX=18, subdivisionsY=2, subdivisionsZ=2, axis=[0, 1, 0], ch=1)
mc.setAttr('L_arm_skn_mesh.translateX', 13.495)
mc.setAttr('L_arm_skn_mesh.translateY', 44.5)
mc.setAttr('L_arm_skn_mesh.translateZ', -1.598)
mc.makeIdentity('L_arm_skn_mesh', apply=True)
mc.delete('L_arm_skn_mesh', constructionHistory=True)
cmds.skinCluster( ['L_shoulder_rigJnt', 'L_forearm_rigJnt', 'L_wrist_rigJnt'], 'L_arm_skn_mesh', dr=4.5, sm=1, name='L_arm_sknCls')
mc.rename('tweak1', 'L_arm_skn_mesh_tweak')

# --- Locking and Hiding ctrls channels
cmds.setAttr( 'L_shoulder_FkJnt.tx', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_shoulder_FkJnt.ty', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_shoulder_FkJnt.tz', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_shoulder_FkJnt.sx', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_shoulder_FkJnt.sy', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_shoulder_FkJnt.sz', lock=True, keyable=False, channelBox=False )
#
cmds.setAttr( 'L_forearm_FkJnt.tx', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_forearm_FkJnt.ty', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_forearm_FkJnt.tz', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_forearm_FkJnt.sx', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_forearm_FkJnt.sy', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_forearm_FkJnt.sz', lock=True, keyable=False, channelBox=False )
#
cmds.setAttr( 'L_wrist_FkJnt.tx', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_wrist_FkJnt.ty', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_wrist_FkJnt.tz', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_wrist_FkJnt.sx', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_wrist_FkJnt.sy', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_wrist_FkJnt.sz', lock=True, keyable=False, channelBox=False )
#
cmds.setAttr( 'L_arm_IkHdl.rx', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_IkHdl.ry', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_IkHdl.rz', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_IkHdl.sx', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_IkHdl.sy', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_IkHdl.sz', lock=True, keyable=False, channelBox=False )
#
cmds.setAttr( 'L_arm_poleVector.rx', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_poleVector.ry', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_poleVector.rz', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_poleVector.sx', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_poleVector.sy', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_poleVector.sz', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_poleVector.visibility', lock=True, keyable=False, channelBox=False )
#
cmds.setAttr( 'L_arm_settings_Ctrl.tx', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_settings_Ctrl.ty', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_settings_Ctrl.tz', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_settings_Ctrl.rx', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_settings_Ctrl.ry', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_settings_Ctrl.rz', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_settings_Ctrl.sx', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_settings_Ctrl.sy', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_settings_Ctrl.sz', lock=True, keyable=False, channelBox=False )
cmds.setAttr( 'L_arm_settings_Ctrl.visibility', lock=True, keyable=False, channelBox=False )
