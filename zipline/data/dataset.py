"""
dataset.py
"""
from six import (
    iteritems,
    with_metaclass,
)

from zipline.modelling.computable import Term


class Column(object):
    """
    An abstract column of data, not yet associated with a dataset.
    """

    def __init__(self, dtype):
        self.dtype = dtype

    def bind(self, parent, name):
        """
        Bind a column to a concrete dataset.
        """
        return BoundColumn(self.dtype, parent, name)


class BoundColumn(Term):
    """
    A Column of data that's been concretely bound to a particular dataset.
    """

    def __init__(self, dtype, parent, name):
        self._dtype = dtype
        self._parent = parent
        self._name = name

        super(BoundColumn, self).__init__(
            inputs=(),
            lookback=0,
            domain=self.parent.domain,
        )

    @property
    def dtype(self):
        return self._dtype

    @property
    def parent(self):
        return self._parent

    @property
    def name(self):
        return self._name

    @property
    def qualname(self):
        """
        Fully qualified of this column.
        """
        return '.'.join([self.parent.__name__, self.name])

    def __repr__(self):
        return "{qualname}::{dtype}".format(
            qualname=self.qualname,
            dtype=self.dtype.__name__,
        )


class DataSetMeta(type):
    """
    Metaclass for DataSets

    Supplies name and parent information to Column attributes.
    """

    def __new__(mcls, name, bases, dict_):

        newtype = type.__new__(mcls, name, bases, dict_)
        _columns = []
        for maybe_colname, maybe_column in iteritems(dict_):
            if isinstance(maybe_column, Column):
                bound_column = maybe_column.bind(newtype, maybe_colname)
                setattr(newtype, maybe_colname, bound_column)
                _columns.append(bound_column)

        newtype._columns = _columns
        return newtype

    @property
    def columns(self):
        return self._columns


class DataSet(with_metaclass(DataSetMeta)):
    domain = None
