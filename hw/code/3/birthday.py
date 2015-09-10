import random

# Exercise 10.15 #8
def print_header(people, runs, seed):
	print "Birthday Paradox Estimator"
	print "Parameters:\n   People:%d\n   Runs:%d\n   Seed:%d" % (people, runs, seed)


def has_duplicates(mylist):
	return len(mylist) != len(set(mylist))

def birthday_paradox_estimator(people=23, runs=1000, seed=42):
	print_header(people, runs, seed)
	random.seed(seed)
	count = 0
	for i in xrange(runs):
		birthdays = [random.randint(1, 366) for _ in xrange(people)]
		count += has_duplicates(birthdays)
	return float(count)/runs 

print "Probability of collision: %0.2f%%" % (birthday_paradox_estimator(runs=10000)*100)