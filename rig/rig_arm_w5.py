import maya.cmds as cmds
import json
import system.utils as utils
from rig.Arm import Arm as Arm

def rigArm():
	fileNames = 'Users/BackboneLabs/Documents/Python_101_S1_2016/layout/default_labels.json'        
	filePos = 'Users/BackboneLabs/Documents/Python_101_S1_2016/layout/default_positions.json'
	names = json.loads(utils.readJson(fileNames))
	jntPos = json.loads(utils.readJson(filePos))

	myArm = Arm(jntPos, names)
	myArm.rigArm()

if __name__ == '__main__':
	rigArm()