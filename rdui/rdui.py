'''
Creates a menu that produces a rigging tool window. 
This window has buttons to rig an arm and eventually other tools. 
'''


import maya.cmds as cmds
import rig.rig_arm as rig
import system.utils as utils
import os
from functools import partial
reload(utils)
reload(rig)

print "This is RDUI\n"

arm_obj = rig.Rig_Arm()




##############
# Menu Items #
##############


class RDojo_UI:

    def __init__(self, *args):
        print 'In RDojo_UI'
        #Create menu and menu items for creating arm rig.
        mi = cmds.window('MayaWindow', q=True, ma=True)

        #Delete existing menu
        for m in mi:
            if m == 'RDojo_Menu':
                cmds.deleteUI('RDojo_Menu', m=True)
                print('Deleting existing menu')


        rdojo_menu = cmds.menu( 'RDojo_Menu', label='RD Menu', to=True, p='MayaWindow')
        cmds.menuItem(label='Rig Tool', p=rdojo_menu, command=self.ui)
        

        '''Dictionary to store layouts, buttons, etc.'''
        self.UIElements = {}







    def ui(self, *args):
        '''Check if the UI exists'''
        print('This is RDojo_UI.ui')
        window_name = 'window'
        if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name)

        '''define dimensions of window and buttons'''
        window_width = 350
        window_height = 480
        button_width = 50
        button_height = 30
        field_width = 100

        self.UIElements['window'] = cmds.window(window_name, width=window_width, height=window_height, title='RDojo_UI', rtf=True)

        self.UIElements['mainColLayout'] = cmds.columnLayout( adjustableColumn=True )
        self.UIElements['guiFrameLayout1'] = cmds.frameLayout( label='Layout', borderStyle='out', p=self.UIElements['mainColLayout'] )
        self.UIElements['guiFlowLayout1'] = cmds.flowLayout( v=False, width=window_width, height=window_height/2, wr=True, bgc=[0.2, 0.2, 0.2], p=self.UIElements['guiFrameLayout1'])
        self.UIElements['rowColumnLayout1'] = cmds.rowColumnLayout( numberOfColumns=3, columnAlign=[ (1, 'right'), (2, 'right'), (3, 'right')], columnWidth=[(1, 100), (2, 150), (3, 100)] )

        self.UIElements['joint1_label'] = cmds.text( label='Joint1 Name', p=self.UIElements['rowColumnLayout1'])
        self.UIElements['enter_name'] = cmds.textField( width=field_width, p=self.UIElements['rowColumnLayout1'])
        self.UIElements['separator'] = cmds.separator( h=10, style='none')

        self.UIElements['separator'] = cmds.separator( h=10, style='none')
        self.UIElements['separator'] = cmds.separator( h=10, style='none')
        self.UIElements['separator'] = cmds.separator( h=10, style='none')

        self.UIElements['joint1_xvalue'] = cmds.intFieldGrp( numberOfFields=3, value1=0, value2=0, value3=0, p=self.UIElements['guiFlowLayout1'])
        #self.UIElements['separator'] = cmds.separator( h=10, style='none')
        #self.UIElements['separator'] = cmds.separator( h=10, style='none')

        self.UIElements['separator'] = cmds.separator( h=10, style='none')
        self.UIElements['separator'] = cmds.separator( h=10, style='none')
        self.UIElements['separator'] = cmds.separator( h=10, style='none')

        self.UIElements['rig_button'] = cmds.button(label='rig_arm', width=button_width, height=button_height, bgc=[0.2, 0.4, 0.2], p=self.UIElements['rowColumnLayout1'], command=self.rig_arm_full_button)
        self.UIElements['separator'] = cmds.separator( h=10, style='none')
        self.UIElements['separator'] = cmds.separator( height=10, style='none' )

        self.UIElements['separator'] = cmds.separator( h=10, style='none')
        self.UIElements['separator'] = cmds.separator( h=10, style='none')
        self.UIElements['separator'] = cmds.separator( h=10, style='none')

        self.UIElements['define_joints'] = cmds.button(label='Define Joints', width=button_width, height=button_height, bgc=[0.2, 0.2, 0.4], p=self.UIElements['rowColumnLayout1'], command=self.define_joints_button)
        self.UIElements['create_arm_joints'] = cmds.button(label='Create Arm Joints', width=button_width, height=button_height, bgc=[0.2, 0.2, 0.4], p=self.UIElements['rowColumnLayout1'], command=self.create_joints_button)
        self.UIElements['make_ik_controls'] = cmds.button(label='Make IK Controls', width=button_width, height=button_height, bgc=[0.2, 0.2, 0.4], p=self.UIElements['rowColumnLayout1'], command=self.make_ik_controls_button)
        
        self.UIElements['make_fk_controls'] = cmds.button(label='Make FK Controls', width=button_width, height=button_height, bgc=[0.2, 0.2, 0.4], p=self.UIElements['rowColumnLayout1'], command=self.make_fk_controls_button)
        self.UIElements['connect_blend_nodes'] = cmds.button(label='Blend Nodes', width=button_width, height=button_height, bgc=[0.2, 0.2, 0.4], p=self.UIElements['rowColumnLayout1'], command=self.connect_blend_nodes_button)
        self.UIElements['separator'] = cmds.separator( h=10, style='none')
        
        self.UIElements['json_filename'] = cmds.textFieldGrp( label='Json Filename: ', text='enter filename', p=self.UIElements['guiFlowLayout1'])
        self.UIElements['writeJson_field'] = cmds.textFieldGrp( label='Json Filename: ', text='enter data', p=self.UIElements['guiFlowLayout1'])
        self.UIElements['separator'] = cmds.separator( h=10, style='none')

        self.UIElements['writeJson_button'] = cmds.button( 'writeJson_button', command=partial(utils.writeJson, os.environ["RD_DATA"] + self.UIElements['json_filename'], self.UIElements['writeJson_field']))
        #self.UIElements['writeJson_button'] = cmds.button( command=utils.writeJson(self.UIElements['json_filename'], self.UIElements['writeJson_field']))

        '''Show the window'''
        cmds.showWindow(window_name)



    #Creates an arm rig and controls by performing all 
    def rig_arm_full_button(*args):
        arm_obj.rig_arm()


        



    #define which joints will be built and where they will be placed. 
    def define_joints_button(*args):
        arm_obj.define_joints(arm_obj.jnt_arm_info, arm_obj.jnt_prefix, arm_obj.jnt_dict)


        




    #Create all joints
    def create_joints_button(*args):
        arm_obj.create_joints(arm_obj.jnt_dict, arm_obj.jnt_rot)
        





    # ---- IK Controls ----
    # creates ik controls to drive the rotation values of the ik arm_obj.joints
    def make_ik_controls_button(*args):
        arm_obj.make_ik_controls(arm_obj.jnt_arm_info, arm_obj.jnt_dict, arm_obj.jnt_rot)







    # ---- FK Controls ----
    # creates fk controls to drive the rotation values of the fk arm_obj.joints
    def make_fk_controls_button(*args):
        arm_obj.make_fk_controls(arm_obj.jnt_arm_info, arm_obj.jnt_dict, arm_obj.jnt_rot)






    # ---- Blend Nodes ----
    # Use the color blend attribute to connect ik and fk rotational values to drive arm_obj.joints
    def connect_blend_nodes_button(*args):
        arm_obj.connect_blend_nodes(arm_obj.jnt_arm_info, arm_obj.jnt_dict)




    def text_entry(*args):
        '''text field that takes the joint name information'''
        cmds.text( label='Joint 1:' )
        self.name_joint = cmds.textField()
        '''text field that takes the joint placement - 3 floats separated by commas'''
        '''assign values in fields to class variables'''

        '''function that holds two functions 1)text_entry 2)writeJson '''

