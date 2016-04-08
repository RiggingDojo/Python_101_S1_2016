import maya.cmds as cmds
import json
import tempfile

def writeJson( fileName, data ):
	''' writes a pretty json file'''
	
	with open(fileName, 'w') as outfile:
		json.dump( data, outfile, sort_keys = True, indent = 4, ensure_ascii=False )
	file.close(outfile)

def readJson( fileName ):
	'''reads json file'''

	with open(fileName, 'r') as infile:
		data = ( open(infile.name, 'r' ).read())
	return data

def createJoint( name, position, instance ):
	'''
	for i in range(len( jntinfo )):
		cmds.joint( n=jntinfo[i], p=self.module_info['positions'][i] )
	'''
	jnt_list = [cmds.joint( n = name[i].replace('_s_', instance), p=position[i]) for i in range(len(name)) ]
	cmds.select( d=True )
	return( jnt_list )
	#orient joints
	for i in range(len( jntinfo )):
		cmds.joint(jntinfo[i], edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True)

def createControl( ctrlinfo ):
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



def calculatePVPosition( jnts ):
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
