import maya.cmds as cmds
import system.utils as utils
import json
reload(utils)


    
# ASSIGN NAMES FOR DICTIONARY ITEMS
dict = {'translation': ['.translateX', '.translateY', '.translateZ'],
    'rotation': ['.rotateX', '.rotateY', '.rotateZ'],
    'scale': ['.scaleX', '.scaleY', '.scaleZ'],
    'prefix': ['ik_', 'fk_', 'rig_'],
    'group':'grp_',
    'control': 'ctrl_',
    'jointSuffix':'_jnt',
    'pv': 'polev_',
    'shoulder': 'shoulder',
    'elbow': 'elbow',
    'wrist': 'wrist',
    'wristEnd': 'wristEnd'
    }

pos = {'shoulder': [-0.2, 0.0, 8.5],
    'elbow': [-4.0, 0.0, 0.04],
    'wrist': [0.15, 0, -4.7],
    'wristEnd': [-0.07, 0, -7.4]
    }
   
        
# JOINT INFO
joint_names = [[dict['shoulder'] + dict['jointSuffix'], pos['shoulder']],
               [dict['elbow'] + dict['jointSuffix'], pos['elbow']],
               [dict['wrist'] + dict['jointSuffix'], pos['wrist']],
               [dict['wristEnd'] + dict['jointSuffix'], pos['wristEnd']]]

# JOINT ROOT
joint_root = (dict['prefix'][0],
              dict['prefix'][1],
              dict['prefix'][2])

# MAKE FULL JOINT DICTIONARY WITH POSITIONS
# Create joint dictionary as function
def createJntDict(keys, values):
    
    joint_dict = {}

    for var in joint_root:
        
        tmp_lst = []
        
        for i in range(len(keys)):
            new_name = var + keys[i][0]
            tmp_lst.append([new_name, keys[i][1]])
         
        joint_dict[var] = tmp_lst
    return joint_dict

# Create dictionary with joint data
joint_dict = createJntDict(joint_names, joint_root)
# Write dictionary out to json file
rig_data = {}
# List comprehension
rig_data['ikjnts'] = [joint_dict['ik_'][i][0] for i in range(len(joint_dict['ik_']))]
rig_data['fkjnts'] = [joint_dict['fk_'][i][0] for i in range(len(joint_dict['fk_']))]
rig_data['rigjnts'] = [joint_dict['rig_'][i][0] for i in range(len(joint_dict['rig_']))]
rig_data['ikcontrols']  = ['ctrl_ik_arm', 'ikh_arm', 'ctrl_pv_arm']
rig_data['fkcontrols'] = ['ctrl_fk_shoulder', 'ctrl_fk_elbow', 'ctrl_fk_wrist']
rig_data['positions'] = [-0.2, 0.0, 8.5], [-4.0, 0.0, 0.04], [0.15, 0, -4.7], [-0.07, 0, -7.4]

# Write out Json joint list
fileName = 'C:/Users/richard/Documents/GitHub/Python_101_S1_2016/layout/jointlist.json'
utils.writeJson(fileName, rig_data)

newdata = utils.readJson(fileName)
print newdata
# Read in newdata variable into info variable
info = utils.json.loads( newdata )

# Iterate through the dictionary
for key, value in info.iteritems():
    print key
    print value

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# CLASSES AND FUNCTIONS
class Rig_Arm:
    
    def createJoint(makejnt):
        for i in range(len(makejnt)):
            cmds.joint(n=item[0], p=item[1])  
        cmds.select(d = True)

    def createControl(ctrlinfo):
        for info in ctrlinfo:
            # Create ik control
            # Get ws position of wrist joint
            pos = info[0]
            # Create an empty group
            ctrlgrp = cmds.group(em-True, name=info[2])
            # Create circle control object
            ctrl = cmds.circle(n=fk_ctrl_name, normal=(1, 0, 0), center=(0, 0, 0), sweep=360, radius=2)
            # Parent the control to the group
            cmds.parent(ctrl, ctrl_grp)
            # Move the group to the joint
            cmds.xform(ctrlgrp, t=pos, ws=True)
            
    def calculatePVPosition(jnts):
        from maya import cmds, OpenMaya
        start = cmds.xform(jnts[0] ,q=True, ws=True, t=True)
        mid = cmds.xform(jnts[1] ,q=True, ws=True, t=True)
        end = cmds.xform(jnts[2] ,q=True, ws=True, t=True)
        startV = OpenMaya.MVector(start[0], start[1], start[2])
        midV = OpenMaya.MVector(mid[0], mid[1], mid[2])
        endV = OpenMaya.MVector(end[0], end[1], end[2])
        startEnd = endV - startV
        startMid = midV - startV
        dotP = startMid * startEnd
        proj = float(dotP) / float(startEnd.length())
        startEndN = startEnd.normal()
        projV = startEndN * proj
        arrowV = startMid - projV
        finalV = arrowV + midV
        return ([finalV.x, finalV.y, finalV.z])
        
# Create Ik joints

createJoint() 

# CREATE ALL JOINTS AS FUNCTION
 
    

    # LOOP THROUGH JOINTS AND ORIENT TO XYZ
    for key, value in joint_dict.iteritems():
         
        for i in range(len(value)):
            joint_name = value[i][0]
            joint_pos = value[i][1]
            cmds.joint( (joint_name), edit=True, zso=True, oj='xyz', sao='yup')
         
        cmds.select(d = True)

    # JOINT NAME AND POS TO CREATE CTRL AND GRP
        # CREATE FK RIG
        if key.startswith('fk'):
            for i in range(len(value)):
                joint_name = value[i][0]
                group_pos = value[i][1]
                fk_grp_name = dict['group'] + dict['control'] + joint_name[:-len(dict['jointSuffix'])]
                grp_rot = cmds.xform(joint_name, q=True, ro=True, ws=True)
                fk_ctrl_name = dict['control'] + joint_name[:-len(dict['jointSuffix'])]
                                        
                if 'End' not in joint_name:
                    # CREATE AN EMPTY GROUP AND NAME BY THE JOINT
                    cmds.group(em=True, name=fk_grp_name)
                    # ROTATE EMPTY GROUP TO THE GROUP ROTATION
                    cmds.xform(fk_grp_name, ro=grp_rot, ws=True)
                    # CREATE CIRCLE CTRL ROTATED 90 IN X
                    cmds.circle(n=fk_ctrl_name, normal=(1, 0, 0), center=(0, 0, 0), sweep=360, radius=2)
                    # DEL CIRCLE HISTORY
                    cmds.delete(fk_ctrl_name, constructionHistory=True)
                    # PARENT THE CTRL TO THE CTRL GRP
                    cmds.parent(fk_ctrl_name, fk_grp_name)
                    cmds.setAttr(fk_ctrl_name + dict['rotation'][1], 0)
                    # XFORM GROUP TO THE GROUP POSITION
                    cmds.xform(fk_grp_name, t=group_pos, ws=True)
                    # ORIENT CONSTRAINT CTRL TO JOINT
                    cmds.orientConstraint(fk_ctrl_name, joint_name)
                    # LOCK CTRL ATTRIBUTES TRANSLATION AND SCALE
                    for v in fk_ctrl_name:
                        cmds.setAttr(fk_ctrl_name + '.t', edit=True,  lock=True, keyable=False, channelBox=False)
                        cmds.setAttr(fk_ctrl_name + '.s', edit=True,  lock=True, keyable=False, channelBox=False)
            # PARENT CTRLS
            cmds.parent(dict['group'] + dict['control'] + dict['prefix'][1] + dict['elbow'], dict['control'] + dict['prefix'][1] + dict['shoulder'])
            cmds.parent(dict['group'] + dict['control'] + dict['prefix'][1] + dict['wrist'], dict['control'] + dict['prefix'][1] + dict['elbow'])
            # DESELECT
            cmds.select(d=True)

        # CREATE IK RIG
        elif key.startswith('ik'):
            # CREATE IK HANDLE
            cmds.ikHandle( name="ikh_arm", startJoint=joint_dict['ik_'][0][0], endEffector=joint_dict['ik_'][2][0], solver="ikRPsolver", priority=2, weight=1 )
            # GET WS POSITION OF WRIST JOINT
            pos = cmds.xform(joint_dict['ik_'][2][0], query=True, translation=True, worldSpace=True)
            # CREATE GROUP
            cmds.group( em=True, name="grp_ctrl_ikWrist" )
            # CREATE A CIRCLE CONTROL OBJECT
            cmds.circle( name="ctrl_ik_wrist", normal=(0, 0, 1), center=(0, 0, 0), sweep=360, radius=2 )
            # DELETE HISTORY ON CIRCLE
            cmds.delete( 'ctrl_ik_wrist', constructionHistory=True )
            # PARENT THE CONTROL TO THE GROUP
            cmds.parent("ctrl_ik_wrist", "grp_ctrl_ikWrist")
            rot = cmds.xform('ik_wrist_jnt', q=True, ro=True, ws=True)
            cmds.xform('grp_ctrl_ikWrist', ro=rot, ws=True)
            cmds.xform( r=True, ro=(0, 90, 0) )
            # MOVE THE GROUP TO THE JOINT
            cmds.xform("grp_ctrl_ikWrist", translation=pos, a=True)
            # PARENT IKH TO CONTROL
            cmds.parent("ikh_arm", "ctrl_ik_wrist")
            # ORIENT CONSTRAINT CONTROL TO JOINT
            cmds.orientConstraint( 'ctrl_ik_wrist', 'ik_wrist_jnt', mo = True)
            # GET ELBOW XFORM
            ikpos = cmds.xform('ik_elbow_jnt', query=True, translation=True, worldSpace=True)
            # Move ikpos x -2 in x
            k = [ -2, 0, 0] 
            zipped = [sum(i) for i in zip(ikpos,k)]
            ikpos = zipped
            cmds.spaceLocator( n='ik_poleVector')
            cmds.xform('ik_poleVector', ws=True, t=(ikpos))
            # ATTACH PV TO IK
            cmds.poleVectorConstraint( 'ik_poleVector', 'ikh_arm' )
            # Lock ctrl_ikWrist scale
            cmds.setAttr(dict['control'] + dict['prefix'][0] + dict['wrist'] + '.s', edit=True,  lock=True, keyable=False, channelBox=False)
            # Deselect
            cmds.select(d=True)

    # CREATE RIG
        elif key.startswith('rig'):
            # GET WS POSITION OF WRIST JOINT
            cmds.xform(joint_dict['rig_'][2][0], query=True, translation=True, worldSpace=True)
            # CREATE GROUP
            ikgrp = cmds.group(em=True, name="grp_switch_ikfk")
            # CREATE A CIRCLE CONTROL OBJECT
            cmds.circle(name="switch_ikfk", normal=(0, 0, 1), center=(0, 0, 0), sweep=360, radius=2)
            # DELETE HISTORY ON CIRCLE
            cmds.delete('switch_ikfk', constructionHistory=True)
            # PARENT THE CONTROL TO THE GROUP
            cmds.parent("switch_ikfk", "grp_switch_ikfk")
            rot = cmds.xform('switch_ikfk', q=True, ro=True, ws=True)
            cmds.xform('grp_switch_ikfk', ro=rot, ws=True)
            cmds.xform( r=True, ro=(90, 0, 0) )
            # MOVE THE GROUP TO THE JOINT
            cmds.xform("grp_switch_ikfk", translation=pos, a=True)
            # PARENT SWITCH GROUP TO WRIST JOINT
            cmds.parent( 'grp_switch_ikfk', 'rig_wrist_jnt')
            # LOCK CTRL ATTR
            cmds.setAttr('switch_ikfk' + '.t', edit=True,  lock=True, keyable=False, channelBox=False)
            cmds.setAttr('switch_ikfk' + '.s', edit=True,  lock=True, keyable=False, channelBox=False)
            cmds.setAttr('switch_ikfk' + '.r', edit=True,  lock=True, keyable=False, channelBox=False)
            
            
    
    
    rigArm()
    
    
# Create blend attribute
cmds.select( d=True )
cmds.select( 'switch_ikfk' )
cmds.addAttr( 'switch_ikfk', longName='IKFKBlend', attributeType='double', min=0, max=1, defaultValue=1 )
cmds.setAttr( 'switch_ikfk.IKFKBlend', edit=True, keyable=True )
cmds.setAttr( 'switch_ikfk.IKFKBlend', 0 )

# Create 3 blend color nodes
cmds.shadingNode( 'blendColors', name="blend_shoulder", asUtility=True )
cmds.shadingNode( 'blendColors', name="blend_elbow", asUtility=True )
cmds.shadingNode( 'blendColors', name="blend_wrist", asUtility=True )

# Connect blends to rig joints
cmds.connectAttr( 'blend_shoulder.outputR', 'rig_shoulder_jnt.rotateX')
cmds.connectAttr( 'blend_shoulder.outputG', 'rig_shoulder_jnt.rotateY')
cmds.connectAttr( 'blend_shoulder.outputB', 'rig_shoulder_jnt.rotateZ')

cmds.connectAttr( 'blend_elbow.outputR', 'rig_elbow_jnt.rotateX')
cmds.connectAttr( 'blend_elbow.outputG', 'rig_elbow_jnt.rotateY')
cmds.connectAttr( 'blend_elbow.outputB', 'rig_elbow_jnt.rotateZ')

cmds.connectAttr( 'blend_wrist.outputR', 'rig_wrist_jnt.rotateX')
cmds.connectAttr( 'blend_wrist.outputG', 'rig_wrist_jnt.rotateY')
cmds.connectAttr( 'blend_wrist.outputB', 'rig_wrist_jnt.rotateZ')

# Connect ik and fk to drive the blender nodes
cmds.connectAttr( 'ik_shoulder_jnt.rotateX', 'blend_shoulder.color1R')
cmds.connectAttr( 'ik_shoulder_jnt.rotateY', 'blend_shoulder.color1G')
cmds.connectAttr( 'ik_shoulder_jnt.rotateZ', 'blend_shoulder.color1B')
cmds.connectAttr( 'ik_elbow_jnt.rotateX', 'blend_elbow.color1R')
cmds.connectAttr( 'ik_elbow_jnt.rotateY', 'blend_elbow.color1G')
cmds.connectAttr( 'ik_elbow_jnt.rotateZ', 'blend_elbow.color1B')
cmds.connectAttr( 'ik_wrist_jnt.rotateX', 'blend_wrist.color1R')
cmds.connectAttr( 'ik_wrist_jnt.rotateY', 'blend_wrist.color1G')
cmds.connectAttr( 'ik_wrist_jnt.rotateZ', 'blend_wrist.color1B')


cmds.connectAttr( 'fk_shoulder_jnt.rotateX', 'blend_shoulder.color2R')
cmds.connectAttr( 'fk_shoulder_jnt.rotateY', 'blend_shoulder.color2G')
cmds.connectAttr( 'fk_shoulder_jnt.rotateZ', 'blend_shoulder.color2B')
cmds.connectAttr( 'fk_elbow_jnt.rotateX', 'blend_elbow.color2R')
cmds.connectAttr( 'fk_elbow_jnt.rotateY', 'blend_elbow.color2G')
cmds.connectAttr( 'fk_elbow_jnt.rotateZ', 'blend_elbow.color2B')
cmds.connectAttr( 'fk_wrist_jnt.rotateX', 'blend_wrist.color2R')
cmds.connectAttr( 'fk_wrist_jnt.rotateY', 'blend_wrist.color2G')
cmds.connectAttr( 'fk_wrist_jnt.rotateZ', 'blend_wrist.color2B')

cmds.connectAttr( 'switch_ikfk.IKFKBlend', 'blend_shoulder.blender')
cmds.connectAttr( 'switch_ikfk.IKFKBlend', 'blend_elbow.blender')
cmds.connectAttr( 'switch_ikfk.IKFKBlend', 'blend_wrist.blender')

