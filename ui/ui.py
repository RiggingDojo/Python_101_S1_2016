import maya.cmds as cmds

print "This is UI"

def rigarm(*args):
	print "Rig_Arm test again"


# The UI class
class RDojo_UI:

   def __init__(self, *args):
       print 'In RDojo_UI'


mymenu = cmds.menu( 'RDojo_Menu', label='RD Menu', to=True, p='MayaWindow')
cmds.menuItem(label='Rig_Arm', p=mymenu, command=rigarm)



