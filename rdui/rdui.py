import maya.cmds as cmds

print "UI"

def rigarm(*args):
    print "Rig_Arm"

mymenu = cmds.menu('RDojo_Menu', label='RDMenu', to=True, p='MayaWindow')
cmds.menuItem(label='Rig_Arm', p=mymenu, command=rigarm)



    