import numpy as np
import cv2
from PIL import Image

class Length:
    def __init__(self, file_name, BAU):
        # Use Baidu API to get images
        self.orig_name = file_name
        BAU.upload(self.orig_name)
        self.data = BAU.getBodyAnalysis()
        BAU.getBodySeg()
        self.left_hip_y = self.data["person_info"][0]["body_parts"]["left_hip"]['y']
        self.right_hip_y = self.data["person_info"][0]["body_parts"]["right_hip"]['y']
        self.left_shoulder = self.data["person_info"][0]["body_parts"]["left_shoulder"]
        self.left_shoulder_y = self.left_shoulder['y']
        self.right_shoulder = self.data["person_info"][0]["body_parts"]["right_shoulder"]
        self.right_shoulder_y = self.right_shoulder['y']
        self.ankle_left = self.data["person_info"][0]["body_parts"]["left_ankle"]['y']
        self.ankle_right = self.data["person_info"][0]["body_parts"]["right_ankle"]['y']

        self.pixel_height = self.data["person_info"][0]["location"]["height"]

        self.hip_hi = max(self.left_hip_y, self.right_hip_y)
        self.hip_low = min(self.left_hip_y, self.right_hip_y)
        self.shoulder_hi = max(self.left_shoulder_y, self.right_shoulder_y)
        self.shoulder_low = min(self.left_shoulder_y, self.right_shoulder_y)

        self.ankle = (self.ankle_left + self.ankle_right) / 2
        self.shoulder = (self.shoulder_low + self.shoulder_hi) / 2
        self.hip = (self.left_hip_y + self.right_hip_y) / 2

        # 1/4 shoulder to hip, averaged
        self.dist_y = (self.shoulder_hi - self.hip_hi + self.shoulder_low - self.hip_low) / 8

        self.height = None
        if 'front' in file_name:
            self.noArmLabelFileName = self.remove_noise()
        if 'side' in file_name:
            self.noArmLabelFileName = self.orig_name.split('.')[0] + "-labelmap.png"

    def input_height(self, height_input):
        self.height = height_input

    def remove_noise(self):
        black = (0, 0, 0)
        name = self.orig_name.split('.')[0] + "-labelmap.png"
        img = Image.open(name)
        width, height = img.size
        plist = []
        for row in range(height):
            for col in range(width):
                if col > self.left_shoulder['x'] or col < self.right_shoulder['x']:
                    element = (col, row)
                    plist.append((element, black))
        for p in plist:
            img.putpixel(p[0], p[1])
        noArmFileName = name.split('.')[0] + "withoutNoise.png"
        img.save(noArmFileName)
        return noArmFileName


    def hip_measure(self):

        name = self.noArmLabelFileName
        img = cv2.imread(name)
        # print(img.shape)
        # print(int(hip_y))
        # print(np.sum(img[int(hip_y),700:900, :] == 0))
        # ==0 checks for black pixels, subtract black to get white
        # Each [0,0,0] becomes [True, True, True], so divide by 3
        hip_measure = np.sum(img[int(self.hip), :,:] == 255)/3
        if self.height is not None:
            hip_measure = self.height * hip_measure/self.pixel_height

        return hip_measure

    def chest_measure(self):
        # Get y-position for chest
        chest_y = self.shoulder - self.dist_y

        name = self.noArmLabelFileName
        img = cv2.imread(name)
        # Each [0,0,0] becomes [True, True, True], so divide by 3
        chest_measure = np.sum(img[int(chest_y), :, :] == 255) / 3
        if self.height is not None:
            chest_measure = self.height * chest_measure/self.pixel_height
        return chest_measure

    def waist_measure(self):
        # Get y-position for waist
        waist_y = self.dist_y + self.hip

        name = self.noArmLabelFileName
        img = cv2.imread(name)
        # Each [0,0,0] becomes [True, True, True], so divide by 3
        waist_measure = np.sum(img[int(waist_y), :, :] == 255) / 3
        if self.height is not None:
            waist_measure = self.height * waist_measure/self.pixel_height
        return waist_measure

    def leg_measure(self):
        # Get leg length
        leg_measure = - self.hip + self.ankle
        if self.height is not None:
            leg_measure = self.height * leg_measure/self.pixel_height
        return leg_measure