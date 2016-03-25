import maya.cmds as cmds

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
         'armSufix': 'arm',
         'plusMinusPrefix': 'plusminus_',
         'multiplyDividePrefix': 'multdiv_',
         'blendingNode': 'FKIK_Blend'
         }

# Lists with joints data
jntInfo = [[names['shoulder'] + names['jointSufix'], [2.1, 0.0, 5.0]], 
              [names['elbow'] + names['jointSufix'], [-0.1, 0.0, 0.0]], 
              [names['wrist'] + names['jointSufix'], [-0.1, 0.0, -5.0]], 
              [names['wristEnd'] + names['jointSufix'], [-0.1, 0.0, -8.0]]]    
             
jntChains = (names['ikPrefix'],
                names['fkPrefix'], 
                names['bindPrefix'])
###############################################
###############################################
                
# Functions
def createDict(keys, values):
    
    dict = {}

    for label in keys:
        
        tmpJntList = []
        
        for i in range(len(values)):
            newName = label + values[i][0]
            tmpJntList.append([newName, values[i][1]])

        dict[label] = tmpJntList
    
    return dict
    
def lockAndHide(attrList, object):

    for attr in attrList:
        
        cmds.setAttr(object + attr, edit=True,  lock=True, keyable=False, channelBox=False)    
        
def createAlignCtrl(groupName, ctrlName, jointName, pos, rot):
    
    cmds.group(em=True, name=groupName)
    cmds.xform(groupName, ro=rot, ws=True)
    cmds.circle(n=ctrlName, nr=(1, 0, 0), c=(0, 0, 0))
    cmds.delete(ctrlName, constructionHistory=True)
    cmds.parent(ctrlName, groupName)
    cmds.setAttr(ctrlName + '.rotateY', 0)
    cmds.xform(groupName, t=pos, ws=True)
    cmds.orientConstraint(ctrlName, jointName)

def parentFKIKChains(dict):
    
    for key, value in dict.iteritems():
        
        for i in range(len(value)):
       
            jntName = value[i][0]
    
            if 'End' not in jntName:
                
                if key.startswith('ik'):
                    
                    jntBindName = jntName.replace(names['ikPrefix'], names['bindPrefix'])
                    cmds.parentConstraint(jntName, jntBindName, weight = 0)
                    
                elif key.startswith('fk'):
                    
                    jntName = value[i][0]
                    jntBindName = jntName.replace(names['fkPrefix'], names['bindPrefix'])
                    cmds.parentConstraint(jntName, jntBindName)

def createPV(jntName, ikHandleName, PVName):
    
    pos = cmds.xform(jntName, q=True, t=True, ws=True)
    pos[0] -= 2
    cmds.spaceLocator(n=PVName)
    cmds.xform(PVName, ws=True, t=pos)
    cmds.poleVectorConstraint(PVName, ikHandleName)
     
# This should be refactored to support chains of different lenghts, or types, such as leg chains      
def createArmFKIKBlend(ctrlName):

    # Create blend attribute
    cmds.select(d=True)
    cmds.select(ctrlName)
    cmds.addAttr(ctrlName, ln=names['blendingNode'], at='long', min=0, max=10, dv=0)
    cmds.setAttr(ctrlName + '.' + names['blendingNode'], edit=True, keyable=True)
    cmds.setAttr(ctrlName + '.' + names['blendingNode'], 0)
    
    # Create nodes to perform the blend
    multDivNode = cmds.createNode('multiplyDivide', n=names['multiplyDividePrefix'] + names['blendingNode'])
    cmds.connectAttr(ctrlName + '.' + names['blendingNode'], multDivNode + '.input1X')
    cmds.setAttr(multDivNode + '.input2X', 10)
    
    plusMinusNode = cmds.createNode('plusMinusAverage', n=names['plusMinusPrefix'] + names['blendingNode'])
    cmds.setAttr(plusMinusNode + '.operation', 2)
    cmds.setAttr(plusMinusNode + '.input1D[0]', 100)
    cmds.connectAttr(multDivNode + '.output.outputX', plusMinusNode + '.input1D[1]')

    cmds.connectAttr(multDivNode + '.output.outputX', names['bindPrefix'] + names['shoulder'] + names['jointSufix'] + '_parentConstraint1.' + names['ikPrefix'] + names['shoulder'] + names['jointSufix'] + 'W0')
    cmds.connectAttr(plusMinusNode + '.output1D', names['bindPrefix'] + names['shoulder'] + names['jointSufix'] + '_parentConstraint1.' + names['fkPrefix'] + names['shoulder'] + names['jointSufix'] + 'W1')
    cmds.connectAttr(multDivNode + '.outputX', names['bindPrefix'] + names['elbow'] + names['jointSufix'] + '_parentConstraint1.' + names['ikPrefix'] + names['elbow'] + names['jointSufix'] + 'W0')
    cmds.connectAttr(plusMinusNode + '.output1D', names['bindPrefix'] + names['elbow'] + names['jointSufix'] + '_parentConstraint1.' + names['fkPrefix'] + names['elbow'] + names['jointSufix'] + 'W1')
    cmds.connectAttr(multDivNode + '.output.outputX', names['bindPrefix'] + names['wrist'] + names['jointSufix'] + '_parentConstraint1.' + names['ikPrefix'] + names['wrist'] + names['jointSufix'] + 'W0')
    cmds.connectAttr(plusMinusNode + '.output1D', names['bindPrefix'] + names['wrist'] + names['jointSufix'] + '_parentConstraint1.' + names['fkPrefix'] + names['wrist'] + names['jointSufix'] + 'W1')
    
###############################################
###############################################

def rigArm():
    
    # Create dictionay with joint data
    jntDict = createDict(jntChains, jntInfo)
    
    # Iterate skeleton dictionary data to create joints, controls and groups       
    for key, value in jntDict.iteritems():
        
        for i in range(len(value)):
            
            tmpName = value[i][0]
            tmpPos = value[i][1]
            cmds.joint(n = tmpName, p = tmpPos)
        
        cmds.select(d = True)
        
        # Orient joints
        for i in range(len(value)):
            
            tmpName = value[i][0]
            cmds.joint(tmpName, edit=True, zso=True, oj='xyz', sao='yup')
        
        # Create controls and groups
        if key.startswith('fk'):
            
            for i in range(len(value)):
                
                jntName = value[i][0]
                grpPos = value[i][1]
                grpName = names['groupPrefix'] + names['controlPrefix'] + jntName[:-len(names['jointSufix'])]
                grpRot = cmds.xform(jntName, q=True, ro=True, ws=True)
                ctrlName = names['controlPrefix'] + jntName[:-len(names['jointSufix'])]
                
                if 'End' not in jntName:
                    
                    # Create and align control and group
                    createAlignCtrl(grpName, ctrlName, jntName, grpPos, grpRot)
    
                    # Lock and hide ctrl attributes
                    tmpAttrList = ('.tx', '.ty','.tz','.sx','.sy','.sz')
                    lockAndHide(tmpAttrList, ctrlName)
    
            # Parent cntrls
            cmds.parent(names['groupPrefix'] + names['controlPrefix'] + names['fkPrefix'] + names['elbow'], names['controlPrefix'] + names['fkPrefix'] + names['shoulder'])
            cmds.parent(names['groupPrefix'] + names['controlPrefix'] + names['fkPrefix'] + names['wrist'], names['controlPrefix'] + names['fkPrefix'] + names['elbow'])
    
            # Deselect to avoid parenting
            cmds.select(d=True)
            
        elif key.startswith('ik'):
            
            jntName = names['ikPrefix'] + names['wrist'] + names['jointSufix']
            grpPos = cmds.xform(names['ikPrefix'] + names['wrist'] + names['jointSufix'], q=True, t=True, ws=True)
            grpName = names['groupPrefix'] + names['controlPrefix'] + names['ikPrefix'] + names['wrist']
            grpRot = cmds.xform(jntName, q=True, ro=True, ws=True)
            ctrlName = names['controlPrefix'] + names['ikPrefix'] + names['wrist']
            ikHandleName = names['ikHandle'] + names['armSufix']
            PVName = names['ikPrefix'] + names['poleVector'] + names['armSufix']
            
            # Ik handle
            cmds.ikHandle(n=ikHandleName, ee=jntName, sj=names['ikPrefix'] + names['shoulder'] + names ['jointSufix'], sol='ikRPsolver', p=2, w=1 )
    
            # Create ik control
            createAlignCtrl(grpName, ctrlName, jntName, grpPos, grpRot)
            
            # Parent ikhandle to ctrl
            cmds.parent(ikHandleName, ctrlName)
            
            # Create pole vector
            createPV(names['ikPrefix'] + names['elbow'] + names['jointSufix'], ikHandleName, PVName)
            
            # Lock and hide ctrl attributes
            tmpAttrList = ('.sx','.sy','.sz')
            lockAndHide(tmpAttrList, ctrlName)
           
            # Deselect to avoid parenting
            cmds.select(d=True)
        
        elif key.startswith('bn'):
            
            jntName = value[i][0]
            
            if 'End' in jntName:
    
                # Create blend ctrl
                grpPos = value[i][1]
                grpName = names['groupPrefix'] + names['controlPrefix'] + names['armSufix']
                grpRot = cmds.xform(jntName, q=True, ro=True, ws=True)
                ctrlName = names['controlPrefix'] + names['armSufix']
                
                createAlignCtrl(grpName, ctrlName, jntName, grpPos, grpRot)
                
                # Move the group to the joint
                cmds.xform(grpName, t=grpPos, ws=True)
                cmds.parent(grpName, jntName)
    
                # Lock and hide ctrl attributes
                tmpAttrList = ('.tx','.ty','.tz', '.rx','.ry','.rz', '.sx','.sy','.sz')
                lockAndHide(tmpAttrList, ctrlName)
    
                # Deselect to avoid parenting
                cmds.select(d=True)
    
    # Connect Ik and Fk to bind joints
    parentFKIKChains(jntDict)
    
    # Create blend nodes
    createArmFKIKBlend(names['controlPrefix'] + names['armSufix'])

if __name__ == '__main__':

    rigArm()