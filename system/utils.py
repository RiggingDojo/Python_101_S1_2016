import maya.cmds as cmds
import json


def writeJson(filename, data):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)


def readJson(filename):
	with open(filename, 'r') as infile:
		data = (infile.read())
	return data


def createDict(keys, values, names, side):
	"""
	A function that creates a dictionary from two lists

	:param keys: A list with the keys for the dictionary
	:param values: A list with the values for each keys
	:param names: A list with the names convention for the data
	:param side: The side of the body for the limb
	:type keys: list
	:type values: list
	:type names: list
	:type side: string
	:rtype: dict
	"""
	# Declare temp variables
	dict = {}
	tmpJntList = []
	# Feed data into dictionary
	for label in keys:
		tmpJntList = []
		for i in range(len(values)):
			newName = label + names[side] + values[i][0] + names['jointSufix']
			tmpJntList.append([newName, values[i][1]])
		dict[label] = tmpJntList
	return dict


def createJointChain(jntList):
	"""
	A function that creates chains of joints and
	orients them with their x axis following the chain and the y axis up

	:param jntList: A list with the data for all the joints
	:type jntList: list
	"""
	# Deselect everything for the joint command to work properly
	cmds.select(d=True)
	# Create Joints
	for item in jntList:
		[cmds.joint(n=item[i][0], p=item[i][1]) for i in range(len(item))]
		cmds.select(d=True)
	# Orient joints with their 'x' axis pointing to the next one in the hierarchy and 'y' axis as up
	for item in jntList:
		[cmds.joint(item[i][0], edit=True, zso=True, oj='xyz', sao='yup') for i in range(len(item))]


def createControl(jntName, names):
	"""
	A function that creates an animation control nested into a group and
	aligns and constraints them to a joint. Returns de name of the newly created control

	:param jntName: The name of the joint for which the control will be created
	:param names: A list with the names convention for the data
	:type jntName: string
	:type names: list
	:rtype: string
	"""
	# Get control info
	grpPos = cmds.xform(jntName, q=True, t=True, ws=True)
	grpName = names['groupPrefix'] + names['controlPrefix'] + jntName[:-len(names['jointSufix'])]
	grpRot = cmds.xform(jntName, q=True, ro=True, ws=True)
	ctrlName = names['controlPrefix'] + jntName[:-len(names['jointSufix'])]
	# Create and orient control and control group
	cmds.group(em=True, name=grpName)
	cmds.xform(grpName, ro=grpRot, ws=True)
	cmds.circle(n=ctrlName, nr=(1, 0, 0), c=(0, 0, 0))
	cmds.delete(ctrlName, constructionHistory=True)
	cmds.parent(ctrlName, grpName)
	cmds.setAttr(ctrlName + '.rotateX', 0)
	cmds.setAttr(ctrlName + '.rotateY', 0)
	cmds.setAttr(ctrlName + '.rotateZ', 0)
	cmds.xform(grpName, t=grpPos, ws=True)
	cmds.orientConstraint(ctrlName, jntName)
	return ctrlName


def lockAndHide(attrList, controlName):
	"""
	A function that hides and locks the listed attributes from a control

	:param attrList: A list with the attributes to be hiden and locked
	:param controlName: The name of the affected control
	:type attrList: list
	:type controlName: string
	"""
	[cmds.setAttr(controlName + attr, e=True, l=True, k=False, cb=False) for attr in attrList]


def mirrorJointChain(joint, axis, names):
	"""
	A function that mirrors a joint chain based in the passed axis. Returns the mirrored chain

	:param joint: The first joint of the chain to be mirrored
	:param axis: The axis to perform the mirror on
	:type joint: string
	:type axis: string
	:rtype mirrorJntList: list
	"""
	mirrorJntList = []
	# Get the selected axis and return the mirrored chain depending on the axis
	if axis == 'xy':
		mirrorJntList = cmds.mirrorJoint(joint, mirrorXY=True, mirrorBehavior=True, searchReplace=('R', 'L'))
	elif axis == 'yz':
		mirrorJntList = cmds.mirrorJoint(joint, mirrorYZ=True, mirrorBehavior=True, searchReplace=('R', 'L'))
	elif axis == 'xz':
		mirrorJntList = cmds.mirrorJoint(joint, mirrorXZ=True, mirrorBehavior=True, searchReplace=('R', 'L'))
	return mirrorJntList
