import system.utils as utils
from rig.Limb import Limb as Limb
import os

className = 'LayoutLeg'


class LayoutLeg(Limb):
	'''
	A class for laying out the joint chain for an leg rig

	Attributes:
		className: The name of the class for external reference
	'''

	fileNames = os.environ['RDOJO_DATA'] + 'leg_labels.json'
	filePos = os.environ['RDOJO_DATA'] + 'leg_positions.json'

	def __init__(self, side):
		'''
		Init function that just calls parent class initializer
		'''
		self.side = side
		Limb.__init__(self, self.side, self.fileNames, self.filePos)
		self.layoutLeg()

	def layoutLeg(self):
		'''
		The method that creates the layout for the leg
		'''
		# Iterate skeleton dictionary data to create joints, controls and groups
		for key, value in self.jntInfo.iteritems():
			# Create controls and groups
			if key.startswith('bn'):
				for i in range(len(value)):
					jntList = []
					jntList.append(value)
				# Create and orient joints
				utils.createJointChain(jntList)
