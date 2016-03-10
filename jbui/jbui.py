import maya.cmds as cmds
import rig.rig_arm_w5 as rig
'''
def rigarm(*args):
	rig.rigArm()	
	
myMenu = cmds.menu('RDojo_Menu', label='RDMenu', to=True, p='MayaWindow')
cmds.menuItem(label='Rig Arm', p=myMenu, command=rigarm)
'''
class RDojo_UI:

	def __init__(self, *args):
		mi = cmds.window('MayaWindow', ma=True, q=True)
		for m in mi:
			if m == 'RDOJO_Menu':
				cmds.deleteUI('RDojo_Menu', m=True)

		myMenu = cmds.menu('RDojo_Menu', label='RDMenu', to=True, p='MayaWindow')
		cmds.menuItem(label='Rig Tool', p=myMenu, command=self.ui)

		# Dictionary to store UI elements
		self.UIElements = {}

	def ui(self, *args):
		# Check to see if UI exists
		windowName = 'Window'
		if cmds.window(windowName, exists=True):
			cmds.deleteUI(windowName)
		# Define Width and Height for buttons and windows
		windowWidth = 480
		windowHeight = 80
		buttonWidth = 100
		buttonHeight = 30

		self.UIElements['window'] = cmds.window(windowName, width=windowWidth, height=windowHeight, title='RDojo_UI', sizeable=True)
		self.UIElements['mainColLayout'] = cmds.columnLayout(adjustableColumn=True)
		self.UIElements['guiFrameLayout1'] = cmds.frameLayout(label='Layout', borderStyle='in', p=self.UIElements['mainColLayout'])
		self.UIElements['guiFlowLayout1'] = cmds.flowLayout(v=False, width=windowWidth, height=windowHeight/2, wr=True, bgc=[0.2, 0.2, 0.2], p=self.UIElements['guiFrameLayout1'])

		# Menu listing all the layout files
		cmds.separator(w=10, hr=True, st='none', p=self.UIElements['guiFlowLayout1'])
		self.UIElements['rig_button'] = cmds.button(label='rig_arm', width=buttonWidth, height=buttonHeight, bgc=[0.2, 0.4, 0.2], p=self.UIElements['guiFlowLayout1'], c=self.rigarm)

		# Show the Window
		cmds.showWindow(windowName)

	def rigarm(*args):
		rig.rigArm()


