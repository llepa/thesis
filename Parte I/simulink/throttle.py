import numpy as np
import random

class ThrottleMarkov:

	outValues = list()
	state = 1
	transitionMatrix = [[0.3, 0.3, 0.15, 0.1, 0.05, 0.04, 0.03, 0.01, 0.01, 0.01],
						[0.2, 0.2, 0.2, 0.1, 0.05, 0.05, 0.04, 0.03, 0.02, 0.01],
						[0.1, 0.15, 0.2, 0.2, 0.1, 0.1, 0.05, 0.05, 0.03, 0.02],
						[0.06, 0.1, 0.2, 0.2, 0.2, 0.1, 0.05, 0.04, 0.03, 0.02],
						[0.04, 0.07, 0.1, 0.2, 0.2, 0.2, 0.1, 0.05, 0.03, 0.01],
						[0.03, 0.04, 0.06, 0.1, 0.2, 0.2, 0.2, 0.1, 0.04, 0.03],
						[0.01, 0.03, 0.04, 0.07, 0.1, 0.2, 0.2, 0.2, 0.1, 0.05],
						[0.01, 0.03, 0.05, 0.1, 0.2, 0.2, 0.2, 0.1, 0.07, 0.03],
						[0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.2, 0.2, 0.1, 0.06],
						[0.02, 0.03, 0.05, 0.05, 0.1, 0.1, 0.2, 0.2, 0.15, 0.1]]

	def __init__(self, dim, ttMax, vMax):
		timestamps = sorted([random.random()*ttMax for i in range(dim)])
		values = [((10 - self.getState()) / 10)*vMax for i in range(dim)]
		self.outValues = [[timestamps[i], values[i]] for i in range(dim)]

	def getValues(self):
		return self.outValues

	def pick(self):
		r = np.random.random()
		i = 0
		p = self.transitionMatrix[self.state-1][i]
	
		while (r > p and i < len(self.transitionMatrix)):
			i += 1
			p += self.transitionMatrix[self.state-1][i]
			
		self.state = i + 1

	def getState(self):
		temp = self.state
		self.pick()
		return temp