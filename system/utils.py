import maya.cmds as cmds
import json



def writeJson(fileName, data, *args):
	with open(fileName, 'w') as outfile:
		json.dump(data, outfile)
	file.close(outfile)


def readJson(fileName, *args):
	with open(fileName, 'r') as infile:
		data = (open(infile.name, 'r').read())
	return data


