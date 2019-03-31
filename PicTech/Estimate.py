import math
import Length
import FileUtil as fu


class Estimate:
	def __init__(self, frontFileName, sideFileName):
		self.frontFigure = Length(frontFileName)
		self.sideFigure = Length(sideFileName)

	def calculate_ellipse_parameter(self, long, short):
		table = fu.getEllipticDict()
		t = round(short/long, 2)
		parameter = float(table[str(t)]) * (long + short)
		return parameter

	def getWaistEllipse(self):
		long_axis = self.frontFigure.waist_measure()
		short_axis = self.sideFigure.waist_measure()
		return self.calculate_ellipse_parameter(long_axis, short_axis)

	def getChestEllipse(self):
		long_axis = self.frontFigure.chest_measure()
		short_axis = self.sideFigure.chest_measure()
		return self.calculate_ellipse_parameter(long_axis, short_axis)

	def getHipEllipse(self):
		long_axis = self.frontFigure.hip_measure()
		short_axis = self.sideFigure.hip_measure()
		return self.calculate_ellipse_parameter(long_axis, short_axis)

	def getGeneral(self):
		generalData = dict()
		generalData['waist'] = self.getWaistEllipse()
		generalData['hip'] = self.getHipEllipse()
		generalData['chest'] = self.getChestEllipse()
		return generalData