import random

class Candidate(object):
	def __init__(self):
		self.decisions = []	
		self.scores = []
		self.energy = None

# model as class
class Model(object):
	def __init__(self):
		self.decisionRanges = []
		self.objectives = []
		self.constraints = []
		self.sampleMin = 0
		self.sampleMax = 1
		print self.objectives

	def eval(self, candidate, energyFunction):
		candidate.scores = [objective(candidate.decisions) for objective in self.objectives]
		candidate.energy = self.energyFunction(self, candidate.scores)
		return candidate

	def isValid(self, candidate):
		return False not in ([len(candidate.decisions) == len(self.decisionRanges)] + 
			[x >= y[0] and x <= y[1] for x, y in zip(candidate.decisions, self.decisionRanges)] + 
			[constraint(candidate.decisions) for constraint in self.constraints])
	
	def generateRandomCandidate(self):
		can = Candidate()
		can.decisions = [random.uniform(low, high) for low, high in self.decisionRanges]
		return can

	def sumEnergyFunction(self, scores):
		return sum(scores - self.sampleMin) / (self.sampleMax - self.sampleMin)

	# can only run this if the baseline study has been run
	def sumNormalizedEnergyFunction(self, scores):
		return (float(sum(scores) - self.sampleMin))

	def baselineStudy(self, numSamples=100):
		validSample = []
		while len(validSample) < numSamples:
			can = self.generateRandomCandidate()
			if self.isValid(can): 
				validSample.append(self.eval(can, energyFunction=self.sumEnergyFunction).energy) 
		self.sampleMin, self.sampleMax = min(validSample), max(validSample)

class Schaffer(Model):
	def f1(self, x):
		return x[0]**2
	def f2(self, x):
		return (x[0]-2)**2
	def __init__(self):
		Model.__init__(self)
		self.decisionRanges = [(-10**5, 10**5)]
		self.objectives = [self.f1, self.f2]
		self.constraints = []
		self.energyFunction = Model.sumNormalizedEnergyFunction

class Osyczka2(Model):
	def f1(self, x):
		return -1*(25*(x[0]-2)**2 + 
			          (x[1]-2)**2 + 
			          (x[2]-1)**2 * (x[3]-4)**2 +
			          (x[4]-1)**2)
	def f2(self, x):
		return sum(var**2 for var in x)
	def g1(self, x):
		return 0 <= x[0] + x[1] - 2
	def g2(self, x):
		return 0 <= 6 - x[0] - x[1]
	def g3(self, x):
		return 0 <= 2 - x[1] + x[0]
	def g4(self, x):
		return 0 <= 2 - x[0] - 3*x[1]
	def g5(self, x):
		return 0 <= 4 - (x[2]-3)**2 - x[3]
	def g6(self, x):
		return 0 <= (x[4]-3)**3 + x[5] - 4
	def __init__(self):
		Model.__init__(self)
		self.decisionRanges = [(0, 10), (0, 10), (1,  5)
		                       (0,  6), (1,  5), (0, 10)]
		self.objectives = [self.f1, self.f2]
		self.constraints = [self.g1, self.g2, self.g3, self.g4, self.g5, self.g6]
		self.energyFunction = Model.sumNormalizedEnergyFunction

# Default a,b values taken from: https://github.com/vivekaxl/TuningWei/blob/master/witschey/models/kursawe.py
class Kursawe(Model):
	def f1(self, x):
		return sum(-10*math.exp(-0.2*math.sqrt(x[i]**2 + x[i+1]**2)) for i in xrange(2))
	def f2(self, x):
		return sum(x[i]**self.a + 5*math.sin(x[i])**self.b for i in xrange(3))
	def __init__(self, a=0.8, b=3):
		self.a, self.b = a, b
		Model.__init__(self)
		self.decisionRanges = [(-5, 5) for _ in xrange(3)]
		self.objectives = [self.f1, self.f2]
		self.constraints = []
		self.energyFunction = Model.sumNormalizedEnergyFunction

#def run(model):
#	can = Candidate()
#	can.decisions = [10**5]
#	can = model.eval(can)
#	print can.scores
#	print can.energy
#	print model.isValid(can)

#run(Schaffer())