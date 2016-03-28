import maya.cmds as cmds
import system.utils as utils
from rig.Limb import Limb as Limb

className = 'Arm'


class Arm(Limb):
	'''
	A class for rigging an arm

	Attributes:
		className: The name of the class for external reference
		nddJnts: The number of joints that needs to be selected for the arm being rigged
		args: Optional argument to indicate side in the case arm is a mirrored arm
	'''
	nddJnts = 4

	def __init__(self, *args):
		'''
		Init function that calls the parent class initializer and calls the rig arm function
		in the case we have all the needed joints selected. When an Arm is created from the menu,
		it's always a right arm, when it's mirrored, a parameter indicating side is passed with
		the constructor.
		'''
		# Get the side if the arm
		if not args:
			self.side = 'right'
		else:
			self.side = args[0]
		# Call parent's class initializer
		Limb.__init__(self, self.side)
		self.nddJnts = Arm.nddJnts
		if (len(cmds.ls(sl=True)) == self.nddJnts):
			self.getLayoutPos(cmds.ls(sl=True))
			self.rigArm()
		else:
			cmds.confirmDialog(t='Warning!', m='Please select the 4 bones of the arm.', b='OK', db='OK')

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

	def rigArm(self):
		'''
		The method that creates the actual rig for the arm
		'''
		# Create and orient joints
		utils.createJointChain(self.jntInfo.values())
		# Iterate skeleton dictionary data to create joints, controls and groups
		for key, value in self.jntInfo.iteritems():
			# Create controls and groups
			if key.startswith('fk'):
				for i in range(len(value)):
					if 'End' not in value[i][0]:
						# Create and align control and group
						ctrlName = utils.createControl(value[i][0], self.names)
						# Lock and hide ctrl attributes
						tmpAttrList = ('.tx', '.ty', '.tz', '.sx', '.sy', '.sz')
						utils.lockAndHide(tmpAttrList, ctrlName)
				# Parent controls
				cmds.parent(
							self.names['groupPrefix'] +
							self.names['controlPrefix'] +
							self.names['fkPrefix'] +
							self.names[self.side] +
							self.names['elbow'],
							self.names['controlPrefix'] +
							self.names['fkPrefix'] +
							self.names[self.side] +
							self.names['shoulder']
							)
				cmds.parent(
							self.names['groupPrefix'] +
							self.names['controlPrefix'] +
							self.names['fkPrefix'] +
							self.names[self.side] +
							self.names['wrist'],
							self.names['controlPrefix'] +
							self.names['fkPrefix'] +
							self.names[self.side] +
							self.names['elbow']
							)
				# Deselect to avoid parenting
				cmds.select(d=True)
			elif key.startswith('ik'):
				# Create IK control
				ctrlName = Limb.createIK(
										self,
										self.names['ikPrefix'] +
										self.names[self.side] +
										self.names['shoulder'] +
										self.names['jointSufix'],
										self.names['ikPrefix'] +
										self.names[self.side] +
										self.names['wrist'] +
										self.names['jointSufix'],
										self.names['ikHandle'] +
										self.names[self.side] +
										self.names['armSufix']
										)
				# Lock and hide ctrl attributes
				tmpAttrList = ('.sx', '.sy', '.sz')
				utils.lockAndHide(tmpAttrList, ctrlName)
				# Create pole vector
				ctrlName = Limb.createPV(
										self,
										self.names['ikHandle'] +
										self.names[self.side] +
										self.names['armSufix'],
										self.names['ikPrefix'] +
										self.names[self.side] +
										self.names['shoulder'] +
										self.names['jointSufix'],
										self.names['ikPrefix'] +
										self.names[self.side] +
										self.names['elbow'] +
										self.names['jointSufix'],
										self.names['ikPrefix'] +
										self.names[self.side] +
										self.names['wrist'] +
										self.names['jointSufix']
										)
				# Lock and hide ctrl attributes
				tmpAttrList = ('.rx', '.ry', '.rz', '.sx', '.sy', '.sz')
				utils.lockAndHide(tmpAttrList, ctrlName)
				# Deselect to avoid parenting
				cmds.select(d=True)
			elif key.startswith('bn'):
				jntName = (
						self.names['bindPrefix'] +
						self.names[self.side] +
						self.names['wrist'] +
						self.names['jointSufix']
						)
				# Create blend ctrl
				ctrlName = utils.createControl(jntName, self.names)
				# Rename and parent constraint control and group
				ctrlName = cmds.rename(
									ctrlName,
									self.names['controlPrefix'] +
									self.names[self.side] +
									self.names['armSufix']
									)
				grpName = cmds.rename(cmds.listRelatives(
														ctrlName, p=True),
														self.names['groupPrefix'] +
														self.names[self.side] +
														self.names['armSufix']
														)
				cmds.delete(jntName + '_orientConstraint1')
				cmds.parentConstraint(jntName, grpName)
				# Scale control
				cmds.setAttr(grpName + '.sx', 2)
				cmds.setAttr(grpName + '.sy', 2)
				cmds.setAttr(grpName + '.sz', 2)
				# Lock and hide ctrl attributes
				tmpAttrList = ('.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz')
				utils.lockAndHide(tmpAttrList, ctrlName)
				# Deselect to avoid parenting
				cmds.select(d=True)
		# Connect Ik and Fk to bind joints
		Limb.parentFKIKChains(self, self.jntInfo)
		# Create blend nodes
		Limb.createArmFKIKBlend(self, self.jntInfo)
