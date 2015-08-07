

class Anim:
	def __init__(self, startFrom, size):
		self.curr = startFrom
		self.size = size

	def Next(self):
		self.curr += 1

		if self.curr > self.size:
			self.curr = 1


	def Get(self):
		return self.curr
