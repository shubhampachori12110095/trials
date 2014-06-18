trials
======
Tiny Bayesian A/B testing library

[![Build Status](https://travis-ci.org/bogdan-kulynych/trials.svg?branch=master)](https://travis-ci.org/bogdan-kulynych/trials)

### Install:

```
pip install -r requirements.txt
```

pip might not install all the system packages needed for scipy. To install them on Debian:

```
sudo apt-get install libatlas-dev libatlas-base-dev liblapack-dev gfortran
```

Running tests:

```
nosetests
```

### Usage

```python
from trials import Trials

# Start an A/B test with Bernoulli (binary) observations
test = Trials(['A', 'B', 'C'])

# Observe successes and failures
test.update({
    'A': (50, 10), # 50 successes, 10 failures, total 60
    'B': (75, 15), # 75 successes, 15 failures, total 90
    'C': (20, 15)  # 20 successes, 15 failures, total 35
})

# Evaluate some metrics, like
## Dominance probabilities P(X > A)
dominance = test.evaluate('dominance', control='A')
## Expected lifts E[(X-A)/A]
lift = test.evaluate('expected lift', control='A')
## Lifts' 95%-credible intervals
interval = test.evaluate('lift CI', control='A', ci=95)

# Print results
for variation in ['B', 'C']:
    print('Variation {name}:'.format(name=variation))
    print('* E[lift] = {value:.2%}'.format(value=lift[variation]))
    print('* P({lower:.2%} < lift < {upper:.2%}) = 95%' \
        .format(lower=interval[variation][0], upper=interval[variation][2]))
    print('* P({name} > {control}) = {value:.2%}' \
        .format(name=variation, control='A', value=dominance[variation]))
```

Output:
```
Variation B:
* E[lift] = 0.22%
* P(-13.47% < lift < 17.31%) = 95%
* P(B > A) = 49.27%
Variation C:
* E[lift] = -31.22%
* P(-51.33% < lift < -9.21%) = 95%
* P(C > A) = 0.25%
```

There's 50% chance that variation **B** is better than **A** (*dominance*). Most likely it is better by about 0.2% (*expected lift*), but there's 95% chance that real lift is anywhere betwen -13% to 17% (*lift CI*). You need more data to know if **B** is better or worse for sure.

There's 100% - 0.25% = 99.75% chance that variation **C** is worse than **A**. Most likely it is worse by about 31%, and there's 95% chance that real lift falls betwen -51% to -9%. The data was sufficient to tell that this variation is almost certainly inferior to both **A** and **B**. However, if this 99.75% chance still doesn't convince you, you need more data.

### Theory
Explanation of mathematics behind and usage guide are coming soon as a blog post.

Meanwhile, see the [notebook](http://nbviewer.ipython.org/github/bogdan-kulynych/trials/blob/master/examples/benchmark.ipynb) for comparison of Bayesian lift (blue) and empirical lift (green) errors in a theoretical benchmark with equal sample sizes. Bayesian approach is a little better at predicting the lift, but no miracles here. Bayesian p-values and frequentist (z-test) p-values yield almost identical results.
