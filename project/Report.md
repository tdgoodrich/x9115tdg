# Final Project

Timothy Goodrich  
tdgoodri@ncsu  
Submitted December 8, 2015

## Section 1: Introduction
### 1.1. Motivation
As software projects become larger and larger, testing them becomes incresingly intractable without rigorous automated tools. One such tool is a *defect predictor*. Phrased as a supervised machine learning problem: Given a set of points, composed of a software project's features, predict whether the module represented by this point contains a bug or not. However, solving this problem is not good enough; we also need a very *fast* (and potentially parallelizable) solution.  

One method of developing a fast solution is to develop a slower learner and then find an invariant property in the data structure that can be used as a proxy for recognizing the existance of bugs. Structural graph theory provides a plethora of such invariants, including some that can be computed in linear time, leading to the need for a slower, more accurate learner with strong graph theory structure. Developing such a learner is the goal of this project. 


### 1.2. Objectives
This work is driven by the following objectives:
* Research Goal 1: Understand which clustering methods accurately describe the CK metrics.
* Research Goal 2: Identify better parameters for a clusterer by using an optimizer (e.g. Differential Evolution). 
* Research Goal 3: Having identified reasonable clustering parameters, conjecture what underlying graph structure we can exploit. 

### 1.3. Data
For this project, I selected 11 data sets from the PROMISE repository's CK collection, listed in the table below:

|  **Name** | **Version** |  
|---|---|
| ant | 1.7 |  
| camel | 1.6 |  
| ivy | 2.0 |  
| jedit | 4.3 |  
| log4j | 1.2 |  
| lucene | 2.4 |  
| poi | 3.0 |  
| synapse | 1.2 |  
| velocity | 1.6 |  
| xalan | 2.7 |  
| xerces | 1.4 |  

The CK metrics originated from Chidamber and Kemerer (CK) in 1994 as an object-oriented version of the CH metrics. The metrics come from three distinct areas: the *identification* of classes, the *semantics* of classes, and the *relationship* between classes. More details (such as exact features) can be read at the dataset's [tutorial page](http://openscience.us/repo/defect/ck/tut.html) or in the [original publication itself](http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=295895&url=http%3A%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D295895).


### 1.4. Algorithms

Per our research goals, we need a clustering algorithm and an optimizer:
* The first choice for clusterer was [DBSCAN](http://scikit-learn.org/stable/modules/clustering.html#dbscan), based on Scikit-Learn's [clusterer comparison page](http://scikit-learn.org/stable/modules/clustering.html). DBSCAN identifies clusters by initially selecting a set of *core samples* in dense areas. Additional points are then added to the clusters by counting how many paths the point has to the core samples, providing the algorithm's two parameters (a distance threshold for a point to be considered nearby to a core sample, and number of nearby core samples required for a point to join a cluster). One pro of this approach is that the clusters need not be convex (as opposed to K-Means), allowing more fluid clusters. Unfortunately, when applied to the CK data, I could not achieve a comfortable medium between 1-2 clusters and 200+ clusters. This is bad because the former makes vast false positive and false negative errors, and the latter one is useless because only 1-3 points belong to a cluster. Instead, we want closer to 10-50 clusters.
* Given that we needed to manually impose a number of clusters, the next natural choice was [KMeans](http://scikit-learn.org/stable/modules/clustering.html#k-means). More specifically, Scikit-Learn provides a faster version named [MiniBatchKMeans](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html#sklearn.cluster.MiniBatchKMeans), which I used so that more time could be spent optimizing the parameters' values. (Note that the selection of these parameters is detiled in Section 2.2 below). KMeans works by randomly placing K centroids into the data and repeating the following two steps:
    1. Compute the distance from each point to every centroid and assign each point to the closest centroid.
    2. Given a cluster (a centroid and its assigned points), relocate the centroid to be in the center of this cluster.

  In theory, these centroids converge to an optimal clustering with exactly K clusters. However, choosing exactly what K should be is itself an optimization task, but one that we relegate to the optimizer. 
  
* For an optimizer I used [Diferential Evolution (DE)](https://en.wikipedia.org/wiki/Differential_evolution) due to its simplicity, speed, and reletively good performance. DE works by creating an initial population of *np* number of points, which are then improved upon through *n* generations. Each generation consists of doing the following per candidate solution in the population:
    1. Copy the old candidate's info to a new candidate. 
    2. Select three other candidates X, Y, and Z.
    2. For each decision, at probability *cr*, set the new candidate's decision equal to *X[decision] + f * (Y[decision] - Z[decision)*. (Note that *f* is another parameter). At probability *(1-cr)* keep the old decision. 
    3. Evaluate the new candidate and compare to the old one. If the new one is better, use it to replace the old one.   
    
  One note is that the average solution quality is monotonely increasing; we never add a worse solution to our frontier. 

## Section 2: Methodology and Implementation Details

### 2.1. Data Parsing
For simplicity of reading, I converted the input file to an ARFF format (where feature data types are provided). To further reduce the problem complexity I also changed the output column (the bug number) from numerical (an integer representing the error code) to boolean (whether there was a bug or not). 

### 2.2. Clusterer Parameters
Consulting the [MiniBatchKMeans](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html#sklearn.cluster.MiniBatchKMeans) Scikit-Learn page we see that MiniBatchKMeans only has 3 tunable parameters:  
    1. `n_clusters`: The number of clusters. For optimization I fixed the range at [5, 50].  
    2. `max_no_improvement`: The number of steps to continue running while no improvements are found. For optimization I fixed the range at [0, 20].  
    3. `reassignment_ratio`: The ratio of cluster points needed before the centroid is reassigned (1.0 is the standard KMeans). For optimization I fixed the range at [0, 1].  

### 2.3. Differential Evolution Parameters
As noted in Section 1.4, DE has many parameters. I fixed them as follows:
1. I always run DE/random/1, meaning that I choose a random candidate for X, and 1 pair of random candidates Y/Z. 
2. *n* (the number of iterations) was set to 100, but was never reached because of the next parameter.
3. *epsilon* was set to 0.001, such that the algorithm would quit if we did not get an improvement of at least 0.001 in the current generation. 
4. *np* (population size) was set to 30 as recommended by [Storn 1997](http://link.springer.com/article/10.1023%2FA%3A1008202821328#page-1) (10 times the number of decisions). 
5. *f* (the amount of crossover) is fixed at 0.75, between the commended range of 0.5 to 1.0.
6. *cr* (the probability of crossover) is ranged over {0.3, 0.7, 1.0}.

### 2.4. Clusterer as Predictor

Once we have a clustering on a dataset, we still need to obtain a bug detection prediction. We do this as follows:
1. For each cluster, we count the number of points with bugs and without bugs. 
2. We then choose the majority output as the whole cluster's prediction.
3. Each point's prediction is then the prediction for the cluster it was assigned to.

### 2.5. Output Metrics
For evaluating the clusterer, we will use the F1 score (F-measure with *beta = 1*). The F-measure gives us the harmonic mean of precision and recall, which we want to include given that a program may have very few bugsp; a very high true negative value could make accuracy look better than it really was. 

For tables, we want to report three different F1 scores:
1. The average from the initial DE population (equivalent to random sampling).
2. The average from the final DE population.
3. The highest score from the final DE population.

## Section 3: Results


### 3.1. F1 Scores

**Table 1: Average Initial F1 scores**   
| Optimizer: | **ant** | **camel** | **ivy** | **jedit** | **log4j** | **lucene** | **poi** | **synapse** | **velocity** | **xalan** | **xerces** |  
|---|---|---|---|---|---|---|---|---|---|---|---|  
| DE(f=0.3) | 56% | 12% | 37% | 14% | 96% | 74% | 82% | 62% | 58% | 99% | 86% |
| DE(f=0.7) | 57% | 13% | 38% | 14% | 96% | 75% | 83% | 64% | 59% | 99% | 87% |
| DE(f=1.0) | 57% | 12% | 37% | 15% | 96% | 75% | 83% | 64% | 59% | 99% | 87% |

We see in Table 1 a wide range of prediction qualities: log4j and xalan start extremely well, lucene, poi and xerces start very strong, and camel and jedit start extremely weak. 

**Table 1: Average Final F1 scores**   
| Optimizer: | **ant** | **camel** | **ivy** | **jedit** | **log4j** | **lucene** | **poi** | **synapse** | **velocity** | **xalan** | **xerces** |  
|---|---|---|---|---|---|---|---|---|---|---|---|  
| DE(f=0.3) | 59% | 22% | 55% | 32% | 96% | 77% | 85% | 70% | 68% | 99% | 89% |
| DE(f=0.7) | 59% | 22% | 55% | 32% | 96% | 78% | 85% | 69% | 68% | 99% | 89% |
| DE(f=1.0) | 59% | 22% | 55% | 32% | 96% | 78% | 85% | 70% | 67% | 99% | 89% |

After converging, DE improves most every prediction, doubling the ones with very bad starts (camel and jedit), and not making any improvements on the ones with very good starts (log4j and xalan).

**Table 1: Best Final F1 scores**   
| Optimizer: | **ant** | **camel** | **ivy** | **jedit** | **log4j** | **lucene** | **poi** | **synapse** | **velocity** | **xalan** | **xerces** |  
|---|---|---|---|---|---|---|---|---|---|---|---|  
| DE(f=0.3) | 60% | 23% | 56% | 36% | 96% | 78% | 85% | 71% | 68% | 99% | 90% |
| DE(f=0.7) | 60% | 23% | 57% | 37% | 96% | 79% | 85% | 70% | 68% | 99% | 90% |
| DE(f=1.0) | 60% | 23% | 56% | 36% | 96% | 79% | 85% | 71% | 68% | 99% | 90% |

Looking at the best single scores, we see that most predictions go up by a percentage and not much more (excepting jedit). This suggests that the whole frontier has converged and not just a few high points. This result seems to suggest that some ideal parameters were found all over the board -- a common structure that could be utilized by something like graph theory. 

## Section 4: Conclusion

### 4.1. Summary
In summary, we find that
1. KMeans seems to provide a reasonable bug detector.
2. Differential Evolution was able to further tune the clusterer, with very extreme improvements on the low end (camel and jedit). 
3. The population as a whole seemed to converge in terms of F1 scores, suggesting that there is some common underlying structure that could be recognized, hopefully with a faster heuristic. 

### 4.2. Threats to Validity
Some threats to validity include:
1. Lack of baseline comparison. What do baseline results from other learners look like for this data? Perhaps a 85% F1 score on poi is a bad result compared to something like logistic regression. By exploring more varied predictors, we could have a better idea of the context of these results.
2. Overtraining. Nowhere did we do cross-validation, suggesting that we might have overtrained somehow. It is rather unclear how to introduce cross-validation, however, because the clusterer works more like an unsupervised learner than a supervised one; we are required to take an extra step to turn the clusters into bug predictions.
3. Exact structure unclear. We noted that the whole DE population seemed to converge in F1 scores, but what about in parameter selection? This study did not include a rigorous way of comparing the final parameters and probing out any concrete structure. 

### 4.3. Future Work

As mentioned in the previous section, the next step must be to establish more context for these results. How well does a logistic regression model perform? What about a predictor that was also tuned with DE? We cannot really understand if this is a good predictor without some benchmarks.  

Secondly, we need a rigorous manner of evaluating what common structure we ended up with. Does it matter if some parameters are different? How different? Perhaps a12 could be used here to note if the differences are meaningful or not. 




