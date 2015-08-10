import anim

class TaR:
	def __init__(self, size):
		self.state = anim.Anim(1,4)
		self.tortoise = anim.Anim(1,size)
		self.rabbit = anim.Anim(1,size)
		self.result = 1

	def Update(self):
		self.state.Next()
		#self.result = 1
		if self.state.Get() == 1:
			self.result = self.rabbit.Get()
			self.rabbit.Next()
		if self.state.Get() == 2:
			self.result = self.rabbit.Get()
			self.rabbit.Next()
		if self.state.Get() == 3:
			self.result = self.tortoise.Get()
		if self.state.Get() == 4:
			self.result = self.tortoise.Get()
			self.tortoise.Next()

	def Get(self):
		return self.result

class Naive:
	def __init__(self, size, ticks=1):
		self.ticks = ticks;
		self.state = anim.Anim(1,ticks)
		self.pointer = anim.Anim(1,size)
		self.result = 1

	def Update(self):
		self.state.Next()

		if self.state.Get()==self.ticks:
			self.pointer.Next()
			self.result = self.pointer.Get()

	def Get(self):
		return self.result
