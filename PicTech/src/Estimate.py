import Length


class Estimate:
	def __init__(self, frontFileName, sideFileName, height, ellipticTable, bau):
		self.frontFigure = Length.Length(frontFileName, bau)
		self.frontFigure.input_height(height)
		self.sideFigure = Length.Length(sideFileName, bau)
		self.sideFigure.input_height(height)
		self.ellipticTable = ellipticTable

	def calculate_ellipse_parameter(self, long, short):
		table = self.ellipticTable
		t = round(short/long, 2)
		parameter = float(table[str(t)]) * (long + short)
		return parameter

	def getWaistEllipse(self):
		long_axis = self.frontFigure.waist_measure()/2
		short_axis = self.sideFigure.waist_measure()/2
		return self.calculate_ellipse_parameter(long_axis, short_axis)

	def getChestEllipse(self):
		long_axis = self.frontFigure.chest_measure()/2
		short_axis = self.sideFigure.chest_measure()/2
		return self.calculate_ellipse_parameter(long_axis, short_axis)

	def getHipEllipse(self):
		long_axis = self.frontFigure.hip_measure()/2
		short_axis = self.sideFigure.hip_measure()/2
		return self.calculate_ellipse_parameter(long_axis, short_axis)

	def getGeneral(self):
		generalData = dict()
		generalData['waist'] = self.getWaistEllipse()
		generalData['hip'] = self.getHipEllipse()
		generalData['chest'] = self.getChestEllipse()
		generalData['leg'] = (self.sideFigure.leg_measure() + self.frontFigure.leg_measure())/2
		return generalData