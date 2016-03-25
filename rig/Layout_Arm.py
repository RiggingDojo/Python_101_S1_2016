import system.utils as utils
from rig.Limb import Limb as Limb

className = 'Layout_Arm'


class Layout_Arm(Limb):
	'''
	A class for laying out the joint chain for an arm rig

	Attributes:
		className: The name of the class for external reference
	'''
	def __init__(self):
		'''
		Init function that just calls parent class initializer
		'''
		Limb.__init__(self)
		self.layoutArm()

	def layoutArm(self):
		'''
		The method that creates the actual layout for the arm
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
