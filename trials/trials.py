"""Trials class."""

from collections import OrderedDict

from .variations import vtypes as default_vtypes
from .metrics import metrics as default_metrics


class Trials(object):

    """Main A/B test class."""

    class UnsupportedVariationType(Exception):
        pass

    class UnsupportedMetric(Exception):
        pass

    def __init__(self, variation_labels, vtype='bernoulli', *args, **kwargs):
        """Create an A/B test assuming vtype variations."""
        if isinstance(vtype, str):
            if vtype not in default_vtypes:
                raise Trials.UnsupportedVariationType(vtype)
            vtype = default_vtypes[vtype]

        self.vtype = vtype
        self.variations = OrderedDict([(label, vtype(*args, **kwargs))
                                      for label in variation_labels])

    def update(self, feed):
        """Update test state with observations."""
        for label, observations in feed.items():
            self.variations[label].update(*observations)

    def evaluate(self, metric, *args, **kwargs):
        """Evaluate a metric."""
        result = None
        if isinstance(metric, str):
            if metric not in self.vtype.metrics:
                raise Trials.UnsupportedMetric(metric)
            func = default_metrics[metric]
            result = func(self.variations, *args, **kwargs)
        else:
            result = metric(self.variations, *args, **kwargs)
        return result
