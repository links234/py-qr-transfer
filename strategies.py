import anim
import random
import math

class TaR:
	def __init__(self, size):
		self.state = anim.Anim(1,4)
		self.tortoise = anim.Anim(1,size)
		self.rabbit = anim.Anim(1,size)
		self.result = 1

	def Update(self):
		self.state.Next()

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
		self.ticks = ticks
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

class Random:
	def __init__(self, size, ticks=1):
		self.ticks = ticks
		self.size = size
		self.state = anim.Anim(1,ticks)
		self.result = 1

	def Update(self):
		self.state.Next()

		if self.state.Get()==self.ticks:
			self.result = random.randrange(1,self.size+1)

	def Get(self):
		return self.result


SEGMENT_SIZE = 9
SEGMENT_TICKS = SEGMENT_SIZE*5

class Segments:
	def __init__(self, size):
		self.offset = 0
		self.segment = anim.Anim(1, math.ceil(size/SEGMENT_SIZE))
		self.state = anim.Anim(1, SEGMENT_TICKS)
		self.pattern = TaR(SEGMENT_SIZE)
		self.result = 1
		self.size = size

	def Update(self):
		self.state.Next()

		if self.state.Get()==SEGMENT_TICKS:
			self.segment.Next()
			print "next segment = ",self.segment.Get()
			self.offset = (self.segment.Get()-1)*SEGMENT_SIZE
			self.pattern = TaR(min(SEGMENT_SIZE,self.size-self.offset))
			self.result = self.offset+self.pattern.Get()
		else:
			self.pattern.Update()
			self.result = self.offset+self.pattern.Get()

	def Get(self):
		return self.result
