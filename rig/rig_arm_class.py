import maya.cmds as cmds
import json
import os
import system.utils as utils

class Rig_Arm:
	
	def __init__( self ):
		# Get our joint lists from a json file.
		data_path = os.environ["RDOJO_DATA"] + 'rig/arm.json'
		# Use our readJson function
		data = utils.readJson( data_path )
		# Load the json in a dictionary
		self.module_info = json.loads( data )

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


	def orient_joints( self )
		for i in sel:
			cmds.joint(i, edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True)

	def calculatePVPosition( jnts ):
		"Calculates the Position of jnts"
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

