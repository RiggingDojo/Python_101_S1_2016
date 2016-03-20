import maya.cmds as cmds
import system.utils as utils
from rig.Limb import Limb as Limb


class Arm(Limb):

	def __init__(self):
		'''
		Init function that just calls parent class initializer
		'''
		Limb.__init__(self)

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
						if ctrlName:
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
