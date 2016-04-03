import maya.cmds as cmds
import json
import os
import system.utils as utils

# Class Attr
classname = 'Rig_Arm'
lytfile = 'arm.json'
numjnts = 4


class Rig_Arm:
	'''creates instance of arm, default is right arm blah blha blha blha'''

	def __init__( self ):
		# Get our joint lists from a json file.
		data_path = os.environ["RDOJO_DATA"] + 'rig/arm.json'
		#data_path = "C:/Users/Bears/Documents/GitHub/Python_101_S1_2016/data/" + 'rig/arm.json'
		# Use our readJson function
		data = utils.readJson( data_path )
		# Load the json in a dictionary
		self.module_info = json.loads( data )
		# stores data to be modified
		self.rig_info = {}

		# Allows for seletion of new joints to get new positions from
		if len( cmds.ls( sl=True, type='joint' )) == numjnts :
			sel = cmds.ls( sl=True, type='joint' )
			positions = []
			for s in sel:
				positions.append( cmds.xform( s, q=True, ws=True, t=True ))
			self.rig_info['positions'] = positions

		else:
			#goes to default
			self.rig_info['positions'] = self.module_info['positions']

		self.instance = '_L_'
		# run righ_arm function
		self.rig_arm()



	def rig_arm( self ):
		# de select because of the check in class
		cmds.select( d=True )
		# Create Ik joints, passing in keys
		self.rig_info['ikjnts'] = utils.createJoint( self.module_info['ikjnts'], self.rig_info['positions'], self.instance )
		#cmds.select( d=True )
		
		# Create Fk joints
		self.rig_info['fkjnts'] = utils.createJoint( self.module_info['fkjnts'], self.rig_info['positions'], self.instance )
		#cmds.select( d=True )
		
		# Create Rig joints
		self.rig_info['rigjnt'] = self.createJoint( self.module_info['rigjnt'], self.rig_info['positions'], self.instance )
		#cmds.select( d=True )		


		# Create Ik Rig
		# Ik handle
		#  "ikcontrols" : ["ctrl_ik_arm, ikh_arm", "ctrl_pv_arm"]
		ikhname = self.module_info["ikcontrols"][1].replace( '_s_', self.instance )
		self.rig_info['ikh'] = cmds.ikHandle( n=ikhname, sj=self.rig_info['ikjnts'][0], ee=self.rig_info['ikjnts'][2], sol='ikRPsolver', p=2, w=1)
		
		utils.createControl( [[self.module_info['positions'][2], self.module_info["ikcontrols"][0]]] )

		pvpos = utils.calculatePVPosition( [self.module_info['ikjnts'][0], self.module_info['ikjnts'][1], self.module_info['ikjnts'][2]] )

		pvctrlinfo = [ [pvpos, self.module_info["ikcontrols"][2]] ]
		utils.createControl(pvctrlinfo)

		# Parent ikh to ctrl
		cmds.parent( self.module_info["ikcontorls"][1], self.module_info["ikcontrols"][0])

		# PV constraint
		cmds.poleVectorConstraint( self.module_info["ikcontrols"][2], self.module_info["ikcontrols"][1])

		# Orient constrain arm ik_wrist to ctrl arm
		cmds.orientConstraint( self.module_info["ikcontrols"][0], self.module_info['ikjnts'][2], mo=True)

		
		# Create FK Rig
		self.rig_info['fkcontrols'] = utils.createControl( [[self.module_info["positions"][2], self.module_info["fkcontrols"][2]], 
		[self.module_info["positions"][1], self.module_info["fkcontrols"][1]], 
		[self.module_info["positions"][0], self.module_info["fkcontrols"][0]]] ) 

		#Parent fk controls
		cmds.parent( fkctrlinfo[0][0], fkctrlinfo[1][1][0] )
		cmds.parent( fkctrlinfo[1][0], fkctrlinfo[2][1][0] )

		# Create Rig jnts by parenting FK and IK to Rig jnts
		pass




