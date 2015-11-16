from __future__ import print_function
import random
import math
import models

def say(x): print(x, end="")

# Note: could return None
def randomNeighbor(model, currentCandidate, lives=100):
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

def printHeaderSA(model, seed, kmax, initialSol):
	print("Simulated Annealing on the %s model" % (model.name))
	print("Parameters: \n   Seed: %s\n   kmax: %d\n   initialSol: %s\n" % (seed, kmax, str(initialSol)))
	say("%4s : %-12s %-15s" % ("k", "bestSol", "bestEn"))
	say("\n%s" % ("-"*37))

def printUpdateSA(k, bestSol, bestEn):
	say("\n%4d : %-10s   %-15g |  " % (k, str(bestSol), bestEn))

def sa(model, seed=42, kmax=1000):
	random.seed(seed)
	model.baselineStudy(1000)
	currentCandidate = model.eval(model.generateRandomCandidate(), model.sumNormalizedEnergyFunction)
	bestCandidate = currentCandidate

	k = 0
	printHeaderSA(model, seed, kmax, currentCandidate.decisions)
	printUpdateSA(k, bestCandidate.decisions, bestCandidate.energy)
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
			printUpdateSA(k, bestCandidate.decisions, bestCandidate.energy)
	print("")
	return bestCandidate

# mws methods:
def printHeaderMWS(model, seed=42, maxTries=1000, maxChanges=10, p=0.5):
	print("MaxWalkSat on the %s model" % (model.name))
	print("Parameters: \n   Seed: %s\n   maxTries: %d\n   maxChanges: %.2f\n   p: %.2f\n" % (seed, maxTries, maxChanges, p))
	say("%4s : %-12s %-15s" % ("k", "bestSol", "bestEn"))
	say("\n%s" % ("-"*37))

def printUpdateMWS(k, bestSol, bestEn):
	say("\n%4d : %-10s   %-15g |  " % (k, bestSol, bestEn))

def mutateToRandom(model, candidate, index, timeout=100):
	counter = 0
	candidate.decisions[index] = random.uniform(model.decisionRanges[index][0], model.decisionRanges[index][1]+1);
	while(not model.isValid(candidate) and counter < timeout):
		counter += 1
		candidate.decisions[index] = random.uniform(model.decisionRanges[index][0], model.decisionRanges[index][1]+1);
	return candidate

def mutateToBest(model, candidate, index):
	tempCandidate = candidate
	bestCandidate = candidate
	increment = (model.decisionRanges[index][1]-model.decisionRanges[index][0])/100.0
	tempCandidate.decisions[index] = model.decisionRanges[index][0]
	for _ in xrange(10):
		if(model.isValid(tempCandidate)):
			tempCandidate = model.eval(tempCandidate, energyFunction=model.sumNormalizedEnergyFunction)
		if(tempCandidate.energy < bestCandidate.energy):
			bestCandidate = tempCandidate
		tempCandidate.decisions[index] += increment
	return bestCandidate

def mws(model, seed=42, maxTries=200, maxChanges=5, p=0.5):
	printHeaderMWS(model, seed, maxTries, maxChanges, p)
	random.seed(seed)
	model.baselineStudy(1000)
	currentCandidate = model.eval(model.generateRandomCandidate(), model.sumNormalizedEnergyFunction)
	bestCandidate = currentCandidate
	gen = 0

	for i in xrange(0, maxTries): 
		nextCandidate = currentCandidate
		for j in xrange(0, maxChanges):
			gen += 1
			nextChar = "."
			changeIndex = random.randint(0,len(nextCandidate.decisions)-1)
			if p < random.random():
				nextCandidate = mutateToRandom(model, nextCandidate, changeIndex)
			else:
				nextCandidate = mutateToBest(model, nextCandidate, changeIndex)
				if not model.isValid(nextCandidate):
					say(nextChar)
					if gen % 25 == 0:
						printUpdateMWS(gen, "Omitted", bestCandidate.energy)
					break;
			if nextCandidate.energy < bestCandidate.energy:
				bestCandidate = nextCandidate
				nextChar = "!"
			elif nextCandidate.energy < currentCandidate.energy:
				currentCandidate = nextCandidate
				nextChar = "+"
			say(nextChar)
			if gen % 25 == 0:
				printUpdateMWS(gen, "Omitted", bestCandidate.energy)
	print("")
	return bestCandidate