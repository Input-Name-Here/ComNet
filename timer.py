import time
class Timer:
	def __init__(self):
		self.tstart = time.clock()
		self.tnow = self.tstart
	def elapsed(self):
		return (self.tnow-self.tstart)