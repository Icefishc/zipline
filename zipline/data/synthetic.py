"""
Synthetic data loaders for testing.
"""
from abc import abstractmethod
from collections import OrderedDict

from numpy import (
    arange,
    empty
)

from zipline.data.baseloader import DataLoader


class SyntheticDataLoader(DataLoader):
    """
    DataLoader subclass that builds synthetic data based only on the shape
    of the desired output.

    Subclasses should implement the following methods:

    make_column(dtype: np.dtype, nrows: int, ncols: int, idx: int) -> ndarray
    """

    def load_columns(self, columns, assets, dates):
        """
        Load each column with self.make_column.
        """
        nrows = len(assets)
        ncols = len(dates)
        return OrderedDict(
            [
                (col.name, self.make_column(col.dtype, nrows, ncols, idx))
                for idx, col in enumerate(columns)
            ]
        )

    @abstractmethod
    def make_column(self, dtype, nrows, ncols, idx):
        """
        Returns an ndarray of dtype dtype and shape (nrows, ncols).

        idx is incremented and passed for each unique field loaded.
        """
        pass


class ConstantLoader(SyntheticDataLoader):
    """
    SyntheticDataLoader that returns a constant value for each sid/column.
    """

    def make_column(self, dtype, nrows, ncols, idx):
        buf = empty(
            (nrows, ncols),
            dtype=dtype,
        )
        buf[:] = idx
        return buf


class ARangeLoader(SyntheticDataLoader):
    """
    A DataLoader that just returns np.aranges for each sid and column.
    """

    def make_column(self, dtype, nrows, ncols, idx):
        buf = empty(
            (nrows, ncols),
            dtype=dtype,
        )
        buf[:] = arange(1, ncols + 1) * idx
        return buf
