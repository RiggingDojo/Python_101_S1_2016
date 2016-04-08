import maya.cmds as cmds

sel = cmds.ls(sl=True)
print sel

def reOrient(sel):
	for i in sel:
		cmds.joint(i, edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True)

reOrient(sel)		