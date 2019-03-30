import requests
import FileUtil as fu
import numpy as np
import demjson
import cv2
import base64
from aip import AipBodyAnalysis
from PIL import Image


class BaiduApiUtil:

	def __init__(self):
		keyInfo = fu.readConfig('Baidu_MeasuringTech', 'PicTech.conf')
		self.appid = keyInfo['appid']
		self.api_key = keyInfo['api_key']
		self.secret_key = keyInfo['secret_key']
		self.client = AipBodyAnalysis(self.appid, self.api_key, self.secret_key)
		self.filename = None
		self.picture = None
		self.picture_size = None
		self.picture_format = None

	def upload(self, filename):
		self.picture = fu.readPicture(filename)
		self.filename = filename.split('.')[0]
		img = Image.open(filename)
		self.picture_size = img.size
		self.picture_format = img.format

	def getAccessToken(self):
		keyInfo = fu.readConfig('Access_Token', 'PicTech.conf')
		host = keyInfo['addr'] % (keyInfo['grant_type'], keyInfo['client_id'], keyInfo['client_secret'])
		response = requests.post(host)
		if response.status_code != 200:
			print('Error Happened When Acquiring Access Token')
			return -1
		content = demjson.decode(response.text)
		if 'error' in content.keys():
			print('Invalid API Key or Secret Key')
			return -1
		return content['refresh_token']

	def getBodyAnalysis(self):
		return self.client.bodyAnalysis(self.picture)

	def getBodySeg(self):
		result = self.client.bodySeg(self.picture)

		foreground = base64.b64decode(result['foreground'])
		labelmap = base64.b64decode(result['labelmap'])
		scoremap = base64.b64decode(result['scoremap'])

		nparr_foreground = np.fromstring(foreground, np.uint8)
		foregroundimg = cv2.imdecode(nparr_foreground, 1)
		foregroundimg = cv2.resize(foregroundimg, self.picture_size, interpolation=cv2.INTER_NEAREST)
		im_new_foreground = np.where(foregroundimg == 1, 10, foregroundimg)
		cv2.imwrite(self.filename + '-foreground.png', im_new_foreground)

		nparr_labelmap = np.fromstring(labelmap, np.uint8)
		labelmapimg = cv2.imdecode(nparr_labelmap, 1)
		labelmapimg = cv2.resize(labelmapimg, self.picture_size, interpolation=cv2.INTER_NEAREST)
		im_new_labelmapimg = np.where(labelmapimg == 1, 255, labelmapimg)
		cv2.imwrite(self.filename + '-labelmap.png', im_new_labelmapimg)

		nparr_scoremap = np.fromstring(scoremap, np.uint8)
		scoremapimg = cv2.imdecode(nparr_scoremap, 1)
		scoremapimg = cv2.resize(scoremapimg, self.picture_size, interpolation=cv2.INTER_NEAREST)
		im_new_scoremapimg = np.where(scoremapimg == 1, 255, scoremapimg)
		cv2.imwrite(self.filename + '-scoremap.png', im_new_scoremapimg)


BAU = BaiduApiUtil()
BAU.upload("resources/test-model posture.jpg")
BAU.getBodySeg()
print(BAU.getBodyAnalysis())

