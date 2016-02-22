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

