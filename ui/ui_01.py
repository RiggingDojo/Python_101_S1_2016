from PySide import QtGui as qg 
from PySide import QtCore as qc

import maya.cmds  as mc
import pymel.core as pm

import maya.OpenMayaUI as mui
import shiboken

import rig.rig_arm_classes as rig_classes
reload(rig_classes)

class RDojo_UI(qg.QDialog):
    def __init__(self):
        qg.QDialog.__init__(self)
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setObjectName( 'RDojo_UI v1.00' )
        self.setWindowTitle( 'RDojo_UI v1.00' )
        self.setFixedWidth(314)

        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)

        scroll_area = qg. QScrollArea()
        scroll_area.setWidgetResizable( True )
        scroll_area.setFocusPolicy( qc.Qt.NoFocus )
        scroll_area.setHorizontalScrollBarPolicy( qc.Qt.ScrollBarAlwaysOff )
        self.layout().addWidget( scroll_area )

        main_widget = qg.QWidget()
        main_layout = qg.QVBoxLayout()
        main_layout.setContentsMargins(5,5,5,5)
        main_layout.setAlignment(qc.Qt.AlignTop)
        main_widget.setLayout(main_layout)
        scroll_area.setWidget(main_widget)

        self.interp_layout = qg.QVBoxLayout()
        self.interp_layout.setContentsMargins(0,0,0,0)
        self.interp_layout.setSpacing(0)
        self.interp_layout.setAlignment(qc.Qt.AlignTop)
        main_layout.addLayout(self.interp_layout)

        button_layout = qg.QHBoxLayout()
        button_layout.setContentsMargins(0,0,0,0)
        button_layout.setAlignment(qc.Qt.AlignRight)
        main_layout.addLayout(button_layout)

        # Creating Instance of RDojoWidget()
        new_widget = RDojoWidget()
        
        self.interp_layout.addWidget(new_widget)

        self._interp_widget = []
        self._interp_widget.append(new_widget)

        self._dock_widget = self._dock_name = None

    #------------------------------------------------------------------------------------------#

    def connectDockWidget( self, dock_name, dock_widget ):
        self._dock_widget = dock_widget
        self._dock_name = dock_name

    def close( self ):
        if self._dock_widget:
            mc.deleteUI( self._dock_name )
        else:
            qg.QDialog.close( self )
        self._dock_widget = self._dock_name = None

#--------------------------------------------------------------------------------------------------#


class RDojoWidget(qg.QFrame):
    def __init__(self, *args, **kwargs):
        qg.QFrame.__init__(self, *args, **kwargs)
        
        self.setLayout(qg.QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        self.layout().setSpacing(5)
        self.setFrameStyle(qg.QFrame.Panel | qg.QFrame.Raised)
        self.setFixedHeight(150)

        
        self.main_widget = qg.QWidget()
        self.main_widget.setObjectName('mainWidget')
        self.main_widget.setLayout(qg.QVBoxLayout())
        self.main_widget.layout().setContentsMargins(2,2,2,2)
        self.main_widget.layout().setSpacing(5)
        self.layout().addWidget(self.main_widget)
        

        
        select_layout = qg.QHBoxLayout()
        button_layout = qg.QHBoxLayout()
        check_layout  = qg.QHBoxLayout()
        
        self.main_widget.layout().addLayout( select_layout )
        self.main_widget.layout().addLayout( button_layout )
        self.main_widget.layout().addLayout( check_layout )

        
        #adds widget to layout


        rigarm_button = qg.QPushButton( 'Rig Arm' )
        select_layout.addWidget( rigarm_button )
        
        #set the height and width of the button
        #select_layout.addSpacerItem(qg.QSpacerItem(5, 5, qg.QSizePolicy.Expanding))
        #select_layout.addSpacerItem(qg.QSpacerItem(5, 5, qg.QSizePolicy.Expanding))
       
        
        # connect modifers
        rigarm_button.clicked.connect( rig_classes.Rig_Arm )
        

#--------------------------------------------------------------------------------------------------#

dialog = None

def create(docked=True):
    global dialog

    if dialog is None:
        dialog = RDojo_UI()

    # docking window if statment    
    if docked is True:
        ptr = mui.MQtUtil.mainWindow()
        main_window = shiboken.wrapInstance(long(ptr), qg.QWidget)

        dialog.setParent( main_window )
        size = dialog.size()
        #return proper full name
        name = mui.MQtUtil.fullName(long(shiboken.getCppPointer(dialog)[0]))
        dock = mc.dockControl(
            allowedArea =['right', 'left'],
            area        = 'left',
            floating    = True,
            content     = name,
            width       = size.width(),
            height      = size.height(),
            label       = 'RDojo_UI v1.00' )

        # Convert to Dock widget
        widget      = mui.MQtUtil.findControl(dock)
        dock_widget = shiboken.wrapInstance(long(widget), qc.QObject)
        dialog.connectDockWidget( dock, dock_widget )

    else:
        dialog.show()


def delete():
    global dialog
    if dialog:
        dialog.close()
        dialog = None
