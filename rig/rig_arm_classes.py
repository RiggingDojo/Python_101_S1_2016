import maya.cmds as cmds
import json
import os
import system.utils as utils


rig_data = {}
rig_data[ 'ikjnts' ] = [ 'ik_shoulder_jnt', 'ik_elbow_jnt', 'ik_wrist_jnt', 'ik_wristEnd_jnt' ]
rig_data[ 'fkjnts' ] =  [ 'fk_shoulder_jnt', 'fk_elbow_jnt', 'fk_wrist_jnt', 'fk_wristEnd_jnt' ]
rig_data[ 'rigjnt' ] = [ 'ik_shoulder_jnt', 'ik_elbow_jnt', 'ik_wrist_jnt', 'ik_wristEnd_jnt' ]
rig_data[ 'bindjnts' ] = [ 'bind_shoulder_jnt', 'bind_elbow_jnt', 'bind_wrist_jnt', 'bind_wristEnd_jnt' ]
rig_data[ 'ikcontrols' ] = [ 'ctrl_ik_arm, ikh_arm', 'ctrl_pv_arm']
rig_data[ 'fkcontrols' ] = [ 'ctrl_fk_shoulder', 'ctrl_fk_elbow', 'ctrl_fk_wrist' ]
rig_data[ 'positions' ] = [[0.0, 0.0, 0.0], [-1.0, 0.0, 2.0], [0.0, 0.0, 4.0], [0.0, 0.0, 6.0] ]


class Rig_Arm:
	'''creates instance of arm, default is right arm'''

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


	def orient_joints( self ):
		for i in sel:
			cmds.joint(i, edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True)

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

