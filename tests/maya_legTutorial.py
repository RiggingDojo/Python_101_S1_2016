'''
This is a tutorial from RiggingDojo Python101 that shows how to create a leg 
rig with stretchy Ik controls and a full complement of root roll controls
This typed out as a copy of Riggig Dojo's tutorial.

Some modifications include making control object with scripts. 

'''


import maya.cmds as cmds


#Create ikHandles for the leg, ball and toe
cmds.ikHandle( name='ikh_leg', startJoint='ikj_hip', endEffector='ikj_ankle', solver='ikRPsolver' )
cmds.ikHandle( name='ikh_ball', startJoint='ikj_ankle', endEffector='ikj_ball', solver='ikSCsolver' )
cmds.ikHandle( name='ikh_toe', startJoint='ikj_ball', endEffector='ikj_toe', solver='ikSCsolver' )




#create a list of control groups and create the empty groups from this list
footGroups = ('grp_footPivot', 'grp_heel', 'grp_toe', 'grp_ball', 'grp_flap')

for item in footGroups:
        cmds.group( name=item, empty=True, world=True )

      
        
#Get the positions of all the joints and assign variables
hipPos = cmds.xform( 'ikj_hip', q=True, worldSpace=True, translation=True )
anklePos = cmds.xform( 'ikj_ankle', q=True, worldSpace=True, translation=True )
ballPos = cmds.xform( 'ikj_ball', q=True, worldSpace=True, translation=True )
toePos = cmds.xform( 'ikj_toe', q=True, worldSpace=True, translation=True )
pelvisPos = cmds.xform( 'jnt_pelvis', q=True, worldSpace=True, translation=True )



#snap groups to joints and control objects
cmds.xform( 'grp_toe', worldSpace=True, translation=toePos )
cmds.xform( 'grp_ball', worldSpace=True, translation=ballPos )
cmds.xform( 'grp_flap', worldSpace=True, translation=ballPos )
cmds.circle( name='ctrl_leg', normal=(0, 1, 0), center=anklePos )




#parent groups 
cmds.parent('grp_heel', 'grp_footPivot')
cmds.parent('grp_toe', 'grp_heel')
cmds.parent('grp_ball', 'grp_toe')
cmds.parent('grp_flap', 'grp_toe')
cmds.parent('ikh_leg', 'grp_ball')
cmds.parent('ikh_ball', 'grp_ball')
cmds.parent('ikh_toe', 'grp_flap')
cmds.parent('grp_footPivot', 'ctrl_leg')



#create a no-flip knee
cmds.spaceLocator( name='lctrPv_leg' )
cmds.xform( 'lctrPv_leg', worldSpace=True, translation=pelvisPos )

cmds.poleVectorConstraint('lctrPV_leg', 'ikh_leg', weight=1 )
cmds.select( 'ctrl_leg', r=True )
cmds.addAttr( shortName='Twist', longName='Twist', defaultValue=0, keyable=True )


cmds.shadingNode( 'plusMinusAverage', asUtility=True, n='pmaNOde_LegTwist' )
cmds.shadingNode( 'multiplyDivide', asUtility=True, n='mdNode_LegTwist' )


#Set up the connections using the following commands :
cmds.connectAttr('ctrl_leg.Twist', 'mdNode_LegTwist.input1X')
cmds.connectAttr('ctrl_leg.ry', 'mdNode_LegTwist.input1Y')
cmds.connectAttr('jnt_pelvis.ry', 'mdNode_LegTwist.input1Z')
cmds.setAttr('mdNode_LegTwist.input2X', -1)
cmds.setAttr('mdNode_LegTwist.input2Y', -1)
cmds.setAttr('mdNode_LegTwist.input2Z', -1)

cmds.connectAttr('mdNode_LegTwist.input1X', 'pmaNode_LegTwist.input1D[0]')
cmds.connectAttr('mdNode_LegTwist.input1Y', 'pmaNode_LegTwist.input1D[1]')
cmds.connectAttr('pmaNode_LegTwist.output1D', 'ikh_leg.twist')









#Step 6:  Create the Stretchy IK
#Start by creating all of the nodes we will need for the stretch.
cmds.shadingNode('addDoubleLinear', asUtility=True, n='adlNode_LegStretch')
cmds.shadingNode('clamp', asUtility=True, n='clampNode_LegStretch')
cmds.shadingNode('multiplyDivide', asUtility=True, n='mdNode_LegStretch')
cmds.shadingNode('multiplyDivide', asUtility=True, n='mdNode_KneeStretch')
cmds.shadingNode('multiplyDivide', asUtility=True, n='mdNode_AnkleStretch')

#Add a “Stretch” attribute to ctrl_leg.
cmds.select('ctrl_leg')
cmds.addAttr( shortName='Stretch', longName='Stretch', defaultValue=0, keyable=True)


#Create a distance tool to measure the distance between hip and ankle joints
hipPos = cmds.xform('ikj_hip', q=True, translation=True)
anklePos = cmds.xform('ikj_ankle', q=True, translation=True)

disDim = cmds.distanceDimension(startPoint=(hipPos), endPoint=(anklePos))
cmds.rename('distanceDimension1', 'disDimNode_legStretch')
cmds.rename('locator1', 'lctrDis_hip')
cmds.rename('locator2', 'lctrDis_ankle')

cmds.parent('lctrDis_hip', 'jnt_pelvis')
cmds.parent('lctrDis_ankle', 'grp_ball')







#Step 7:  Create the Foot Roll

#Create Attributes on the ctrl_foot
cmds.select('ctrl_leg')
cmds.addAttr(shortName='Roll_Break', longName='Roll_Break', defaultValue=0, k=True)
cmds.addAttr(shortName='Foot_Roll', longName='Foot_Roll', defaultValue=0, k=True)


#Set the foot roll and Create utility nodes
cmds.shadingNode('condition', asUtility=True, n='conNode_ballRoll')
cmds.shadingNode('condition', asUtility=True, n='conNode_negBallRoll')
cmds.shadingNode('condition', asUtility=True, n='conNode_toeRoll')
cmds.shadingNode('plusMinusAverage', asUtility=True, n='pmaNode_ballRoll')
cmds.shadingNode('plusMinusAverage', asUtility=True, n='pmaNode_toeRoll')
cmds.shadingNode('condition', asUtility=True, n='conNode_heelRoll')
cmds.setAttr('pmaNode_toeRoll.operation', 2) #Check what "operation" does
cmds.setAttr('conNode_toeRoll.operation', 2)
cmds.setAttr('conNode_toeRoll.colorlfFalseR', 0)
cmds.setAttr('conNode_toeRoll.colorlfFalseG', 0)
cmds.setAttr('conNode_toeRoll.colorlfFalseB', 0)
cmds.setAttr('conNode_heelRoll.operation', 4)
cmds.setAttr('conNode_heelRoll.colorlfFalseR', 0)
cmds.setAttr('conNode_heelRoll.colorlfFalseG', 0)
cmds.setAttr('conNode_heelRoll.colorlfFalseB', 0)
cmds.setAttr('pmaNode_ballRoll.operation', 2)
cmds.setAttr('conNode_negBallRoll.operation', 3)
cmds.setAttr('conNode_ballRoll.operation', 3)


#Connect Utility Nodes
#Setup Toe
cmds.connectAttr('ctrl_leg.Foot_Roll', 'conNode_toeRoll.firstTerm')
cmds.connectAttr('ctrl_leg.Foot_Roll', 'conNode_toeRoll.colorlfTrueR')
cmds.connectAttr('ctrl_leg.Roll_Break', 'conNode_toeRoll.secondTerm')
cmds.connectAttr('ctrl_leg.Roll_Break', 'conNode_toeRoll.colorlfFalseR')
cmds.connectAttr('ctrl_leg.Roll_Break', 'pmaNode_toeRoll.input1D[1]')
cmds.connectAttr('conNode_toeRoll.outColorR', 'pmaNode_toeRoll.input1D[0]')
cmds.connectAttr('pmaNode_toeRoll.output1D', 'grp_toe.rx')


#Setup Heel
cmds.connectAttr('ctrl_leg.Foot_Roll', 'conNode_heelRoll.firstTerm')
cmds.connectAttr('ctrl_leg.Foot_Roll', 'conNode_heelRoll.colorIfTrueR')
cmds.connectAttr('conNode_heelRoll.outColorR', 'grp_heel.rotateX')

#Setup Ball
cmds.connectAttr('ctrl_leg.Foot_Roll', 'conNode_ballRoll.firstTerm')
cmds.connectAttr('ctrl_leg.Foot_Roll', 'conNode_ballRoll.colorIfTrueR')
cmds.connectAttr('ctrl_leg.Roll_Break', 'conNode_negBallRoll.secondTerm')
cmds.connectAttr('ctrl_leg.Roll_Break', 'conNode_negBallRoll.colorIfTrueR')
cmds.connectAttr('conNode_negBallRoll.outColorR', 'pmaNode_ballRoll.input1D[0]')
cmds.connectAttr('grp_toe.rx', 'pmaNode_ballRoll.input1D[1]')
cmds.connectAttr('pmaNode_ballRoll.output1D', 'grp_ball.rx')
cmds.connectAttr('conNode_ballRoll.outColorR', 'conNode_negBallRoll.firstTerm')
cmds.connectAttr('conNode_ballRoll.outColorR', 'conNode_negBallRoll.colorIfFalseR')




#Make a Toe Flap
#make a new attribute called Toe_Flap on ctrl_foot.  
#then connect Toe_Flap to grp_flap rotateX.
cmds.select('ctrl_leg')
cmds.addAttr(shortName='Toe_Flap', longName='Toe_Flap', defaultValue=0, k=True)
cmds.connectAttr('ctrl_leg.Toe_Flap', 'grp_flap.rx')









#Step 8:  Pivot for Bank and Twist

#Create Pin Shape
cmds.circle( name='ctrl_footPivot', normal=(0, 1, 0) )
cmds.select( 'ctrl_footPivot.cv[1]')
cmds.move( 0, 0, -3, objectSpace=True, worldSpaceDistance=True )

#Move the control to the grp_ball.
ballPos = cmds.xform('grp_ball', q=True, t=True, ws=True)
cmds.xform('ctrl_footPivot', t=ballPos)
cmds.select(clear)



#create an empty group at the origin.
cmds.group(name='grp_ctrl_footPivot', empty=True)
cmds.parent('grp_ctrl_footPivot', 'ctrl_footPivot')
cmds.parent('ctrl_footPivot', 'ctrl_foot')
cmds.makeIdentity(apply=True) #Freeze Transforms



#connect the grp_ctrl_footPivot.translate to grp_footPivot.rotatePivot
cmds.connectAttr('grp_ctrl_footPivot.translate', 'grp_footPivot.rotatePivot')
cmds.xform('grp_ctrl_footPivot', t=ballPos)


#Make a couple more attributes for twist and bank
#then hook those up to the grp_footPivot.
cmds.select('ctrl_leg')
cmds.addAttr(shortName='Foot_Pivot', longName='Foot_Pivot', defaultValue=0, k=True)
cmds.addAttr(shortName='Foot_Bank', longName='Foot_Bank', defaultValue=0, k=True)
cmds.connectAttr('ctrl_leg.FootPivot', 'grp_footPivot.ry')
cmds.connectAttr('ctrl_leg.FootBank', 'grp_footPivot.rz')













