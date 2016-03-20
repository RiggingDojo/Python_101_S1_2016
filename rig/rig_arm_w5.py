import rig.Arm


def rigArm():
	reload(rig.Arm)
	from rig.Arm import Arm as Arm

	myArm = Arm()
	myArm.rigArm()

if __name__ == '__main__':
	rigArm()
