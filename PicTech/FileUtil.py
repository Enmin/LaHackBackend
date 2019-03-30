import configparser


def readConfigSections(filename):
	cf = configparser.ConfigParser()
	cf.read(filename)
	return cf.sections()


def readConfig(category, filename="PicTech.conf"):
	cf = configparser.ConfigParser()
	cf.read(filename)
	info = dict()
	for key in cf[category]:
		info[key]=cf[category][key]
	return info


def readPicture(filename):
	with open(filename, 'rb') as f:
		image = f.read()
	return image