import maya.cmds as cmds
import json
import os
import system.utils as utils



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




	def rig_arm( self ):
		# Create Ik joints, passing in keys
		self.createJoint( self.module_info['ikjnts'] )
		cmds.select( d=True )
		# Create Fk joints
		self.createJoint( self.module_info['fkjnts'] )
		cmds.select( d=True )
		# Create Rig joints
		self.createJoint( self.module_info['rigjnt'] )
		cmds.select( d=True )		


		# Create Ik Rig
		# Ik handle
		#  "ikcontrols" : ["ctrl_ik_arm, ikh_arm", "ctrl_pv_arm"]
		ikh = cmds.ikHandle( n=self.module_info["ikcontrols"][1], sj=self.module_info['ikjnts'][0], ee=self.module_info['ikjnts'][2], sol='ikRPsolver', p=2, w=1)
		
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

		# Create Rig jnts by parenting FK and IK to Rig jnts
		pass



	def createJoint( self, jntinfo ):
		for i in range(len( jntinfo )):
			cmds.joint( n=jntinfo[i], p=self.module_info['positions'][i] )
		#orient joints
		for i in range(len( jntinfo )):
			cmds.joint(jntinfo[i], edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True)

	def createControl( self, ctrlinfo ):
		for info in ctrlinfo:
			# Create ik control
			# get ws position of wrist joint
			pos = info[0]
			# create an empty group
			ctrlgrp = cmds.group( em=True, name=info[2] )
			# Create circle control object
			ctrl = cmds.circle( n=info[1], nr=(0, 0, 1), c=(0, 0, 0) )
			# Parent the control to the group
			cmds.parent( ctrl, ctrlgrp )
			# Move the group to the joint
			cmds.xform( ctrlgrp, t=pos, ws=True ) 



	def calculatePVPosition( self, jnts ):
		#Calculates the pole vector of jnts
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

