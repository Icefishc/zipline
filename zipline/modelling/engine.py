"""
Compute Engine for FFC API
"""
from itertools import chain
from networkx import DiGraph


def _compute_term(term, workspace, loader, assets, dates):

    workspace.add_term(term)
    filters, classifiers, factors = term.dependencies()

    _compute(filters, classifiers, factors, workspace, loader, assets, dates)
    term.compute()


def _compute(filters,
             classifiers,
             factors,
             workspace,
             loader,
             assets,
             dates):
    """
    Compute an FFC Matrix from iterables of filters, factors, and classifiers.

    Depth-first compute filters, then classifiers, then factors.
    """
    for filter_ in filters:
        _compute_term(filter_, workspace, loader, assets, dates)

    for classifier in classifiers:
        _compute_term(classifier, workspace, loader, assets, dates)

    for factor in factors:
        _compute_term(factor, workspace, loader, assets, dates)

    return workspace


def build_dependency_graph(filters, classifiers, factors):

    dependencies = DiGraph()
    cycle_context = set()
    for term in chain(filters, classifiers, factors):
        term.update_dependency_graph(
            dependencies,
            cycle_context,
            lookback=0,
        )

    assert not cycle_context
    return dependencies


def compute_all(filters,
                classifiers,
                factors,
                workspace,
                loader,
                assets,
                dates):
    """
    """
    build_dependency_graph(filters, classifiers, factors)
