"""
Tests for the FFC API.
"""
from unittest import TestCase

from numpy import (
    float32,
    uint32,
    uint8,
)

from zipline.data.dataset import (
    Column,
    DataSet,
)
# from zipline.modelling.classifier import Classifier
from zipline.modelling.engine import build_dependency_graph
from zipline.modelling.factor import Factor
# from zipline.modelling.filter import Filter


class SomeDataSet(DataSet):

    foo = Column(float32)
    bar = Column(uint32)
    buzz = Column(uint8)


class ShortFooBar(Factor):
    lookback = 5
    inputs = [SomeDataSet.foo, SomeDataSet.bar]

    def compute(self, foo, bar):
        return foo + bar


class LongFooBar(ShortFooBar):
    lookback = 10


class DependencyResolutionTestCase(TestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_single_factor(self):
        graph = build_dependency_graph([], [], [ShortFooBar.default()])
