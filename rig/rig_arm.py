import maya.cmds as cmds

# Create Ik joints
cmds.joint( name="ik_shoulder_jnt", p=[-0.2, 0, 8.5])
cmds.joint( name="ik_elbow_jnt", p=[-4.0, 0, 0.04])
cmds.joint( name="ik_wrist_jnt", p=[0.15, 0, -4.7])
cmds.joint( name="ik_wristEnd_jnt", p=[-0.07, 0, -7.4])
cmds.select("ik_shoulder_jnt", hierarchy=True)
cmds.joint( edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="yup")
cmds.select(deselect=True)

# Create Fk joints
cmds.joint( name="Fk_shoulder_jnt", p=[-0.2, 0, 8.5])
cmds.joint( name="Fk_elbow_jnt", p=[-4.0, 0, 0.04])
cmds.joint( name="Fk_wrist_jnt", p=[0.15, 0, -4.7])
cmds.joint( name="Fk_wristEnd_jnt", p=[-0.07, 0, -7.4])
cmds.select("Fk_shoulder_jnt", hierarchy=True)
cmds.joint( edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="yup")
cmds.select(deselect=True)

# Create rig joints
cmds.joint( name="rig_shoulder_jnt", p=[-0.2, 0, 8.5])
cmds.joint( name="rig_elbow_jnt", p=[-4.0, 0, 0.04])
cmds.joint( name="rig_wrist_jnt", p=[0.15, 0, -4.7])
cmds.joint( name="rig_wristEnd_jnt", p=[-0.07, 0, -7.4])
cmds.select("rig_shoulder_jnt", hierarchy=True)
cmds.joint( edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="yup")
cmds.select(deselect=True)

# Create Ik Rig

# Create Ik Handle
cmds.ikHandle( name="ikh_arm", startJoint="ik_shoulder_jnt", endEffector="ik_wrist_jnt", solver="ikRPsolver", priority=2, weight=1 )

# Create ik Control
# Get ws position of wrist joint
pos = cmds.xform("ik_wrist_jnt", query=True, translation=True, worldSpace=True)
print pos

# Create and empty group
cmds.group( em=True, name="grp_ctrl_ikWrist" )

# Create a circle for control object
cmds.circle( name="ctrl_ikWrist", normal=(0, 0, 1), center=(0, 0, 0), sweep=360, radius=2 )

# Parent the control to the group
cmds.parent("ctrl_ikWrist", "grp_ctrl_ikWrist")

# Move the group to the joint
cmds.xform("grp_ctrl_ikWrist", translation=pos, worldSpace=True)
# Parent ikh to ctrl
cmds.parent("ikh_arm", "ctrl_ikWrist")


# Create Fk Rig

# Create fk Control
# Store the name of the fkjoints in list
fkjointNames = ["Fk_shoulder", "Fk_elbow", "Fk_wrist"]
print fkjointNames

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

# Zero xforms grp_ctrl_Fk_shoulder
cmds.setAttr ("grp_ctrl_Fk_shoulder.rotateZ", 0)
cmds.setAttr ("grp_ctrl_Fk_shoulder.translateX", 0)
cmds.setAttr ("grp_ctrl_Fk_shoulder.translateY", 0)
cmds.setAttr ("grp_ctrl_Fk_shoulder.translateZ", 0)
cmds.setAttr ("grp_ctrl_Fk_shoulder.rotateX", 0)
cmds.setAttr ("grp_ctrl_Fk_shoulder.rotateY", 0)
cmds.setAttr ("grp_ctrl_Fk_shoulder.rotateX", 90)
cmds.setAttr ("grp_ctrl_Fk_shoulder.rotateZ", 90)
# Zero xforms grp_ctrl_Fk_elbow
cmds.setAttr ("grp_ctrl_Fk_elbow.rotateZ", 0)
cmds.setAttr ("grp_ctrl_Fk_elbow.translateX", 0)
cmds.setAttr ("grp_ctrl_Fk_elbow.translateY", 0)
cmds.setAttr ("grp_ctrl_Fk_elbow.translateZ", 0)
cmds.setAttr ("grp_ctrl_Fk_elbow.rotateX", 0)
cmds.setAttr ("grp_ctrl_Fk_elbow.rotateY", 0)
cmds.setAttr ("grp_ctrl_Fk_elbow.rotateX", 90)
cmds.setAttr ("grp_ctrl_Fk_elbow.rotateZ", 90)
# Zero xforms grp_ctrl_Fk_wrist
cmds.setAttr ("grp_ctrl_Fk_wrist.rotateZ", 0)
cmds.setAttr ("grp_ctrl_Fk_wrist.translateX", 0)
cmds.setAttr ("grp_ctrl_Fk_wrist.translateY", 0)
cmds.setAttr ("grp_ctrl_Fk_wrist.translateZ", 0)
cmds.setAttr ("grp_ctrl_Fk_wrist.rotateX", 0)
cmds.setAttr ("grp_ctrl_Fk_wrist.rotateY", 0)
cmds.setAttr ("grp_ctrl_Fk_wrist.rotateX", 90)
cmds.setAttr ("grp_ctrl_Fk_wrist.rotateZ", 90)

# freeze xforms
cmds.select("grp_ctrl_Fk_shoulder", "grp_ctrl_Fk_elbow", "grp_ctrl_Fk_wrist")
cmds.makeIdentity( apply=True, translate=1, rotate=1, scale=1, normal=0, preserveNormals=1)

# Unparent control group from joint
cmds.Unparent("grp_ctrl_Fk_shoulder")
cmds.Unparent("grp_ctrl_Fk_elbow")
cmds.Unparent("grp_ctrl_Fk_wrist")


# Parent ctrl
cmds.parent("grp_ctrl_Fk_wrist", "ctrl_Fk_elbow")
cmds.parent("grp_ctrl_Fk_elbow", "ctrl_Fk_shoulder")

# Connect rotation xform of ctrl to the joint
cmds.connectAttr("ctrl_Fk_shoulder.rotate", "Fk_shoulder_jnt.rotate", force=True)
cmds.connectAttr("ctrl_Fk_elbow.rotate", "Fk_elbow_jnt.rotate", force=True)
cmds.connectAttr("ctrl_Fk_wrist.rotate", "Fk_wrist_jnt.rotate", force=True)



# Connect Ik and Fk to Rig joints
# Create null to use as switch for IKFK controls
cmds.spaceLocator(name="IKFK", p=[0,0,0])
cmds.select("IKFK")
cmds.addAttr( ln="FK", min=0, max=1, dv=0)
cmds.setAttr( "IKFK.FK", edit=True, keyable=True)
cmds.addAttr( ln="IK", min=0, max=1 ,dv=0)
cmds.setAttr( "IKFK.IK", edit=True, keyable=True)


# Create orient constraints
cmds.select("ik_wrist_jnt")
cmds.select("Fk_wrist_jnt", add=True)
cmds.select("rig_wrist_jnt", add=True)
cmds.OrientConstraint( offset=[0, 0, 0], weight=1) # Orientation constraint

cmds.select("ik_elbow_jnt")
cmds.select("Fk_elbow_jnt", add=True)
cmds.select("rig_elbow_jnt", add=True)
cmds.OrientConstraint( offset=[0, 0, 0], weight=1) # Orientation constraint

cmds.select("ik_shoulder_jnt")
cmds.select("Fk_shoulder_jnt", add=True)
cmds.select("rig_shoulder_jnt", add=True)
cmds.OrientConstraint( offset=[0, 0, 0], weight=1) # Orientation constraint

# Select orientation constraint and link to IKFK null
cmds.connectAttr( "IKFK.FK", "rig_wrist_jnt_orientConstraint1.Fk_wrist_jntW1", force=True)
cmds.connectAttr( "IKFK.IK", "rig_wrist_jnt_orientConstraint1.ik_wrist_jntW0", force=True)
cmds.connectAttr( "IKFK.FK", "rig_elbow_jnt_orientConstraint1.Fk_elbow_jntW1", force=True)
cmds.connectAttr( "IKFK.IK", "rig_elbow_jnt_orientConstraint1.ik_elbow_jntW0", force=True)
cmds.connectAttr( "IKFK.FK", "rig_shoulder_jnt_orientConstraint1.Fk_shoulder_jntW1", force=True)
cmds.connectAttr( "IKFK.IK", "rig_shoulder_jnt_orientConstraint1.ik_shoulder_jntW0", force=True)






