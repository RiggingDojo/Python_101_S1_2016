import maya.cmds as cmds
import os
from functools import partial


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

		# Dictionary to store the rig folder modules
		self.rigModList = []
		rigContents = os.listdir(os.environ['RDOJO_RIG'])
		# We filter which modules will appear in the combo list (pretty hardcoded and fake -_-)
		[
			self.rigModList.append(mod)
			for mod in rigContents
			if ('.pyc' not in mod) and
			('__init__' not in mod) and
			('.DS_Store' not in mod) and
			('Limb' not in mod) and
			('Layout' not in mod) and
			('Mirror' not in mod)
		]

	def ui(self, *args):
		# Check to see if UI exists
		windowName = 'Window'
		if cmds.window(windowName, exists=True):
			cmds.deleteUI(windowName)
		# Define Width and Height for buttons and windows
		windowWidth = 580
		windowHeight = 80
		buttonWidth = 100
		buttonHeight = 30

		self.UIElements['window'] = cmds.window(
												windowName,
												w=windowWidth,
												h=windowHeight,
												t='RDojo_UI',
												s=True
												)
		self.UIElements['mainColLayout'] = cmds.columnLayout(adj=True)
		self.UIElements['guiFrameLayout1'] = cmds.frameLayout(
															l='Layout',
															bs='in',
															p=self.UIElements['mainColLayout']
															)
		self.UIElements['guiFlowLayout1'] = cmds.flowLayout(
															v=False,
															w=windowWidth,
															h=windowHeight/2,
															wr=True,
															bgc=[0.2, 0.2, 0.2],
															p=self.UIElements['guiFrameLayout1']
														)
		cmds.separator(w=10, hr=True, st='none', p=self.UIElements['guiFlowLayout1'])
		self.UIElements['rigMenu'] = cmds.optionMenu('Rig_Install', l='Rig', p=self.UIElements['guiFlowLayout1'])
		# Dynamically make a button for each rigging module
		for mod in self.rigModList:
			itemName = mod.replace('.py', '')
			cmds.menuItem(l=itemName, p=self.UIElements['rigMenu'])
		cmds.separator(w=10, hr=True, st='none', p=self.UIElements['guiFlowLayout1'])
		# Make an option menu for 'left' and 'right' sides
		sides = ['left', 'right']
		self.UIElements['sideMenu'] = cmds.optionMenu('Side', l='Side', p=self.UIElements['guiFlowLayout1'])
		for s in sides:
			cmds.menuItem(l=s, p=self.UIElements['sideMenu'])
		# Make a button to run the rig script, Layout, and Mirror
		cmds.separator(w=10, hr=True, st='none', p=self.UIElements['guiFlowLayout1'])
		self.UIElements['layoutButton'] = cmds.button(
													l='Layout',
													w=buttonWidth,
													h=buttonHeight,
													bgc=[0.2, 0.4, 0.2],
													p=self.UIElements['guiFlowLayout1'],
													c=partial(self.rigMod, 'Layout')
													)
		self.UIElements['rigButton'] = cmds.button(
													l='Rig',
													w=buttonWidth,
													h=buttonHeight,
													bgc=[0.2, 0.4, 0.2],
													p=self.UIElements['guiFlowLayout1'],
													c=partial(self.rigMod, '')
													)
		self.UIElements['mirrorButton'] = cmds.button(
													l='Mirror',
													w=buttonWidth,
													h=buttonHeight,
													bgc=[0.2, 0.4, 0.2],
													p=self.UIElements['guiFlowLayout1'],
													c=partial(self.rigMod, 'Mirror')
													)
		# Show the Window
		cmds.showWindow(windowName)

	def rigMod(self, action, *args):
		# Get the selected options
		modFile = cmds.optionMenu(self.UIElements['rigMenu'], q=True, v=True)
		side = cmds.optionMenu(self.UIElements['sideMenu'], q=True, v=True)
		# Import attributes from a module
		mod = __import__('rig.' + action + modFile, {}, {}, [modFile])
		reload(mod)
		# Read attribute from the module and instanstiate class
		moduleClass = getattr(mod, mod.className)
		moduleClass(side)
