import maya.cmds as cmds

sel = cmds.ls(sl=True)
print sel
     
def renameJoints(sel):
    """
    User selects joints that needed a prefix and function 
    goes through the joint chain and addes a prefix to them
     
    Parameters
        The number of selected joints by user
         
    Returns
        Returns a list of new names
         
    """
     
    prefix = raw_input("What prefix would you like to use?:"+"\n")
          
    for i in sel:
        print ("Your new name is: "),prefix + str(i)
        cmds.rename(str(i), prefix+str(i))
 
renameJoints(sel)