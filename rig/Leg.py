import maya.cmds as cmds
import system.utils as utils
from rig.Limb import Limb as Limb
import os
reload(utils)

className = 'Leg'


class Leg(Limb):
	'''
	A class for rigging a leg

	Attributes:
		className: The name of the class for external reference
		nddJnts: The number of joints that needs to be selected for the arm being rigged
		args: Optional argument to indicate side in the case leg is a mirrored leg
	fileNames: The path to the json file with the default labels for the limb
		filePos: The path to the json file with the default positions for the limb
	'''
	nddJnts = 4
	fileNames = os.environ['RDOJO_DATA'] + 'leg_labels.json'
	filePos = os.environ['RDOJO_DATA'] + 'leg_positions.json'

	def __init__(self, side):
		'''
		Init function that calls the parent class initializer and calls the rig leg function
		in the case we have all the needed joints selected. When a Leg is created from the menu,
		it's always a right leg, when it's mirrored, a parameter indicating side is passed with
		the constructor.
		'''
		# Get the side if the leg
		self.side = side
		# Call parent's class initializer
		Limb.__init__(self, self.side, self.fileNames, self.filePos)
		self.nddJnts = Leg.nddJnts
		if (len(cmds.ls(sl=True)) == self.nddJnts):
			Limb.getLayoutPos(self, cmds.ls(sl=True))
			self.rigLeg()
		else:
			cmds.confirmDialog(t='Warning!', m='Please select the 4 bones of the leg.', b='OK', db='OK')

	def createFootRoll(self):
		print 'Great foot roll'

	def rigLeg(self):
		self.createFootRoll()
		print 'Great leg rig'

