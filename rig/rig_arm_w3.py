import maya.cmds as cmds


#jnt_info holds all arm joint names and placement
jnt_info = [['shoulder', [-8.0, 0.0, 0.0]], ['elbow', [0.0, 0.0, -2.0]], 
           ['wrist', [8.0, 0.0, 0.0]], ['wristEnd',[10.0, 0.0, 0.0]]]



#prefix list and dict initialize
jnt_prefix = ['ikj_', 'fkj_', 'rigj_']
jnt_dict = {}
jnt_rot = []



#fill jnt_dict with lists of placements for all joints. 
for pfx in jnt_prefix:
    tmp_list = []
    for jnt in jnt_info:
        tmp_list.append([pfx + jnt[0], jnt[1]])
    
    jnt_dict[pfx] = tmp_list
    


#Create all joints
for key, value in jnt_dict.iteritems():
    for i in range(len(value)):
        cmds.joint(n = value[i][0], p=value[i][1])


    #Orient joints
    cmds.select( value[0][0] )
    cmds.joint( value[0][0] , e=True, oj='xyz', sao='yup', ch=True)
    cmds.select(d=True)


    #Store joint rotation values in jnt_rot list
    if key == 'rigj_':
        for y in range(len(value)):
            jnt_rot.append(cmds.xform(value[y][0], q=True, ws=True, ro=True))







# ---- IK Controls ----
#Create IK Handle
cmds.ikHandle( name='ikh_arm', sj='ikj_shoulder', ee='ikj_wrist', sol='ikRPsolver')



#IK wrist control and zero group
cmds.circle( n='ikh_ctrl_arm', normal=(1, 0, 0), radius=1.5)
cmds.group('ikh_ctrl_arm', n='grp_ikh_ctrl_arm', world=True)
cmds.xform('grp_ikh_ctrl_arm', ws=True, t=jnt_info[2][1], ro=jnt_rot[2])

#parent ik handle to ik control shape
cmds.parent( 'ikh_arm', 'ikh_ctrl_arm' )


#Pole Vector
#Create control and zero group
cmds.spaceLocator( name='ctrl_pv_arm')
cmds.group( 'ctrl_pv_arm', n='grp_ctrl_pv_arm', world=True)
cmds.xform('grp_ctrl_pv_arm', ws=True,  t=jnt_info[1][1])

#Apply pole vector contraint
cmds.poleVectorConstraint( 'ctrl_pv_arm', 'ikh_arm' )







# ---- FK Controls ----
for val in range(len(jnt_dict['fkj_'])-1):
    temp_name = 'fk_ctrl_' + jnt_info[val][0]

    cmds.circle( n= temp_name, normal=(1, 0, 0))
    cmds.group(temp_name, n='grp_' + temp_name, world=True)
    cmds.xform('grp_' + temp_name, ws=True, t=jnt_info[val][1], ro=jnt_rot[val])
    
    #connect rotation controls to fk joints
    cmds.connectAttr(temp_name + '.rotate', jnt_dict['fkj_'][val][0] + '.rotate')





# ---- Blend Nodes ----
#create blendColor nodes and connect them to the ik and fk control joints
for x in range(len(jnt_info)-1):
    node_name = 'bldNode_' + str(jnt_info[x][0]) + 'ikfk'
    cmds.shadingNode('blendColors', asShader=True, n= node_name)
    cmds.connectAttr(jnt_dict['ikj_'][x][0] + '.rotate', node_name + '.color1', force=True)
    cmds.connectAttr(jnt_dict['fkj_'][x][0] + '.rotate', node_name + '.color2', force=True)
    cmds.setAttr(node_name + '.blender', 0)



#Loop to connect RGB output of colorblend to rotate XYZ of rig bones 
arm_bones = ['shoulder', 'elbow', 'wrist']
colors = ['R', 'G', 'B']
axes = ['X', 'Y', 'Z']

for bone in arm_bones:
    for color in colors:
        for axis in axes:
            cmds.connectAttr('bldNode_' + bone + 'ikfk.output' + color, 'rigj_' + bone + '.rotate' + axis, force=True)
       

















