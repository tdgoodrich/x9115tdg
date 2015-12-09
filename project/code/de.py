import sys, os, time, random
import arff
from sklearn.cluster import MiniBatchKMeans
import numpy as np
from itertools import product
import copy

dataset_dir = "datasets"

def readArff(filename):
	# Read in arff file
	dataset = arff.load(open(os.path.join(dataset_dir, filename + ".arff"), "rb"))
	data = np.array(dataset['data'])

	# Take only the numeric features (exclude the output field here)
	numericRows = [i for i in xrange(len(dataset["attributes"])-1) if dataset["attributes"][i][1] == "NUMERIC"]
	train = np.array([[row[i] for i in numericRows] for row in data], dtype=float)
	target = np.array([row[-1] for row in data], dtype=float)
	# If we want boolean target:
  	target = np.array([int(x > 0) for x in target], dtype=str)
  	return train, target

class Model(object):
	def __init__(self, **kwargs):
		self.num_decisions = kwargs.get("num_decisions")
		self.ranges = kwargs.get("ranges")
		self.dataset_name = kwargs.get("dataset_name")
		self.train, self.target = readArff(self.dataset_name)
	def low(self, decision):
		return self.ranges[decision][0]
	def high(self, decision):
		return self.ranges[decision][1]
	def get_num_decisions(self):
		return self.num_decisions
	def trim(self, value, decision):
		return max(self.low(decision), min(self.high(decision), value))
	def score(self, candidate):
		raise NotImplementedError("\"score\" method not implemented!")

class Model_KMeans(Model):
	def __init__(self, dataset_name):
		super(Model_KMeans, self).__init__(num_decisions=3, ranges=[(5, 50), (0, 20), (0.0, 1.0)], dataset_name=dataset_name)
	def score(self, candidate):
		n_clusters = int(candidate.get_value(0))
		max_no_improvement = int(candidate.get_value(1))
		reassignment_ratio = candidate.get_value(2)

		# Set up the learner we want
		samples = 15
		start = time.time()
		fscore = 0
		for x in xrange(samples):
			try: 
				learner = MiniBatchKMeans(n_clusters=n_clusters, max_no_improvement=max_no_improvement, reassignment_ratio=reassignment_ratio)
				
				# Form the clusters
				cluster_assignments = learner.fit_predict(self.train)
				
				# Get the bug prediction
				counts = [[0,0] for _ in xrange(n_clusters)]
				for point, assignment in enumerate(cluster_assignments):
		 			counts[assignment][int(self.target[point])] += 1
				cluster_bug_prediction = [0 if x[0] > x[1] else 1 for x in counts]
				bug_prediction = [str(cluster_bug_prediction[assignment]) for assignment in cluster_assignments]
				tp, tn, fp, fn = 0,0,0,0
				for actual, predicted in zip(self.target, bug_prediction):
					if actual == "1" and predicted == "1":
						tp += 1
					elif actual == "0" and predicted == "1":
						fp += 1
					elif actual == "1" and predicted == "0":
						fn += 1
				fscore += 2.0*tp/(2.0*tp+fp+fn)
			except:
				samples -= 1
				print n_clusters, max_no_improvement, reassignment_ratio
		#print "Time taken: ", time.time()-start
		#print "F-Score: ", fscore / samples
		return fscore / samples
		
class Candidate(object):
	def __init__(self, **kwargs):
		self.decisions = kwargs.get("decisions")
		self.score = None
		if kwargs.get("random"):
			self.init_random(kwargs.get("model"))
	def init_random(self, model):
		self.decisions = [random.uniform(model.low(decision), model.high(decision)) for decision in xrange(model.num_decisions)]
	def get_value(self, decision):
		return self.decisions[decision]

class Frontier(object):
	def __init__(self, **kwargs):
		self.candidates = kwargs.get("candidates", [])
		self.next_id = 0
	def get_candidates(self):
		return self.candidates
	def add(self, candidate):
		self.candidates.append(candidate)
	def pick_one(self, avoid=[]):
		candidate = self.candidates[int(random.random() * len(self.candidates))]
		if candidate in avoid:
			return self.pick_one(avoid=avoid)
		else:
			return candidate
	def pick_three(self):
		seen = []
		for _ in xrange(3):
			seen.append(self.pick_one(avoid=seen))
		return seen

def differential_evolution(model, repeats=30, np=100, f=0.75, cr=0.3, epsilon=0.001):
	start = time.time()
	random.seed(42)
	frontier = Frontier(candidates=[Candidate(random=True, model=model) for _ in xrange(np)])
	for candidate in frontier.candidates:
		candidate.score = model.score(candidate)
	last_score = 0
	#print "First frontier: ", frontier.candidates
	for k in xrange(repeats):
		print k
		frontier, total, n = update(model, f, cr, frontier)
		#print "New frontier: ", frontier.candidates
		score = total/n
		print "Generation score: ", score
		if score < (last_score + epsilon):
			break
		last_score = score
	stop = time.time()
	print "Run time: ", stop - start
	return last_score, frontier

def update(model, f, cr, frontier, total=0.0, n=0):
	new_frontier = Frontier()
	for candidate in frontier.get_candidates():
		new_candidate = extrapolate(model, frontier, candidate, f, cr)
		#print "Old candidate score: ", candidate, candidate.score
		#print "New candidate score: ", new_candidate, new_candidate.score
		if new_candidate.score > candidate.score:
			#print "Replacing candidate ", candidate, " with ", new_candidate
			new_frontier.add(new_candidate)
			total += new_candidate.score
		else:
			#print "Keeping candidate ", candidate
			new_frontier.add(candidate)
			total += candidate.score
		n += 1
	return new_frontier, total, n

def extrapolate(model, frontier, candidate, f, cr):
	new_candidate = copy.deepcopy(candidate)
	(x_candidate, y_candidate, z_candidate) = frontier.pick_three()
	changed = False
	for decision in xrange(model.get_num_decisions()):
		(x_value, y_value, z_value) = x_candidate.get_value(decision), y_candidate.get_value(decision), z_candidate.get_value(decision)
		if random.random() < cr:
			changed = True
			new_value = x_value + f * (y_value - z_value)
			new_candidate.decisions[decision] = model.trim(new_value, decision)
	if not changed:
		new_candidate = copy.deepcopy(x_candidate)
	new_candidate.score = model.score(new_candidate)
	return new_candidate


if __name__ == '__main__':
	dataset_name = sys.argv[1]
	model = Model_KMeans(dataset_name)
	nps = [20]
	crs = [0.3, 0.7, 1.0]
	fs = [0.75]
	for np, cr, f in product(nps, crs, fs):
		print "Dataset ", dataset_name, " Parameters: ", np, cr, f
		last_score, frontier = differential_evolution(model, np=np, cr=cr, f=f)
		frontier.candidates.sort(key=lambda x: x.score, reverse=True)
		print "Average: Best: Settings: ", last_score, frontier.candidates[0].score, frontier.candidates[0].decisions 






