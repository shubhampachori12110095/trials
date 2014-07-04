from nose import tools

from trials.trials import *
from trials.metrics import *


eps = 10e-3


class TestExpectedPosterior:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.metric = self.trials.evaluate('expected posterior')

    def test_evaluate(self):
        tools.assert_true(len(self.metric) == 3)

    def test_sanity(self):
        tools.assert_true(self.metric['A'] > 0.99)
        tools.assert_true(np.abs(self.metric['B'] - 0.66) < eps)
        tools.assert_true(self.metric['C'] > 0.9)


class TestPosteriorCI:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.metric = self.trials.evaluate('posterior CI')
        self.mean = self.trials.evaluate('expected posterior')

    def test_evaluate(self):
        tools.assert_true(len(self.metric) == 3)

    def test_sanity(self):
        print(self.metric['A'])
        tools.assert_true(
            self.metric['A'][0] < self.metric['A'][1] < self.metric['A'][2])
        tools.assert_true(
            self.metric['B'][0] < self.metric['B'][1] < self.metric['B'][2])
        tools.assert_true(
            self.metric['C'][0] < self.metric['C'][1] < self.metric['C'][2])
        tools.assert_true(
            self.metric['A'][0] < self.mean['A'] < self.metric['A'][2])
        tools.assert_true(
            self.metric['B'][0] < self.mean['B'] < self.metric['B'][2])
        tools.assert_true(
            self.metric['C'][0] < self.mean['C'] < self.metric['C'][2])


class TestExpectedLift:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.metric = self.trials.evaluate('expected lift', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.metric) == 2)

    def test_sanity(self):
        tools.assert_true(self.metric['C'] < 0 and
                          self.metric['B'] < 0)
        tools.assert_true(self.metric['C'] >
                          self.metric['B'])

    def test_formula_matches_mcmc_result(self):
        a_samples = self.trials.variations['A'].posterior.rvs(size=10000)
        b_samples = self.trials.variations['B'].posterior.rvs(size=10000)
        mcmc_lift = np.mean((b_samples - a_samples) / a_samples)
        tools.assert_true(np.abs(mcmc_lift - self.metric['B']) < eps)


class TestLiftCI:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.metric = self.trials.evaluate('lift CI', control='A')
        self.lift = self.trials.evaluate('expected lift', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.metric) == 2)
        tools.assert_true(len(self.metric['B']) == 3)

    def test_sanity(self):
        tools.assert_true(
            self.metric['B'][0] < self.metric['B'][1] < self.metric['B'][2])
        tools.assert_true(
            self.metric['C'][0] < self.metric['C'][1] < self.metric['C'][2])
        tools.assert_true(
            self.metric['B'][0] < self.lift['B'] < self.metric['B'][2])
        tools.assert_true(
            self.metric['C'][0] < self.lift['C'] < self.metric['C'][2])


class TestDominance:

    def setup(self):
        observations = {'A': (10000, 10), 'B': (10000, 5000), 'C': (1000, 10)}

        self.jeffreys_trials = Trials(['A', 'B', 'C'])
        self.jeffreys_trials.update(observations)
        self.jeffreys_metric = self.jeffreys_trials.evaluate('dominance',
                                                             control='A')

        self.uninform_trials = Trials(['A', 'B', 'C'], alpha=1, beta=1)
        self.uninform_trials.update(observations)
        self.uninform_metric = self.uninform_trials.evaluate('dominance',
                                                             control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.jeffreys_metric) == 2)
        tools.assert_true(len(self.uninform_metric) == 2)

    def test_sanity(self):
        tools.assert_true(self.jeffreys_metric['C'] >=
            self.jeffreys_metric['B'])
        tools.assert_true(self.uninform_metric['C'] >=
            self.uninform_metric['B'])

    def test_uninformed_and_informed_results_match(self):
        print(self.jeffreys_metric['C'], self.uninform_metric['C'])
        tools.assert_true(np.abs(self.jeffreys_metric['B'] -
                                 self.uninform_metric['B']) <= eps)
        tools.assert_true(np.abs(self.jeffreys_metric['C'] -
                                 self.uninform_metric['C']) <= eps)


class TestZTestDominance:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.metric = self.trials.evaluate('z-test dominance', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.metric) == 2)

    def test_sanity(self):
        tools.assert_true(self.metric['C'] > self.metric['B'])


class TestEmpiricalLift:

    def setup(self):
        self.trials = Trials(['A', 'B', 'C'])
        self.trials.update({'A': (1000, 1), 'B': (1000, 500), 'C': (100, 10)})
        self.metric = self.trials.evaluate('empirical lift', control='A')

    def test_evaluate(self):
        tools.assert_true(len(self.metric) == 2)

    def test_sanity(self):
        tools.assert_true(self.metric['C'] < 0 and self.metric['B'] < 0)
        tools.assert_true(self.metric['C'] > self.metric['B'])
