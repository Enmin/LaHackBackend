import sys
import os
src = os.path.join("src")
sys.path.append(src)
import FileUtil
from BaiduApiUtil import BaiduApiUtil
from Estimate import Estimate
import cv2
from PIL import Image


def remove_noise(filename):
	black = (0, 0, 0)
	name = filename.split('.')[0] + "-labelmap.png"
	img = Image.open(name)
	rowNum, colNum = img.size
	plist = []
	for row in range(rowNum):
		for col in range(colNum):
			element = (row, col)
			plist.append((element, black))
	for p in plist:
		img.putpixel(p[0], p[1])
	img.show()


if __name__ == "__main__":
	resources = os.path.join("resources")
	config = os.path.join(resources, "PicTech.conf")
	configSection = 'Baidu_MeasuringTech'
	tokenSection = 'Access_Token'
	baiduApiUtil = BaiduApiUtil(config, configSection)
	# token = baiduApiUtil.getAccessToken(config, tokenSection)
	picDir = os.path.join("pictures")
	frontPicturePath = os.path.join(picDir, "kim-front.jpg")
	sidePicturePath = os.path.join(picDir, "kim-side.jpg")
	height = 165
	ellipticPath = os.path.join(resources, "elliptic")
	ellipticTable = FileUtil.getEllipticDict(ellipticPath)
	estimate = Estimate(frontPicturePath, sidePicturePath, height, ellipticTable, baiduApiUtil)
	print(estimate.getGeneral())
	# remove_noise(frontPicturePath)

# [{'body_parts': {
# 	'left_hip': {'y': 2146.9375, 'x': 1774.875, 'score': 0.8371440768241882},
# 	'top_head': {'y': 431.75, 'x': 1576.96875, 'score': 0.8823502063751221},
# 	'right_mouth_corner': {'y': 695.625, 'x': 1511.0,
# 	                       'score': 0.8953208923339844},
# 	'neck': {'y': 959.5, 'x': 1576.96875, 'score': 0.8825457692146301},
# 	'left_shoulder': {'y': 1157.40625, 'x': 1972.78125,
# 	                  'score': 0.8565347790718079},
# 	'left_knee': {'y': 2806.625, 'x': 1774.875, 'score': 0.8393064141273499},
# 	'left_ankle': {'y': 3466.3125, 'x': 1774.875, 'score': 0.8872614502906799},
# 	'left_mouth_corner': {'y': 695.625, 'x': 1642.9375,
# 	                      'score': 0.9071674346923828},
# 	'right_elbow': {'y': 1685.15625, 'x': 1115.1875,
# 	                'score': 0.8862749338150024},
# 	'right_ear': {'y': 629.65625, 'x': 1445.03125, 'score': 0.8626993298530579},
# 	'nose': {'y': 629.65625, 'x': 1576.96875, 'score': 0.9026660919189453},
# 	'left_eye': {'y': 563.6875, 'x': 1642.9375, 'score': 0.915635347366333},
# 	'right_eye': {'y': 563.6875, 'x': 1511.0, 'score': 0.9304162263870239},
# 	'right_hip': {'y': 2146.9375, 'x': 1445.03125, 'score': 0.8523308634757996},
# 	'left_wrist': {'y': 2080.96875, 'x': 2170.6875,
# 	               'score': 0.8832540512084961},
# 	'left_ear': {'y': 629.65625, 'x': 1774.875, 'score': 0.8812475204467773},
# 	'left_elbow': {'y': 1619.1875, 'x': 2038.75, 'score': 0.8656414747238159},
# 	'right_shoulder': {'y': 1157.40625, 'x': 1247.125,
# 	                   'score': 0.8892698287963867},
# 	'right_ankle': {'y': 3466.3125, 'x': 1379.0625,
# 	                'score': 0.8877508640289307},
# 	'right_knee': {'y': 2872.59375, 'x': 1379.0625,
# 	               'score': 0.8585851788520813},
# 	'right_wrist': {'y': 2146.9375, 'x': 1049.21875,
# 	                'score': 0.8908341526985168}},
#   'location': {'height': 3517.32275390625, 'width': 1343.536376953125,
#                'top': 342.8582763671875, 'score': 0.9966311454772949,
#                'left': 950.19287109375}}, {'body_parts': {
# 	'left_hip': {'y': 1296.25, 'x': 1792.75, 'score': 0.01917260885238647},
# 	'top_head': {'y': 772.8125, 'x': 2106.8125, 'score': 0.0132254371419549},
# 	'right_mouth_corner': {'y': 710.0, 'x': 1729.9375,
# 	                       'score': 0.0722261294722557},
# 	'neck': {'y': 1024.0625, 'x': 1729.9375, 'score': 0.3230763077735901},
# 	'left_shoulder': {'y': 1149.6875, 'x': 1939.3125,
# 	                  'score': 0.5256544947624207},
# 	'left_knee': {'y': 1086.875, 'x': 1918.375, 'score': 0.02454372122883797},
# 	'left_ankle': {'y': 1673.125, 'x': 2148.6875, 'score': 0.0860513225197792},
# 	'left_mouth_corner': {'y': 689.0625, 'x': 1750.875,
# 	                      'score': 0.1163931488990784},
# 	'right_elbow': {'y': 1694.0625, 'x': 2106.8125,
# 	                'score': 0.07779794931411743},
# 	'right_ear': {'y': 793.75, 'x': 1729.9375, 'score': 0.09961669147014618},
# 	'nose': {'y': 689.0625, 'x': 1709.0, 'score': 0.11806420981884},
# 	'left_eye': {'y': 605.3125, 'x': 1709.0, 'score': 0.1030475348234177},
# 	'right_eye': {'y': 668.125, 'x': 1729.9375, 'score': 0.04064510390162468},
# 	'right_hip': {'y': 1317.1875, 'x': 1813.6875, 'score': 0.03003906086087227},
# 	'left_wrist': {'y': 1673.125, 'x': 2085.875, 'score': 0.1710410714149475},
# 	'left_ear': {'y': 856.5625, 'x': 1729.9375, 'score': 0.06111426651477814},
# 	'left_elbow': {'y': 1673.125, 'x': 2064.9375, 'score': 0.4505440592765808},
# 	'right_shoulder': {'y': 1149.6875, 'x': 1939.3125,
# 	                   'score': 0.3108630180358887},
# 	'right_ankle': {'y': 1694.0625, 'x': 2190.5625,
# 	                'score': 0.02336873300373554},
# 	'right_knee': {'y': 1107.8125, 'x': 1897.4375,
# 	               'score': 0.02821076475083828},
# 	'right_wrist': {'y': 1673.125, 'x': 2085.875,
# 	                'score': 0.04579510539770126}}, 'location': {
# 	'height': 571.3296508789062, 'width': 1115.65576171875,
# 	'top': 759.9586791992188, 'score': 0.006836964283138514,
# 	'left': 1847.969482421875}}], 'log_id': 4486832811900771022}


