import requests
import FileUtil as fu
import numpy as np
import demjson
import cv2
import base64
import BaiduApiUtil
from PIL import Image


class Length:
    def __init__(self):
        # Use Baidu API to get images
        self.orig_name = "bikini.jpg"
        BAU = BaiduApiUtil.BaiduApiUtil()
        BAU.upload("resources/" + self.orig_name)
        BAU.getBodySeg()
        self.data = BAU.getBodyAnalysis()
        self.left_hip_y = self.data["person_info"][0]["body_parts"]["left_hip"]['y']
        self.right_hip_y = self.data["person_info"][0]["body_parts"]["right_hip"]['y']
        self.left_shoulder = self.data["person_info"][0]["body_parts"]["left_shoulder"]['y']
        self.right_shoulder = self.data["person_info"][0]["body_parts"]["right_shoulder"]['y']
        self.ankle_left = self.data["person_info"][0]["body_parts"]["left_ankle"]['y']
        self.ankle_right = self.data["person_info"][0]["body_parts"]["right_ankle"]['y']

        self.ankle = self.ankle_left + self.ankle_right / 2
        self.shoulder = (self.shoulder_low + self.shoulder_hi) / 2
        self.hip = (self.left_hip_y + self.right_hip_y) / 2

        self.hip_hi = max(self.left_hip_y, self.right_hip_y)
        self.hip_low = min(self.left_hip_y, self.right_hip_y)
        self.shoulder_hi = max(self.left_shoulder, self.right_shoulder)
        self.shoulder_low = min(self.left_shoulder, self.right_shoulder)

        # 1/4 shoulder to hip, averaged
        self.dist_y = (self.shoulder_hi - self.hip_hi + self.shoulder_low - self.hip_low) / 8
        
    def hip_measure(self):

        name = "resources/" + self.orig_name.split('.')[0] + "-labelmap.png"
        img = cv2.imread(name)
        # print(img.shape)
        # print(int(hip_y))
        # print(np.sum(img[int(hip_y),700:900, :] == 0))
        # ==0 checks for black pixels, subtract black to get white
        # Each [0,0,0] becomes [True, True, True], so divide by 3
        hip_measure = 1200 - np.sum(img[int(self.hip), :,:] == 0)/3
        return hip_measure

    def chest_measure(self):
        # Get y-position for chest
        chest_y = self.shoulder - self.dist_y

        name = "resources/" + self.orig_name.split('.')[0] + "-labelmap.png"
        img = cv2.imread(name)
        # Each [0,0,0] becomes [True, True, True], so divide by 3
        chest_measure = 1200 - np.sum(img[int(chest_y), :, :] == 0) / 3
        return chest_measure

    def waist_measure(self):
        # Get y-position for waist
        waist_y = self.dist_y + self.hip

        name = "resources/" + self.orig_name.split('.')[0] + "-labelmap.png"
        img = cv2.imread(name)
        # Each [0,0,0] becomes [True, True, True], so divide by 3
        chest_measure = 1200 - np.sum(img[int(waist_y), :, :] == 0) / 3
        return chest_measure

    def leg_measure(self):
        # Get leg length
        leg_measure = self.hip - self.ankle
        return leg_measure