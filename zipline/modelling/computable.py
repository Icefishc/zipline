"""
Base class for Filters, Factors and Classifiers
"""
from functools32 import lru_cache


class CyclicDependency(Exception):
    # TODO: Move this somewhere else.
    pass


class Term(object):
    """
    A term.
    """
    inputs = ()
    lookback = 0
    domain = None

    def __init__(self, inputs=None, lookback=None, domain=None):
        self.inputs = inputs or type(self).inputs
        self.lookback = lookback or type(self).lookback
        self.domain = domain or type(self).domain

    @classmethod
    @lru_cache(maxsize=None)
    def default(cls):
        return cls()

    def update_dependency_graph(self,
                                dependencies,
                                cycle_context,
                                lookback):

        if self in cycle_context:
            raise CyclicDependency(self)

        cycle_context.add(self)

        # If we're already in the graph because we're a dependency of a
        # processed node, ensure that we load enough lookback data for our
        # dependencies.
        try:
            existing = dependencies.node[self]
            existing['lookback'] = max(lookback, existing['lookback'])
        except KeyError:
            dependencies.add_node(self, lookback=lookback)

        for term in self.inputs:
            term.update_dependency_graph(
                dependencies,
                cycle_context,
                lookback + self.lookback
            )
            dependencies.add_edge(term, self)

        cycle_context.remove(self)

    def compute(self, *data):
        raise NotImplementedError()
