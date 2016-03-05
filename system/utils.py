import json

def writeJson(filename, data):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)

def readJson(filename):
	with open(filename, 'r') as infile:
		data = (infile.read())
	return data