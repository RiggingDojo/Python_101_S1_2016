import maya.cmds as cmds

class Arm:

	def __init__(self, jntPositions, jointNames):
		self.side = 'right'
		self.jntPos = jntPositions
		self.names = jointNames
		self.jntChains = (self.names['ikPrefix'], self.names['fkPrefix'], self.names['bindPrefix']) 
		self.jntInfo = self.createDict(self.jntChains, self.jntPos)

	def createDict(self, keys, values):
		dict = {}
		# Feed data into dictionary
		for label in keys:
			tmpJntList = []
			for i in range(len(values)):
				newName = label + self.names[self.side] + values[i][0] + self.names['jointSufix']
				tmpJntList.append([newName, values[i][1]])
			dict[label] = tmpJntList
		return dict

	def createJointChain(self, jntList):
		# Create Joints
		for item in jntList:
			for i in range(len(item)):
				cmds.joint(n=item[i][0], p=item[i][1])
			cmds.select(d = True)
		# Orient joints
		for item in jntList:
			for i in range(len(item)):
				cmds.joint(item[i][0], edit=True, zso=True, oj='xyz', sao='yup')

	def createControl(self, jointName):
		# Get control info
		grpPos = cmds.xform(jointName, q=True, t=True, ws=True)
		grpName = self.names['groupPrefix'] + self.names['controlPrefix'] + jointName[:-len(self.names['jointSufix'])]
		grpRot = cmds.xform(jointName, q=True, ro=True, ws=True)
		ctrlName = self.names['controlPrefix'] + jointName[:-len(self.names['jointSufix'])]
		# Create and orient control and control group
		cmds.group(em=True, name=grpName)
		cmds.xform(grpName, ro=grpRot, ws=True)
		cmds.circle(n=ctrlName, nr=(1, 0, 0), c=(0, 0, 0))
		cmds.delete(ctrlName, constructionHistory=True)
		cmds.parent(ctrlName, grpName)
		cmds.setAttr(ctrlName + '.rotateY', 0)
		cmds.xform(grpName, t=grpPos, ws=True)
		cmds.orientConstraint(ctrlName, jointName)
		return ctrlName

	def createIK(self, jntStart, jntEnd, ikHandleName):
		# Get control info
		grpPos = cmds.xform(jntEnd, q=True, t=True, ws=True)
		grpName = self.names['groupPrefix'] + self.names['controlPrefix'] + jntEnd[:-len(self.names['jointSufix'])]
		grpRot = cmds.xform(jntEnd, q=True, ro=True, ws=True)
		ctrlName = self.names['controlPrefix'] + jntEnd[:-len(self.names['jointSufix'])]
		# Ik handle
		cmds.ikHandle(n=ikHandleName, ee=jntEnd, sj=jntStart, sol='ikRPsolver', p=2, w=1 )
		# Create ik control
		self.createControl(jntEnd)
		# Parent ikhandle to ctrl
		cmds.parent(ikHandleName, ctrlName)
		return ctrlName

	def lockAndHide(self, attrList, controlName):
		for attr in attrList:
			cmds.setAttr(controlName + attr, edit=True,  lock=True, keyable=False, channelBox=False)    
	
	def createPV(self, ikHandleName, jointName):
		PVName = self.names['ikPrefix'] + self.names['poleVector'] + self.names[self.side] + self.names['armSufix']
		pos = cmds.xform(jointName, q=True, t=True, ws=True)
		pos[0] -= 2
		cmds.spaceLocator(n=PVName)
		cmds.xform(PVName, ws=True, t=pos)
		cmds.poleVectorConstraint(PVName, ikHandleName)
		return PVName

	def parentFKIKChains(self, dict):
		for key, value in dict.iteritems():
			for i in range(len(value)):
				jntName = value[i][0]
				# If joint is end joint, we don't want to parent it
				if 'End' not in jntName:
					if key.startswith('ik'):
						jntBindName = jntName.replace(self.names['ikPrefix'], self.names['bindPrefix'])
						cmds.parentConstraint(jntName, jntBindName, weight = 0)
					elif key.startswith('fk'):
						jntBindName = jntName.replace(self.names['fkPrefix'], self.names['bindPrefix'])
						cmds.parentConstraint(jntName, jntBindName)	
	
	def createArmFKIKBlend(self, dict):
		ctrlName = self.names['controlPrefix'] + self.names[self.side] + self.names['armSufix']
		# Create blend attribute
		cmds.select(d=True)
		cmds.select(ctrlName)
		cmds.addAttr(ctrlName, ln=self.names['blendingNode'], at='long', min=0, max=10, dv=0)
		cmds.setAttr(ctrlName + '.' + self.names['blendingNode'], edit=True, keyable=True)
		cmds.setAttr(ctrlName + '.' + self.names['blendingNode'], 0)
		# Create nodes to perform the blend
		multDivNode = cmds.createNode('multiplyDivide', n=self.names['multiplyDividePrefix'] + self.names['blendingNode'])
		cmds.connectAttr(ctrlName + '.' + self.names['blendingNode'], multDivNode + '.input1X')
		cmds.setAttr(multDivNode + '.input2X', 10)
		plusMinusNode = cmds.createNode('plusMinusAverage', n=self.names['plusMinusPrefix'] + self.names['blendingNode'])
		cmds.setAttr(plusMinusNode + '.operation', 2)
		cmds.setAttr(plusMinusNode + '.input1D[0]', 100)
		cmds.connectAttr(multDivNode + '.output.outputX', plusMinusNode + '.input1D[1]')
		for key, value in dict.iteritems():
			for i in range(len(value)):
				jntName = value[i][0]
				if 'End' not in jntName:
					if key.startswith('ik'):
						jntBindName = jntName.replace(self.names['ikPrefix'], self.names['bindPrefix'])
						cmds.connectAttr(multDivNode + '.output.outputX', jntBindName + '_parentConstraint1.' + jntName + 'W0')
					elif key.startswith('fk'):
						jntBindName = jntName.replace(self.names['fkPrefix'], self.names['bindPrefix'])
						cmds.connectAttr(plusMinusNode + '.output1D', jntBindName + '_parentConstraint1.' + jntName + 'W1')		

	def mirrorArm(self):
		# Prepare info for the mirroring
		self.jntPos = self.jntPos
		self.side = 'left'
		self.jntInfo = self.createDict(self.jntChains, self.jntPos)
		# Execute rig function
		self.rigArm();

	def rigArm(self):
		# Create and orient joints
		self.createJointChain(self.jntInfo.values())
		# Iterate skeleton dictionary data to create joints, controls and groups       
		for key, value in self.jntInfo.iteritems():
			# Create controls and groups
			if key.startswith('fk'):
				for i in range(len(value)):
					if 'End' not in value[i][0]:
						# Create and align control and group
						ctrlName = self.createControl(value[i][0])
						if ctrlName:
							# Lock and hide ctrl attributes
							tmpAttrList = ('.tx', '.ty','.tz','.sx','.sy','.sz')
							self.lockAndHide(tmpAttrList, ctrlName)
				# Parent cntrls
				cmds.parent(self.names['groupPrefix'] + self.names['controlPrefix'] + self.names['fkPrefix'] + self.names[self.side] + self.names['elbow'], self.names['controlPrefix'] + self.names['fkPrefix'] + self.names[self.side] + self.names['shoulder'])
				cmds.parent(self.names['groupPrefix'] + self.names['controlPrefix'] + self.names['fkPrefix'] + self.names[self.side] + self.names['wrist'], self.names['controlPrefix'] + self.names['fkPrefix'] + self.names[self.side] + self.names['elbow'])
				# Deselect to avoid parenting
				cmds.select(d=True)
			elif key.startswith('ik'):
				# Create IK control
				ctrlName = self.createIK(self.names['ikPrefix'] + self.names[self.side] + self.names['shoulder'] + self.names['jointSufix'], self.names['ikPrefix'] + self.names[self.side] + self.names['wrist'] + self.names['jointSufix'], self.names['ikHandle'] + self.names[self.side] + self.names['armSufix'])
				# Lock and hide ctrl attributes
				tmpAttrList = ('.sx','.sy','.sz')
				self.lockAndHide(tmpAttrList, ctrlName)
				# Create pole vector
				ctrlName = self.createPV(self.names['ikHandle'] + self.names[self.side] + self.names['armSufix'], self.names['ikPrefix'] + self.names[self.side] + self.names['elbow'] + self.names['jointSufix'])
				# Lock and hide ctrl attributes
				tmpAttrList = ('.rx', '.ry','.rz','.sx','.sy','.sz')
				self.lockAndHide(tmpAttrList, ctrlName)
				# Deselect to avoid parenting
				cmds.select(d=True)
			elif key.startswith('bn'):
				jntName = self.names['bindPrefix'] + self.names[self.side] + self.names['wrist'] + self.names['jointSufix']
				# Create blend ctrl
				ctrlName = self.createControl(jntName)
				# Rename and parent constraint control and group
				ctrlName = cmds.rename(ctrlName, self.names['controlPrefix'] + self.names[self.side] + self.names['armSufix'])
				grpName = cmds.rename(cmds.listRelatives(ctrlName, parent=True), self.names['groupPrefix'] + self.names[self.side] + self.names['armSufix'])
				cmds.parentConstraint(jntName, grpName)					
				# Scale control
				cmds.setAttr(grpName + '.sx', 2)
				cmds.setAttr(grpName + '.sy', 2)
				cmds.setAttr(grpName + '.sz', 2)
				# Lock and hide ctrl attributes
				tmpAttrList = ('.tx','.ty','.tz', '.rx','.ry','.rz', '.sx','.sy','.sz')
				self.lockAndHide(tmpAttrList, ctrlName)
				# Deselect to avoid parenting
				cmds.select(d=True)
		# Connect Ik and Fk to bind joints
		self.parentFKIKChains(self.jntInfo)
		# Create blend nodes
		self.createArmFKIKBlend(self.jntInfo)
