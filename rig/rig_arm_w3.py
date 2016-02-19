# Label names for the objects
names = {'ikPrefix': 'ik_', 
         'fkPrefix': 'fk_',
         'groupPrefix': 'grp_',
         'controlPrefix': 'ctrl_',
         'jointSufix': '_jnt',
         'bindPrefix': 'bn_',
         'poleVector': 'pv_',
         'shoulder': 'shoulder',
         'elbow': 'elbow',
         'wrist': 'wrist',
         'wristEnd': 'wristEnd',
         'ikHandle': 'ikh',
         'poleVector': 'pv',
         'armSufix': 'arm',
         'plusMinusPrefix': 'plusminus_',
         'multiplyDividePrefix': 'multdiv_',
         'blendingNode': 'FKIK_Blend'
         }
         
# Lists and dictionary with joints data
joint_info = [[names['shoulder'] + names['jointSufix'], [2.1, 0.0, 5.0]], 
              [names['elbow'] + names['jointSufix'], [-0.1, 0.0, 0.0]], 
              [names['wrist'] + names['jointSufix'], [-0.1, 0.0, -5.0]], 
              [names['wristEnd'] + names['jointSufix'], [-0.1, 0.0, -8.0]]]    
             
joint_chains = (names['ikPrefix'],
                names['fkPrefix'], 
                names['bindPrefix'])

joint_dict = {}
  
for label in joint_chains:
    
    tmpJoint_list = []
    
    for i in range(len(joint_info)):
        new_name = label + joint_info[i][0]
        tmpJoint_list.append([new_name, joint_info[i][1]])
     
    joint_dict[label] = tmpJoint_list

# Iterate skeleton dictionary data to create joints, controls and groups       
for key, value in joint_dict.iteritems():
    
    for i in range(len(value)):
        tmp_name = value[i][0]
        tmp_pos = value[i][1]
        cmds.joint(n = tmp_name, p = tmp_pos)
    
    cmds.select(d = True)
    
    # Orient joints
    for i in range(len(value)):
        tmp_name = value[i][0]
        cmds.joint(tmp_name, edit=True, zso=True, oj='xyz', sao='yup')
    
    # Create controls and groups
    if key.startswith('fk'):
        
        for i in range(len(value)):
            jnt_name = value[i][0]
            grp_pos = value[i][1]
            grp_name = names['groupPrefix'] + names['controlPrefix'] + jnt_name[:-len(names['jointSufix'])]
            grp_rot = cmds.xform(jnt_name, q=True, ro=True, ws=True)
            ctrl_name = names['controlPrefix'] + jnt_name[:-len(names['jointSufix'])]
            
            if 'End' not in jnt_name:
                
                # Create empty group
                cmds.group(em=True, name=grp_name)
                
                # Orient group to joint
                cmds.xform(grp_name, ro=grp_rot, ws=True)
                
                # Create circle control object
                cmds.circle(n=ctrl_name, nr=(1, 0, 0), c=(0, 0, 0))
                
                # Delete history
                cmds.delete(ctrl_name, constructionHistory=True)
                
                # Parent the control to the group
                cmds.parent(ctrl_name, grp_name)
                cmds.setAttr(ctrl_name + '.rotateY', 0)
    
                # Move the group to the joint
                cmds.xform(grp_name, t=grp_pos, ws=True)
    
                # Orient constrain joints to ctrls
                cmds.orientConstraint(ctrl_name, jnt_name)
    
                # Lock and hide ctrl attributes
                cmds.setAttr(ctrl_name + '.tx', edit=True,  lock=True, keyable=False, channelBox=False)
                cmds.setAttr(ctrl_name + '.ty', edit=True,  lock=True, keyable=False, channelBox=False) 
                cmds.setAttr(ctrl_name + '.tz', edit=True,  lock=True, keyable=False, channelBox=False)
                cmds.setAttr(ctrl_name + '.sx', edit=True,  lock=True, keyable=False, channelBox=False)
                cmds.setAttr(ctrl_name + '.sy', edit=True,  lock=True, keyable=False, channelBox=False)
                cmds.setAttr(ctrl_name + '.sz', edit=True,  lock=True, keyable=False, channelBox=False)

        # Parent cntrls
        cmds.parent(names['groupPrefix'] + names['controlPrefix'] + names['fkPrefix'] + names['elbow'], names['controlPrefix'] + names['fkPrefix'] + names['shoulder'])
        cmds.parent(names['groupPrefix'] + names['controlPrefix'] + names['fkPrefix'] + names['wrist'], names['controlPrefix'] + names['fkPrefix'] + names['elbow'])

        # Deselect to avoid parenting
        cmds.select(d=True)
        
    elif key.startswith('ik'):
        
        # Ik handle
        tmp_ikHandle = cmds.ikHandle(n=names['ikHandle'] + names['armSufix'], sj=names['ikPrefix'] + names['shoulder'] + names ['jointSufix'], ee=names['ikPrefix'] + names['wrist'] + names ['jointSufix'], sol='ikRPsolver', p=2, w=1 )
        tmp_ikHandle = tmp_ikHandle[0]
        # Create ik control
        # Get ws position of wrist joint
        pos = cmds.xform(names['ikPrefix'] + names['wrist'] + names['jointSufix'], q=True, t=True, ws=True)
        
        # Create an empty group
        tmp_grp = cmds.group(em=True, name=names['groupPrefix'] + names['controlPrefix'] + names['ikPrefix'] + names['wrist'])
        #tmp_grp = tmp_grp[0]
        
        # Create circle control object
        tmp_ikCtrl = cmds.circle( n=names['controlPrefix'] + names['ikPrefix'] + names['wrist'], nr=(0, 0, 1), c=(0, 0, 0))
        tmp_ikCtrl = tmp_ikCtrl[0]
        
        # Delete history
        cmds.delete(tmp_ikCtrl, constructionHistory=True)
        
        # Parent the control to the group
        cmds.parent(tmp_ikCtrl, tmp_grp)
        
        # Move the group to the joint
        cmds.xform(tmp_grp, t=pos, ws=True)
        
        # Parent ikh to ctrl
        cmds.parent(tmp_ikHandle, tmp_ikCtrl)
        
        # Orient constraint ctrl to joint
        cmds.orientConstraint(tmp_ikCtrl, names['ikPrefix'] + names['wrist'] + names['jointSufix'], mo = True)
        
        # Create pole vector
        pos = cmds.xform(names['ikPrefix'] + names['elbow'] + names['jointSufix'], q=True, t=True, ws=True)
        pos[0] -= 2
        tmp_PV = cmds.spaceLocator(n=names['ikPrefix'] + names['poleVector'] + names['armSufix'])
        cmds.xform(tmp_PV, ws=True, t=pos)
        
        # Attach pole vector to IK
        cmds.poleVectorConstraint(tmp_PV, tmp_ikHandle)
        
        # Lock and hide ctrl attributes
        cmds.setAttr(tmp_ikCtrl + '.sx', edit=True,  lock=True, keyable=False, channelBox=False)
        cmds.setAttr(tmp_ikCtrl + '.sy', edit=True,  lock=True, keyable=False, channelBox=False)
        cmds.setAttr(tmp_ikCtrl + '.sz', edit=True,  lock=True, keyable=False, channelBox=False)
        
        # Deselect to avoid parenting
        cmds.select(d=True)
    
    elif key.startswith('bn'):
        
        jnt_name = value[i][0]
        
        if 'End' in jnt_name:

            # Create blend ctrl
            grp_pos = value[i][1]
            grp_name = names['groupPrefix'] + names['controlPrefix'] + names['armSufix']
            grp_rot = cmds.xform(jnt_name, q=True, ro=True, ws=True)
            ctrl_name = names['controlPrefix'] + names['armSufix']
                        
            # Create an empty group
            cmds.group(em=True, name=grp_name)
            
            # Orient grp to joint
            rot = cmds.xform(jnt_name, q=True, ro=True, ws=True)
            cmds.xform(grp_name, ro=rot, ws=True)

            # Create circle control object
            cmds.circle( n=ctrl_name, nr=(1, 0, 0), c=(0, 0, 0) )

            # Delete history
            cmds.delete(ctrl_name, constructionHistory=True)

            # Parent ctrl to group and group to wrist end joint
            cmds.parent(ctrl_name, grp_name)
            cmds.setAttr(ctrl_name + '.rotateY', 0)
            cmds.setAttr(ctrl_name + '.rotateZ', 90)

            # Move the group to the joint
            cmds.xform(grp_name, t=grp_pos, ws=True)
            cmds.parent(grp_name, jnt_name)

            # Lock and hide ctrl attributes
            cmds.setAttr(ctrl_name + '.tx', edit=True,  lock=True, keyable=False, channelBox=False)
            cmds.setAttr(ctrl_name + '.ty', edit=True,  lock=True, keyable=False, channelBox=False)
            cmds.setAttr(ctrl_name + '.tz', edit=True,  lock=True, keyable=False, channelBox=False)
            cmds.setAttr(ctrl_name + '.rx', edit=True,  lock=True, keyable=False, channelBox=False)
            cmds.setAttr(ctrl_name + '.ry', edit=True,  lock=True, keyable=False, channelBox=False)
            cmds.setAttr(ctrl_name + '.rz', edit=True,  lock=True, keyable=False, channelBox=False)
            cmds.setAttr(ctrl_name + '.sx', edit=True,  lock=True, keyable=False, channelBox=False)
            cmds.setAttr(ctrl_name + '.sy', edit=True,  lock=True, keyable=False, channelBox=False)
            cmds.setAttr(ctrl_name + '.sz', edit=True,  lock=True, keyable=False, channelBox=False)
            
            # Deselect to avoid parenting
            cmds.select(d=True)

# THIS SECTION NEEDS SOME REFINING                       
# Connect Ik and Fk to bind joints
cmds.parentConstraint(names['ikPrefix'] + names['shoulder'] + names['jointSufix'], names['bindPrefix'] + names['shoulder'] + names['jointSufix'], weight = 0.0)
cmds.parentConstraint(names['fkPrefix'] + names['shoulder'] + names['jointSufix'], names['bindPrefix'] + names['shoulder'] + names['jointSufix'])
cmds.parentConstraint(names['ikPrefix'] + names['elbow'] + names['jointSufix'], names['bindPrefix'] + names['elbow'] + names['jointSufix'], weight = 0.0)
cmds.parentConstraint(names['fkPrefix'] + names['elbow'] + names['jointSufix'], names['bindPrefix'] + names['elbow'] + names['jointSufix'])
cmds.parentConstraint(names['ikPrefix'] + names['wrist'] + names['jointSufix'], names['bindPrefix'] + names['wrist'] + names['jointSufix'], weight = 0.0)
cmds.parentConstraint(names['fkPrefix'] + names['wrist'] + names['jointSufix'], names['bindPrefix'] + names['wrist'] + names['jointSufix'])

# Create blend attribute
ctrl_name = names['controlPrefix'] + names['armSufix']
cmds.select(d=True)
cmds.select(ctrl_name)
cmds.addAttr(ctrl_name, ln=names['blendingNode'], at='long', min=0, max=10, dv=0)
cmds.setAttr(ctrl_name + '.' + names['blendingNode'], edit=True, keyable=True)
cmds.setAttr(ctrl_name + '.' + names['blendingNode'], 0)

# Create nodes to perform the blend
tmp_multDiv = cmds.createNode('multiplyDivide', n=names['multiplyDividePrefix'] + names['blendingNode'])
cmds.connectAttr(ctrl_name + '.' + names['blendingNode'], tmp_multDiv + '.input1X')
cmds.setAttr(tmp_multDiv + '.input2X', 10)

tmp_plusMinus = cmds.createNode('plusMinusAverage', n=names['plusMinusPrefix'] + names['blendingNode'])
cmds.setAttr(tmp_plusMinus + '.operation', 2)
cmds.setAttr(tmp_plusMinus + '.input1D[0]', 100)
cmds.connectAttr(tmp_multDiv + '.output.outputX', tmp_plusMinus + '.input1D[1]')

cmds.connectAttr(tmp_multDiv + '.output.outputX', 'bn_shoulder_jnt_parentConstraint1.ik_shoulder_jntW0')
cmds.connectAttr(tmp_plusMinus + '.output1D', 'bn_shoulder_jnt_parentConstraint1.fk_shoulder_jntW1')
cmds.connectAttr(tmp_multDiv + '.outputX', 'bn_elbow_jnt_parentConstraint1.ik_elbow_jntW0')
cmds.connectAttr(tmp_plusMinus + '.output1D', 'bn_elbow_jnt_parentConstraint1.fk_elbow_jntW1')
cmds.connectAttr(tmp_multDiv + '.output.outputX', 'bn_wrist_jnt_parentConstraint1.ik_wrist_jntW0')
cmds.connectAttr(tmp_plusMinus + '.output1D', 'bn_wrist_jnt_parentConstraint1.fk_wrist_jntW1')