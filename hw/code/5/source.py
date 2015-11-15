from __future__ import print_function
import random
import math
import sys

def say(x): print(x, end="")

# Osyczka2 Model

modelRanges = {0: [0, 10], 1: [0, 10], 2: [1, 5], 3: [0, 6], 4: [1, 5], 5: [0, 10]}
INFTY = sys.maxsize

def f1(x):
	return -1*(25*(x[0]-2)**2 + (x[1]-2)**2 + (x[2]-1)**2 * (x[3]-4)**2 + (x[4]-1)**2)

def f2(x):
	return sum(y**2 for y in x)

# Hardcoded constraint check
def isValid(x):
	if not (0 <= x[0] + x[1] - 2)       \
	or not (0 <= 6 - x[0] - x[1])       \
	or not (0 <= 2 - x[1] + x[0])       \
	or not (0 <= 2 - x[0] + 3*x[1])     \
	or not (0 <= 4 - (x[2]-3)**2 -x[3]) \
	or not (0 <= (x[4]-3)**3+x[5]-4):
		return False
	else:
		return True

def randomValidSol():
	solution = [random.uniform(modelRanges[x][0], modelRanges[x][1]+1) for x in xrange(0,6)]
	while(not isValid(solution)):
		solution = [random.uniform(modelRanges[x][0], modelRanges[x][1]+1) for x in xrange(0,6)]
	return solution

# MaxWalkSat
def mutateToValidSol(solution, index, timeout=100):
	counter = 0
	solution[index] = random.uniform(modelRanges[index][0], modelRanges[index][1]+1);
	while(not isValid(solution) and counter < timeout):
		counter += 1
		solution[index] = random.uniform(modelRanges[index][0], modelRanges[index][1]+1);
	return solution

def pickBestValidSol(solution, index):
	tempSol = solution[:]
	increment = (modelRanges[index][1]-modelRanges[index][0])/10.0
	tempSol[index] = modelRanges[index][0]
	bestSol, bestEn = None, INFTY
	for _ in xrange(10):
		if(isValid(solution) and energy(tempSol) < bestEn):
			bestSol, bestEn = tempSol, energy(tempSol)
		tempSol[index] += increment
	return bestSol, bestEn

def energy(x):
	return f1(x) + f2(x)

def printHeader(seed=42, maxTries=1000, maxChanges=10, p=0.5):
	print("MaxWalkSat on the Osyczka2 model")
	print("Parameters: \n   Seed: %s\n   maxTries: %d\n   maxChanges: %.2f\n   p: %.2f\n" % (seed, maxTries, maxChanges, p))
	say("%4s : %-12s %-15s" % ("k", "bestSol", "bestEn"))
	say("\n%s" % ("-"*37))

def printUpdate(k, bestSol, bestEn):
	say("\n%4d : %-10s   %-15g |  " % (k, bestSol, bestEn))

def maxwalksat(seed=42, maxTries=200, maxChanges=5, p=0.5):
	printHeader(seed, maxTries, maxChanges, p)
	random.seed(seed)
	bestSol, bestEn = None, INFTY
	nextSol, nextEn = None, INFTY
	currEn = INFTY
	gen = 0

	for i in xrange(0, maxTries):
		currEn = nextEn
		nextSol = randomValidSol()
		for j in xrange(0, maxChanges):
			gen += 1
			nextChar = "."
			changeIndex = random.randint(0,5)
			if p < random.random():
				mutateToValidSol(nextSol, changeIndex)
				nextEn = energy(nextSol)
			else:
				nextSol, nextEn = pickBestValidSol(nextSol, changeIndex)
				if nextSol == None:
					say(nextChar)
					if gen % 25 == 0:
						printUpdate(gen, "Omitted", bestEn)
					break;
			if nextEn < bestEn:
				bestSol, bestEn = nextSol, nextEn
				nextChar = "!"
			elif nextEn > currEn:
				nextChar = "+"
			say(nextChar)
			if gen % 25 == 0:
				printUpdate(gen, "Omitted", bestEn)
	print("")
	return bestSol, bestEn

result = maxwalksat()