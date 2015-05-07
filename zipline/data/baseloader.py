"""
Base class for new-style data loaders.
"""
from abc import (
    ABCMeta,
    abstractmethod,
)


from six import with_metaclass


class DataLoader(with_metaclass(ABCMeta)):

    def load_dataset(self, dataset, assets, dates):
        return self.load_columns(dataset.columns, assets, dates)

    @abstractmethod
    def load_columns(self, columns, assets, dates):
        raise NotImplementedError
