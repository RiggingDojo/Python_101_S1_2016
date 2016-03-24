import maya.cmds as cmds
import json
import os
import system.utils as utils

class Rig_Arm:
	'''creates instance of arm, default is right arm'''

	def __init__( self ):
		# Get our joint lists from a json file.
		data_path = os.environ["RDOJO_DATA"] + 'rig/arm.json'
		# Use our readJson function
		data = utils.readJson( data_path )
		# Load the json in a dictionary
		self.module_info = json.loads( data )
		# left side of the arm
		side = 'L'

	def rig_arm( self ):
		# Create Ik joints, passing in keys
		self.createJoint( self.module_info['ikjnts'] )
		cmds.select( d=True )
		# Create Fk joints
		self.createJoint( self.module_info['fkjnts'] )
		cmds.select( d=True )
		# Create Rig joints
		self.createJoint( self.moduel_info['rigjnts'] )
		cmds.select( d=True )		


		# Create Ik Rig
		# Ik handle
		#  "ikcontrols" : ["ctrl_ik_arm, ikh_arm", "ctrl_pv_arm"]
		ikh = cmds.ikHandle( n=self.module_info["ikcontrols"][1], sj=self.module_info['ikjnts'][0], ee=self.module_info['ikjnts'][2], solf='ikRPsolver', p=2, w=1)
		
		self.createControl( [[self.module_info['positions'][2], self.module_info["ikcontrols"][0]]] )

		pvpos = self.calculatePVPosition( [self.module_info['ikjnts'][0], self.module_info['ikjnts'][1], self.module_info['ikjnts'][2]] )

		pvctrlinfo = [ [pvpos, self.module_info["ikcontrols"][2]] ]
		self.createControl(pvctrlinfo)

		# Parent ikh to ctrl
		cmds.parent( self.module_info["ikcontorls"][1], self.module_info["ikcontrols"][0])

		# PV constraint
		cmds.poleVectorConstraint( self.module_info["ikcontrols"][2], self.module_info["ikcontrols"][1])

		# Orient constrain arm ik_wrist to ctrl arm
		cmds.orientConstraint( self.module_info["ikcontrols"][0], self.module_info['ikjnts'][2], mo=True)

		
		# Create FK Rig
		fkctrlinfo = self.createControl( [[self.module_info["positions"][2], self.module_info["fkcontrols"][2]], 
		[self.module_info["positions"][1], self.module_info["fkcontrols"][1]], 
		[self.module_info["positions"][0], self.module_info["fkcontrols"][0]]] ) 

		#Parent fk controls
		cmds.parent( fkctrlinfo[0][0], fkctrlinfo[1][1][0] )
		cmds.parent( fkctrlinfo[1][0], fkctrlinfo[2][1][0] )


	'''	
	def orient_joints( self, jnts ):
		for i in jnts:
			cmds.joint(i, edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True)
	'''

	def createJoint( self, jntinfo ):
		for i in range(len( jntinfo )):
			cmds.joint( n=jntinfo[i], p=self.module_info['positions'][i] )


	def calculatePVPosition( self, jnts ):
		#Calculates the Position of jnts
		from maya import cmds, OpenMaya
		start = cmds.xform( jnts[0], q=True, ws=True, t=True )
		mid = cmds.xform( jnts[1], q=True, ws=True, t=True )
		end = cmds.xform( jnts[2], q=True, ws=True, t=True )
		startV = OpenMaya.MVector( start[0], start[1], start[2] )
		midV = OpenMaya.MVector( mid[0], mid[1], mid[2] )
		endV = OpenMaya.MVector( end[0], end[1], end[2] )
		startEnd = endV - startV
		startMid = midV -startV
		dotP = startMid * startEnd
		proj = float( dotP ) / float( startEnd.length() )
		startEndN = startEnd.normal()
		projV = startEndN * proj
		arrowV = startMid - projV
		arrowV*= 0.5
		finalV = arrowV + midV
		return ( [finalV.x, finalV.y, finalV.z] )

