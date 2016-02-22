import maya.cmds as cmds
'''
To Send Code to Maya, ctrl-shift-p, and then ctrl-enter

'''


joint_info = [['shoulder_jnt', [2.1, 0.0, 5.0]], ['elbow_jnt', [-0.1, 0.0, 0.0]], ['wrist_jnt', [-0.1, 0.0, -5.0]], ['wristEnd_jnt',[1.0, 0.0, -8.0]]]

#Creating Empty Dictionary
joint_dict = {}

name_prefix = ('ikj_', 'fkj_', 'rigj_')
for p in name_prefix:
    #Create empty list
    tmpjnt_lst = []
    #iterate through the orginal list
    for i in range(len(joint_info)):
        #first element of the list
        new_name = p + joint_info[i][0]
        print new_name
        #add to the temp list
        tmpjnt_lst.append([new_name, joint_info[i][1]])
    
    #pairs the key to values, appends to the dictionary
    joint_dict[p] = tmpjnt_lst
   
print joint_dict

#Iterate through the dictionary keys
for k, dk in joint_dict.iteritems():
    #Iterate through the values of those keys and create Joints
    for values in dk:
        cmds.joint(n=values[0], p=values[1])
        #deselect after the every joint chain is created
    cmds.select(d=True)
        
      
print ("Finished Creating ik/fk/rig joints..")

############################################################################

#Orient the joints
sel = cmds.ls(sl=True)
print sel
for i in sel:
    cmds.joint(i, edit=True, zeroScaleOrient=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True) 


############################################################################

#Create ik handle for ikj joints
cmds.ikHandle( n='ikh_arm', sj='ikj_shoulder_jnt', ee='ikj_wrist_jnt', sol='ikRPsolver', p=2, w=1 )

#Create Ik controls
#holds world space position   
pos = cmds.xform('ikj_wrist_jnt', q=True, t=True, ws=True)

#create a empty group
cmds.group( em=True, name="grp_ctrl_ikWrist")

#Create circle control boject
cmds.circle (n='ctrl_ikWrist', nr=(0,0,1), c=(0,0,0))

#Parent the control to the goup
cmds.parent('ctrl_ikWrist', 'grp_ctrl_ikWrist')

#Move the gorup to the joint
cmds.xform('grp_ctrl_ikWrist', t=pos, ws=True)

#Parent ikh to ctrl
cmds.parent('ikh_arm', 'ctrl_ikWrist')

############################################################################


#Create FK rig

ctrl_info = [['shoulder_jnt', [2.1, 0.0, 5.0]], ['elbow_jnt', [-0.1, 0.0, 0.0]], ['wrist_jnt', [-0.1, 0.0, -5.0]], ['wristEnd_jnt',[1.0, 0.0, -8.0]]]


for i in range(3):
    cmds.circle(n='ctrl_fk_shoulder', nr=(0,0,1), c=(0,0,0))


def insertIntoDictKey(key, data, dict):
    if not key in my_dict:
        my_dict[key] = [data]    
    else:
        my_dict[key].append([data])    
 
 
 
