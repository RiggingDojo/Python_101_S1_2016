import maya.cmds as cmds

print "This is RDUI"


# The UI class
class RDojo_UI:

   def __init__(self, *args):
       print 'In RDojo_UI'






def rigarm(*args):
	
	print "Rig_Arm test again"




'''
Split into functions

1) Define joints - check
2) Create joints

3) IK controls
4) FK controls
5) Blend nodes

'''





def define_arm_joints(*args):
    #prefix list and dict initialize
    jnt_arm_info = [['shoulder', [-8.0, 0.0, 0.0]], ['elbow', [0.0, 0.0, -2.0]], 
           ['wrist', [8.0, 0.0, 0.0]], ['wristEnd',[10.0, 0.0, 0.0]]]
    jnt_prefix = ['ikj_', 'fkj_', 'rigj_']
    jnt_dict = {}

    #for x in jnt_arm_info:
    #	print x

    for pfx in jnt_prefix:
        tmp_list = []
        for jnt in jnt_arm_info:
            tmp_list.append([pfx + jnt[0], jnt[1]])
        
        jnt_dict[pfx] = tmp_list



    




#Create all joints
def create_joints(jnt_dict, *args):
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


	    return jnt_rot






# ---- IK Controls ----
def make_ik_controls(jnt_dict, jnt_rot, *args):
	#Create IK Handle
	cmds.ikHandle( name='ikh_arm', sj='ikj_shoulder', ee='ikj_wrist', sol='ikRPsolver')


	#IK wrist control and zero group
	cmds.circle( n='ikh_ctrl_arm', normal=(1, 0, 0), radius=1.5)
	cmds.group('ikh_ctrl_arm', n='grp_ikh_ctrl_arm', world=True)
	cmds.xform('grp_ikh_ctrl_arm', ws=True, t=jnt_arm_info[2][1], ro=jnt_rot[2])

	#parent ik handle to ik control shape
	cmds.parent( 'ikh_arm', 'ikh_ctrl_arm' )


	#Pole Vector
	#Create control and zero group
	cmds.spaceLocator( name='ctrl_pv_arm')
	cmds.group( 'ctrl_pv_arm', n='grp_ctrl_pv_arm', world=True)
	cmds.xform('grp_ctrl_pv_arm', ws=True,  t=(jnt_arm_info[1][1][0], jnt_arm_info[1][1][1], jnt_arm_info[1][1][2]-6.0))

	#Apply pole vector contraint
	cmds.poleVectorConstraint( 'ctrl_pv_arm', 'ikh_arm' )







# ---- FK Controls ----
def make_fk_controls(jnt_dict, jnt_rot, *args):
	for val in range(len(jnt_dict['fkj_'])-1):
	    temp_name = 'fk_ctrl_' + jnt_arm_info[val][0]

	    cmds.circle( n= temp_name, normal=(1, 0, 0))
	    cmds.group(temp_name, n='grp_' + temp_name, world=True)
	    cmds.xform('grp_' + temp_name, ws=True, t=jnt_arm_info[val][1], ro=jnt_rot[val])
	    
	    #connect rotation controls to fk joints
	    cmds.connectAttr(temp_name + '.rotate', jnt_dict['fkj_'][val][0] + '.rotate')







# ---- Blend Nodes ----
def connect_blend_nodes(*args):
	#create blendColor nodes and connect them to the ik and fk control joints
	for x in range(len(jnt_arm_info)-1):
	    node_name = 'bldNode_' + str(jnt_arm_info[x][0]) + 'ikfk'
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
	       







rdojo_menu = cmds.menu( 'RDojo_Menu', label='RD Menu', to=True, p='MayaWindow')
cmds.menuItem(label='Rig_Arm test', p=rdojo_menu, command=rigarm)
cmds.menuItem(label='Define Arm Joints', p=rdojo_menu, command=define_arm_joints)
cmds.menuItem(label='Create Arm Joints', p=rdojo_menu, command=create_joints)
cmds.menuItem(label='Make IK Controls', p=rdojo_menu, command=make_ik_controls)
cmds.menuItem(label='Make FK Controls', p=rdojo_menu, command=make_fk_controls)
cmds.menuItem(label='Connect Blend Nodes', p=rdojo_menu, command=connect_blend_nodes)





