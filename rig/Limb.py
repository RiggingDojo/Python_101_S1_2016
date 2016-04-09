import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import system.utils as utils
import json
reload(utils)


class Limb:
	'''
	A class for creating rig sections such as legs, arms
	'''
	def __init__(self, side, fileNames, filePos):
		'''
		Initializes the class with its necessary attributes

		Attributes:
			side: The side of the body where the limb will be placed
			jntPos: List with the positions of the bones
			fileNames: The path to the json file with the default labels for the limb
			filePos: The path to the json file with the default positions for the limb
		'''
		# Initialize attributes
		self.side = side
		self.jntPos = json.loads(utils.readJson(filePos))
		self.names = json.loads(utils.readJson(fileNames))
		self.jntChains = (self.names['ikPrefix'], self.names['fkPrefix'], self.names['bindPrefix'])
		self.jntInfo = utils.createDict(self.jntChains, self.jntPos, self.names, self.side)

	def getLayoutPos(self, jntList):
		'''
		Function that acquires the positions of the bones of the layout object and adds them
		to the data dictionary, replacing the default positions

		param jntList: The list with the bones of the layout object
		type jntList: list
		'''
		# Get position of the selected joints and then delete them
		jntPosList = []
		jntPosList = [cmds.xform(jnt, q=True, ws=True, t=True) for jnt in jntList]
		cmds.delete()
		# Replace default positions in the dictionary for the new ones
		for key, value in self.jntInfo.iteritems():
			for i in range(len(value)):
				value[i][1] = jntPosList[i]

	def createIK(self, jntStart, jntEnd, ikHandleName):
		'''
		Function that creates an IK control for the given joints

		:param jntStart: The name of the start joint
		:param jntEnd: The name of the end joint
		:param ikHandleName: The name of the ik control
		:type jntStart: string
		:type jntEnd: string
		:type ikHandleName: string
		:rtype: string
		'''
		ctrlName = self.names['controlPrefix'] + jntEnd[:-len(self.names['jointSufix'])]
		# Ik handle
		cmds.ikHandle(n=ikHandleName, ee=jntEnd, sj=jntStart, sol='ikRPsolver', p=2, w=1)
		# Create ik control
		utils.createControl(jntEnd, self.names)
		# Parent ikhandle to ctrl
		cmds.parent(ikHandleName, ctrlName)
		return ctrlName

	def calculatePVPosition(self, jntStart, jntMid, jntEnd):
		'''
		Function that uses OpenMaya vector methods to calculate the position of the PV
		based in the vectors of the 3 joints of the IK chain. Returns a list
		with the 3D coord for the PV

		:param jntStart: The name of the start joint
		:param jntMid: The name of the mid joint
		:param jntEnd: The name of the end joint
		:type jntStart: string
		:type jntMid: string
		:type jntEnd: string
		:rtype: list
		'''
		# Calculates the position of joints
		start = cmds.xform(jntStart, q=True, ws=True, t=True)
		mid = cmds.xform(jntMid, q=True, ws=True, t=True)
		end = cmds.xform(jntEnd, q=True, ws=True, t=True)
		startV = OpenMaya.MVector(start[0], start[1], start[2])
		midV = OpenMaya.MVector(mid[0], mid[1], mid[2])
		endV = OpenMaya.MVector(end[0], end[1], end[2])
		startEnd = endV - startV
		startMid = midV - startV
		dotP = startMid * startEnd
		proj = float(dotP) / float(startEnd.length())
		startEndN = startEnd.normal()
		projV = startEndN * proj
		arrowV = startMid - projV
		arrowV *= 0.5
		finalV = arrowV + midV
		return ([finalV.x, finalV.y, finalV.z])

	def createPV(self, ikHandleName, jntStart, jntMid, jntEnd):
		'''
		Function that creates the Pole Vector for an IK control

		:param ikHandleName: The names of the IK control
		:param jntStart: The name of the start joint
		:param jntMid: The name of the mid joint
		:param jntEnd: The name of the end joint
		:type jntStart: string
		:type jntMid: string
		:type jntEnd: string
		:rtype: string
		'''
		PVName = (
				self.names['ikPrefix'] +
				self.names['poleVector'] +
				self.names[self.side] +
				self.names['armSufix']
				)
		pos = self.calculatePVPosition(jntStart, jntMid, jntEnd)
		cmds.spaceLocator(n=PVName)
		cmds.xform(PVName, ws=True, t=pos)
		cmds.poleVectorConstraint(PVName, ikHandleName)
		return PVName

	def parentFKIKChains(self, dict):
		'''
		Function that parents a chain of bind bones to a FK chain and to an IK chain

		:param dict: Dictionary with the data of the 3 chains
		:type dict: dict
		'''
		for key, value in dict.iteritems():
			for i in range(len(value)):
				jntName = value[i][0]
				# Parent all bind joints except the end joint to the FK and IK chains, prioritizing the FK chain
				if 'End' not in jntName:
					if key.startswith('ik'):
						jntBindName = jntName.replace(self.names['ikPrefix'], self.names['bindPrefix'])
						cmds.parentConstraint(jntName, jntBindName, weight=0)
					elif key.startswith('fk'):
						jntBindName = jntName.replace(self.names['fkPrefix'], self.names['bindPrefix'])
						cmds.parentConstraint(jntName, jntBindName)

	def createArmFKIKBlend(self, dict):
		'''
		Function that creates the necessary nodes to perform an IK/FK blend

		:param dict: Dictionary with the data of the 3 chains
		:type dict: dict
		'''
		ctrlName = self.names['controlPrefix'] + self.names[self.side] + self.names['armSufix']
		# Create blend attribute
		cmds.select(d=True)
		cmds.select(ctrlName)
		cmds.addAttr(ctrlName, ln=self.names['blendingNode'], at='long', min=0, max=10, dv=0)
		cmds.setAttr(ctrlName + '.' + self.names['blendingNode'], edit=True, keyable=True)
		cmds.setAttr(ctrlName + '.' + self.names['blendingNode'], 0)
		# Create nodes to perform the blend
		multDivNode = cmds.createNode(
									'multiplyDivide',
									n=(self.names['multiplyDividePrefix'] + self.names[self.side] + self.names['blendingNode'])
									)
		cmds.connectAttr(ctrlName + '.' + self.names['blendingNode'], multDivNode + '.input1X')
		cmds.setAttr(multDivNode + '.input2X', 10)
		plusMinusNode = cmds.createNode(
									'plusMinusAverage',
									n=(self.names['plusMinusPrefix'] + self.names[self.side] + self.names['blendingNode'])
									)
		cmds.setAttr(plusMinusNode + '.operation', 2)
		cmds.setAttr(plusMinusNode + '.input1D[0]', 100)
		cmds.connectAttr(multDivNode + '.output.outputX', plusMinusNode + '.input1D[1]')
		for key, value in dict.iteritems():
			for i in range(len(value)):
				jntName = value[i][0]
				if 'End' not in jntName:
					if key.startswith('ik'):
						jntBindName = jntName.replace(self.names['ikPrefix'], self.names['bindPrefix'])
						cmds.connectAttr(
										multDivNode + '.output.outputX',
										jntBindName + '_parentConstraint1.' + jntName + 'W0'
										)
					elif key.startswith('fk'):
						jntBindName = jntName.replace(self.names['fkPrefix'], self.names['bindPrefix'])
						cmds.connectAttr(
										plusMinusNode + '.output1D',
										jntBindName + '_parentConstraint1.' + jntName + 'W1'
										)
