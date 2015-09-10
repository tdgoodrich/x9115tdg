## Solution

### Output
<img src="sa.PNG" style="width: 600px;"/>

### Some Implementation Notes

1. The neighbor solution is computed by choosing (uniformly at random) another real number within (euclidean distance _radius_ (a parameter to this algorithm implementation). By default I set _radius=500_
2. I went ahead and seeded the random, in case anyone wants to reproduce. 

### Thoughts/Questions/Places I might have gone wrong

1. I did not use `e > emax` as a condition in the while loop. If this is a minimization problem, why would we stop if we're epsilon away from the sampleMaximum? It's likely that our initial solution is less than the sampleMaximum, in fact. Perhaps I'm misunderstanding something.
2. In the pseudocode it says to do `ELSE IF P(e, en, k/kmax) > rand()`. However, later on in the document it says to do `random() > P`. Which way should the inequality go? When I do it the first way I get a lot of jumps to worse solutions, when I do the second way I get absolutely no jumps to worse solutions (but get a much much better final solution).
3. More generally, if I do `random() > P` then the output tells me that all I'm doing is gradient descent (see the output above). Is this bad? Perhaps I defined the neighborhood function poorly, such that most suggested "bad" neighbors are actually too terrible to even consider.