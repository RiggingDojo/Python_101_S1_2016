import maya.cmds as cmds
 
 
joint_info = [['shoulder_jnt', [2.1, 0.0, 5.0]], ['elbow_jnt', [-0.1, 0.0, 0.0]], ['wrist_jnt', [-0.1, 0.0, -5.0]], ['wristEnd_jnt',[1.0, 0.0, -8.0]]]
 
def createJoints(args):
    """
    Create joints based on how many the users lays down
     
    Parameters
        Right now its a nested list with name and postion for each of the joints
     
    Returns
        Returns the joints names into a list         
     
    """
    for joints in args:
        cmds.joint(n=joints[0], p=joints[1])
    cmds.select(d=True)
    print ("Joints Made...:"), args
     
createJoints(joint_info)
     
 
 
