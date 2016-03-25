import os
import jbui.jbui as ui

# Set a system path to data files.
os.environ['RDOJO_DATA'] = 'Users/BackboneLabs/Documents/Python_101_S1_2016/data/'
os.environ['RDOJO_RIG'] = 'Users/BackboneLabs/Documents/Python_101_S1_2016/rig/'
# Create our UI
reload(ui)
ui.RDojo_UI()
