from __future__ import print_function
import random
import math

def say(x): print(x, end="")

# Schaffer Model
def f1(x):
	return x**2

def f2(x):
	return (x-2)**2

def baselineStudy(numSamples):
	sample = [random.uniform(-10**5, 10**5) for _ in xrange(numSamples)]
	energies = [f1(n) + f2(n) for n in sample]
	return min(energies), max(energies)

# Simulated Annealer
def neighbor(currSol, radius):
	return random.uniform(max(currSol-radius, -10**5), min(currSol+radius, 10**5))

def energy(sampleMin, sampleMax, f1, f2, x):
	return (float(f1(x) + f2(x) - sampleMin) / (sampleMax - sampleMin))

def p(currEn, nextEn, t):
	return math.exp(-1*(currEn-nextEn)/t)

def printHeader(seed, kmax, initialSol, neighborRadius):
	print("Simulated Annealing on the Schaffer model")
	print("Parameters: \n   Seed: %s\n   kmax: %d\n   initialSol: %.2f\n   neighborRadius: %.2f\n" % (seed, kmax, initialSol, neighborRadius))
	say("%4s : %-12s %-15s" % ("k", "bestSol", "bestEn"))
	say("\n%s" % ("-"*37))

def printUpdate(k, bestSol, bestEn):
	say("\n%4d : %-10g   %-15g |  " % (k, bestSol, bestEn))

def sa(seed=42, kmax=1000, initialSol=100, neighborRadius=500):
	random.seed(seed)
	sampleMin, sampleMax = baselineStudy(1000)
	sampleEMax = sampleMax - 100

	currSol = neighbor(0,10**5)
	currEn = energy(sampleMin, sampleMax, f1, f2, currSol)
	bestSol, bestEn = currSol, currEn
	k = 0
	printHeader(seed, kmax, initialSol, neighborRadius)
	printUpdate(k, bestSol, bestEn)
	while k < kmax:
		k += 1
		nextChar = "."
		nextSol = neighbor(currSol, neighborRadius)
		nextEn = energy(sampleMin, sampleMax, f1, f2, nextSol)
		if nextEn < bestEn:
			bestSol, bestEn = nextSol, nextEn
			currSol, currEn = nextSol, nextEn
			nextChar = "!"
		elif nextEn < currEn:
			currSol, currEn = nextSol, nextEn
			nextChar = "+"
		elif p(currEn, nextEn, float(k)/kmax) < random.random():
			currSol, currEn = nextSol, nextEn
			nextChar = "?"
		say(nextChar)
		if k % 25 == 0:
			printUpdate(k, bestSol, bestEn)
	print("")
	return bestSol, bestEn

result = sa()