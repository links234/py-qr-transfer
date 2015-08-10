class Anim:
	def __init__(self, left, right, start=-1):
		if start==-1:
			start = left
		self.curr = start
		self.left = left
		self.right = right

	def Next(self):
		self.curr += 1

		if self.curr > self.right:
			self.curr = self.left

	def Prev(self):
		self.curr -= 1

		if self.curr < self.left:
			self.curr = self.right;

	def Get(self):
		return self.curr
