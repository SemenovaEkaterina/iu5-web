class Date:
	def __init__(self, day, month, year):
		self.day = day
		self.month = month
		self.year = year
	
	@staticmethod
	def fromstring(s):
		day, month, year = map(int, s.split('-'))
		return Date(day, month, year)

	def __str__(self):
		return '%02d-%02d-%02d' % (self.day, self.month, self.year)


d = Date.fromstring('01-02-2012')
print d
