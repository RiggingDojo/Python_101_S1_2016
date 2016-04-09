import maya.cmds as cmds
import system.utils as utils
import json
import os
from rig.Leg import Leg as Leg
from functools import partial
reload(utils)

className = 'MirrorLeg'


class MirrorLeg():
	'''
	A class for mirroring an Arm rig

	Attributes:
		className: The name of the class for external reference
		nddJnts: The number of joints that needs to be selected for the arm being rigged
		armInstance: Instance of the mirrored arm

	'''
	nddJnts = 4
	fileNames = os.environ['RDOJO_DATA'] + 'leg_labels.json'

	def __init__(self, side):
		'''
		Init function that creates an instance of an Leg and mirrors the joint chain
		in the case we have selected the needed joints
		'''
		self.nddJnts = MirrorLeg.nddJnts
		self.axis = ''
		self.side = side
		self.mirrorJntList = []
		# Get the path for the files with limb data
		self.names = json.loads(utils.readJson(self.fileNames))
		if (len(cmds.ls(sl=True)) == self.nddJnts):
			self.createRadioButtons(cmds.ls(sl=True))
		else:
			cmds.confirmDialog(t='Warning!', m='Please select the 4 bones of the leg.', b='OK', db='OK')

	def createRadioButtons(self, jntList):
		# Check to see if our window exists
		if cmds.window('utility', ex=True):
			cmds.deleteUI('utility')
		# Create our window
		window = cmds.window('utility', wh=(200, 200), t='Mirror Axis', rtf=1, s=False)
		cmds.setParent(m=True)
		# Create a main layout
		cmds.columnLayout(w=200, h=200, cw=10, rs=8, co=['both', 2])
		# Axis Controls
		cmds.radioCollection()
		xAxis = cmds.radioButton(l='XY')
		yAxis = cmds.radioButton(l='YZ')
		zAxis = cmds.radioButton(l='XZ')
		# Button
		cmds.button(
					l='Mirror Axis',
					w=200,
					h=40,
					c=partial(self.mirrorButton, xAxis, yAxis, zAxis, jntList[0], self.side)
					)
		# Show window
		cmds.showWindow(window)

	def mirrorButton(self, xAxis, yAxis, zAxis, joint, side, *args):
		'''
		Function to mirror an arm with the referenced joints. Mirrors the selected joints, and selects
		the newly created joint chain so we are set to perform the arm rigging

		param joint: The first joint of the chain to be mirrored
		type joint: string
		'''
		# Get the selected axis
		if cmds.radioButton(xAxis, q=True, sl=True):
			self.axis = 'xy'
		elif cmds.radioButton(yAxis, q=True, sl=True):
			self.axis = 'yz'
		elif cmds.radioButton(zAxis, q=True, sl=True):
			self.axis = 'xz'
		# Uses the utils function that mirrors a joint chain
		self.mirrorJntList = utils.mirrorJointChain(joint, self.axis, self.names, side)
		# Deselect and select the mirrored chain
		cmds.select(d=True)
		cmds.select(self.mirrorJntList)
		# Filter objects from the selection to avoid getting constraints, etc
		self.mirrorJntList = cmds.ls(self.mirrorJntList, typ=['joint'])
		# Deselect and select the mirrored chain again
		cmds.select(d=True)
		cmds.select(self.mirrorJntList)
		# Creates the new instance of the arm rig
		Leg(side)
