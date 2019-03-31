import math
import Length
import FileUtil as fu


class Estimate:
	def __init__(self, frontFileName, sideFileName, height):
		self.frontFigure = Length.Length(frontFileName)
		self.frontFigure.input_height(height)
		self.sideFigure = Length.Length(sideFileName)
		self.sideFigure.input_height(height)

	def calculate_ellipse_parameter(self, long, short):
		table = fu.getEllipticDict()
		t = round(short/long, 2)
		parameter = float(table[str(t)]) * (long + short)
		return parameter

	def getWaistEllipse(self):
		long_axis = self.frontFigure.waist_measure()/2
		short_axis = self.sideFigure.waist_measure()/2
		print('Waist')
		print(long_axis, short_axis)
		return self.calculate_ellipse_parameter(long_axis, short_axis)

	def getChestEllipse(self):
		long_axis = self.frontFigure.chest_measure()/2
		short_axis = self.sideFigure.chest_measure()/2
		print('Chest')
		print(long_axis, short_axis)
		return self.calculate_ellipse_parameter(long_axis, short_axis)

	def getHipEllipse(self):
		long_axis = self.frontFigure.hip_measure()/2
		short_axis = self.sideFigure.hip_measure()/2
		print('Hip')
		print(long_axis,short_axis)
		return self.calculate_ellipse_parameter(long_axis, short_axis)

	def getGeneral(self):
		generalData = dict()
		generalData['waist'] = self.getWaistEllipse()
		generalData['hip'] = self.getHipEllipse()
		generalData['chest'] = self.getChestEllipse()
		print(self.sideFigure.leg_measure(), self.frontFigure.leg_measure())
		generalData['leg'] = (self.sideFigure.leg_measure() + self.frontFigure.leg_measure())/2
		return generalData