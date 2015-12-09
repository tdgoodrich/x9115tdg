
from abcd import Abcd
import arff
import sys
import os
import time
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn import cross_validation

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

def printStatistics(k, count, actual, predicted):
	print "\n%d-Fold Cross Validation Fold #%d" % (k, count)
	abcd = Abcd(db="ant", rx="LogReg")
	for act, pred in zip(actual, predicted):
		abcd.tell(actual=act, predict=pred)
	abcd.header()
	abcd.ask() 

def main():
	for filename in sys.argv[1:]:
		train, target = readArff(filename)

		# Set up the learner we want
		samples = 15
		start = time.time()
		fscore = 0
		for x in xrange(samples):
			n_clusters = 10
			learner = MiniBatchKMeans(n_clusters=n_clusters, max_no_improvement=10, reassignment_ratio=0.02)
			
			# Form the clusters
			cluster_assignments = learner.fit_predict(train)
			
			# Get the bug prediction
			counts = [[0,0] for _ in xrange(n_clusters)]
			for point, assignment in enumerate(cluster_assignments):
	 			counts[assignment][int(target[point])] += 1
			cluster_bug_prediction = [0 if x[0] > x[1] else 1 for x in counts]
			bug_prediction = [str(cluster_bug_prediction[assignment]) for assignment in cluster_assignments]
			tp, tn, fp, fn = 0,0,0,0
			for actual, predicted in zip(target, bug_prediction):
				if actual == "1" and predicted == "1":
					tp += 1
				elif actual == "0" and predicted == "1":
					fp += 1
				elif actual == "1" and predicted == "0":
					fn += 1
			fscore += 2.0*tp/(2.0*tp+fp+fn)
		print "Time taken: ", time.time()-start
		print "F-Score: ", fscore / samples


if __name__ == "__main__":
	main()