import configparser
from PIL import Image

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


def getKeyPointsGraph(filename, bodyAnalysisData):
	img = Image.open(filename)
	data = bodyAnalysisData['person_info'][0]['body_parts']
	plist = []
	Green = (220, 20, 60)
	Blue = (0, 0, 255)
	for points in data:
		pixel = (int(data[points]['x']), int(data[points]['y']))
		for i in range(0, 10):
			for j in range(0, 10):
				element = (pixel[0] + i, pixel[1] + j)
				if points == 'right_hip' or points == 'left_hip' or points == 'right_shoulder' or points == 'left_shoulder':
					plist.append((element, Blue))
				else:
					plist.append((element, Green))
	for p in plist:
		img.putpixel(p[0], p[1])
	return img


def getEllipticDict():
	f = open('Data/elliptic')
	ellipticDict = dict()
	for line in f.readlines():
		data = line.strip()
		for segs in data.split(' '):
			temp = segs.split(',')
			t = temp[0]
			v = temp[1]
			ellipticDict[t] = v
	return ellipticDict