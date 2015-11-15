from __future__ import print_function
import random
import math
import models

def say(x): print(x, end="")

# Note: could return None
def randomNeighbor(model, currentCandidate, lives=10):
	if lives == 0:
		return None
	newCandidate = models.Candidate()
	for i in xrange(len(currentCandidate.decisions)):
		newDec = currentCandidate.decisions[i]
		if random.random() < 0.3 or len(currentCandidate.decisions) == 1:
			low, high = model.decisionRanges[i]
			newDec += (high-low)/10.0*random.random()*(1 if random.random() < 0.5 else -1) 
		newCandidate.decisions.append(newDec)
	if model.isValid(newCandidate):
		return model.eval(newCandidate, energyFunction=model.sumNormalizedEnergyFunction)
	else:
		return randomNeighbor(model, currentCandidate, lives=lives-1)

def p(currEn, nextEn, t):
	return math.exp((currEn-nextEn)/t)

def printHeader(seed, kmax, initialSol):
	print("Simulated Annealing on the Schaffer model")
	print("Parameters: \n   Seed: %s\n   kmax: %d\n   initialSol: %s\n" % (seed, kmax, str(initialSol)))
	say("%4s : %-12s %-15s" % ("k", "bestSol", "bestEn"))
	say("\n%s" % ("-"*37))

def printUpdate(k, bestSol, bestEn):
	say("\n%4d : %-10s   %-15g |  " % (k, str(bestSol), bestEn))

def sa(model, seed=42, kmax=1000):
	random.seed(seed)
	model.baselineStudy(1000)
	currentCandidate = model.eval(model.generateRandomCandidate(), model.sumNormalizedEnergyFunction)
	bestCandidate = currentCandidate

	k = 0
	printHeader(seed, kmax, currentCandidate.decisions)
	printUpdate(k, bestCandidate.decisions, bestCandidate.energy)
	while k < kmax:
		k += 1
		nextChar = "."
		nextCandidate = randomNeighbor(model, currentCandidate)
		if nextCandidate.energy < bestCandidate.energy:
			bestCandidate = nextCandidate
			currentCandidate = nextCandidate
			nextChar = "!"
		elif nextCandidate.energy < currentCandidate.energy:
			currentCandidate = nextCandidate
			nextChar = "+"
		elif p(currentCandidate.energy, nextCandidate.energy, float(k)/kmax) < random.random():
			currentCandidate = nextCandidate
			nextChar = "?"
		say(nextChar)
		if k % 25 == 0:
			printUpdate(k, bestCandidate.decisions, bestCandidate.energy)
	print("")
	return bestCandidate