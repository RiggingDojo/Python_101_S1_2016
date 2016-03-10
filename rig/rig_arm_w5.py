import maya.cmds as cmds
import json
import system.utils as utils
import rig.Arm
import os

def rigArm():
	reload(rig.Arm)
	from rig.Arm import Arm as Arm

	fileNames = os.environ['RDOJO_DATA'] + 'default_labels.json'        
	filePos = os.environ['RDOJO_DATA'] + 'default_positions.json'
	names = json.loads(utils.readJson(fileNames))
	jntPos = json.loads(utils.readJson(filePos))
	myArm = Arm(jntPos, names)
	myArm.rigArm()

if __name__ == '__main__':
	rigArm()