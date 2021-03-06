"""Miscellaneous useful tools.

In this module are implemented some common function to use in combination
with the rest of the package.
"""
# This code is written by
#       Salvatore Masecchia <salvatore.masecchia@unige.it>
#       Annalisa Barla <annalisa.barla@unige.it>
#       Federico Tomasi <federico.tomasi@dibris.unige.it>
# Copyright (C) 2017 SlipGURU -
# Statistical Learning and Image Processing Genoa University Research Group
# Via Dodecaneso, 35 - 16146 Genova, ITALY.
#
# This file is part of L1L2Py.
#
# L1L2Py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# L1L2Py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with L1L2Py. If not, see <http://www.gnu.org/licenses/>.
import numpy as np
from six.moves import xrange


__all__ = ('geometric_range', 'standardize', 'center',
           'classification_error', 'balanced_classification_error',
           'regression_error', 'kfold_splits', 'stratified_kfold_splits')


def geometric_range(min_value, max_value, number):
    r"""Geometric range of values between min_value and max_value.

    Sequence of ``number`` values from ``min_value``
    to ``max_value`` generated by a geometric sequence.

    Parameters
    ----------
    min_value : float
    max_value : float
    number : int

    Returns
    -------
    range : (``number``, ) ndarray

    Raises
    ------
    ZeroDivisionError
        If ``min_value`` is ``0.0`` or ``number`` is ``1``

    Examples
    --------
    >>> l1l2py.tools.geometric_range(min_value=0.0, max_value=10.0, number=4)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: float division
    >>> l1l2py.tools.geometric_range(min_value=0.1, max_value=10.0, number=4)
    array([ 0.1       ,  0.46415888,  2.15443469, 10.        ])
    >>> l1l2py.tools.geometric_range(min_value=0.1, max_value=10.0, number=2)
    array([  0.1,  10. ])
    >>> l1l2py.tools.geometric_range(min_value=0.1, max_value=10.0, number=1)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: float division
    >>> l1l2py.tools.geometric_range(min_value=0.1, max_value=10.0, number=0)
    array([], dtype=float64)

    """
    ratio = (max_value / float(min_value)) ** (1. / (number - 1))
    return min_value * (ratio ** np.arange(number))


# Normalization ---------------------------------------------------------------
def center(matrix, optional_matrix=None, return_mean=False):
    r"""Center columns of a matrix setting each column to zero mean.

    The function returns the centered ``matrix`` given as input.
    Optionally centers an ``optional_matrix`` with respect to the mean value evaluated
    for ``matrix``.

    .. note::

        A one dimensional matrix is considered as a column vector.

    Parameters
    ----------
    matrix : (N,) or (N, P) ndarray
        Input matrix whose columns are to be centered.
    optional_matrix : (N,) or (N, P) ndarray, optional (default is `None`)
        Optional matrix whose columns are to be centered
        using mean of ``matrix``.
        It must have the same number of columns as ``matrix``.
    return_mean : bool, optional (default is `False`)
        If `True` returns mean of ``matrix``.

    Returns
    -------
    matrix_centered : (N,) or (N, P) ndarray
        Centered ``matrix``.
    optional_matrix_centered : (N,) or (N, P) ndarray, optional
        Centered ``optional_matrix`` with respect to ``matrix``
    mean : float or (P,) ndarray, optional
        Mean of ``matrix`` columns.

    Examples
    --------
    >>> X = numpy.array([[1, 2, 3], [4, 5, 6]])
    >>> l1l2py.tools.center(X)
    array([[-1.5, -1.5, -1.5],
           [ 1.5,  1.5,  1.5]])
    >>> l1l2py.tools.center(X, return_mean=True)
    (array([[-1.5, -1.5, -1.5],
           [ 1.5,  1.5,  1.5]]), array([ 2.5,  3.5,  4.5]))
    >>> x = numpy.array([[1, 2, 3]])             # 2-dimensional matrix
    >>> l1l2py.tools.center(x, return_mean=True)
    (array([[ 0.,  0.,  0.]]), array([ 1.,  2.,  3.]))
    >>> x = numpy.array([1, 2, 3])               # 1-dimensional matrix
    >>> l1l2py.tools.center(x, return_mean=True) # centered as a (3, 1) matrix
    (array([-1.,  0.,  1.]), 2.0)
    >>> l1l2py.tools.center(X, X[:,:2])
    Traceback (most recent call last):
        ...
    ValueError: shape mismatch: objects cannot be broadcast to a single shape

    """
    mean = matrix.mean(axis=0)

    # Simple case
    if optional_matrix is None and return_mean is False:
        return matrix - mean

    if optional_matrix is None:  # than return_mean is True
        return (matrix - mean, mean)

    if return_mean is False:  # otherwise
        return (matrix - mean, optional_matrix - mean)

    # Full case
    return (matrix - mean, optional_matrix - mean, mean)


def standardize(matrix, optional_matrix=None, return_factors=False):
    r"""Standardize columns of a matrix setting each column with zero mean and
    unitary standard deviation.

    The function returns the standardized ``matrix`` given as input.
    Optionally it standardizes an ``optional_matrix`` with respect to the
    mean and standard deviation evaluatted for ``matrix``.

    .. note::

        A one dimensional matrix is considered as a column vector.

    Parameters
    ----------
    matrix : (N,) or (N, P) ndarray
        Input matrix whose columns are to be standardized
        to mean `0` and standard deviation `1`.
    optional_matrix : (N,) or (N, P) ndarray, optional (default is `None`)
        Optional matrix whose columns are to be standardized
        using mean and standard deviation of ``matrix``.
        It must have same number of columns as ``matrix``.
    return_factors : bool, optional (default is `False`)
        If `True`, returns mean and standard deviation of ``matrix``.

    Returns
    -------
    matrix_standardized : (N,) or (N, P) ndarray
        Standardized ``matrix``.
    optional_matrix_standardized : (N,) or (N, P) ndarray, optional
        Standardized ``optional_matrix`` with respect to ``matrix``
    mean : float or (P,) ndarray, optional
        Mean of ``matrix`` columns.
    std : float or (P,) ndarray, optional
        Standard deviation of ``matrix`` columns.

    Raises
    ------
    ValueError
        If ``matrix`` has only one row.

    Examples
    --------
    >>> X = numpy.array([[1, 2, 3], [4, 5, 6]])
    >>> l1l2py.tools.standardize(X)
    array([[-0.70710678, -0.70710678, -0.70710678],
           [ 0.70710678,  0.70710678,  0.70710678]])
    >>> l1l2py.tools.standardize(X, return_factors=True)
    (array([[-0.70710678, -0.70710678, -0.70710678],
           [ 0.70710678,  0.70710678,  0.70710678]]), array([ 2.5,  3.5,  4.5]), array([ 2.12132034,  2.12132034,  2.12132034]))
    >>> x = numpy.array([[1, 2, 3]])                     # 1 row matrix
    >>> l1l2py.tools.standardize(x, return_factors=True)
    Traceback (most recent call last):
        ...
    ValueError: 'matrix' must have more than one row
    >>> x = numpy.array([1, 2, 3])                       # 1-dimensional matrix
    >>> l1l2py.tools.standardize(x, return_factors=True)  # standardized as a (3, 1) matrix
    (array([-1.,  0.,  1.]), 2.0, 1.0)
    >>> l1l2py.tools.center(X, X[:,:2])
    Traceback (most recent call last):
        ...
    ValueError: shape mismatch: objects cannot be broadcast to a single shape
    """
    if matrix.ndim == 2 and matrix.shape[0] == 1:
        raise ValueError("'matrix' must have more than one row")

    mean = matrix.mean(axis=0)
    std = matrix.std(axis=0, ddof=1)

    # Simple case
    if optional_matrix is None and return_factors is False:
        return (matrix - mean)/std

    if optional_matrix is None:  # than return_factors is True
        return (matrix - mean)/std, mean, std

    if return_factors is False:  # otherwise
        return (matrix - mean) / std, (optional_matrix - mean) / std

    # Full case
    return (matrix - mean) / std, (optional_matrix - mean) / std, mean, std


# Error functions -------------------------------------------------------------
def classification_error(labels, predictions):
    r"""Evaluate the binary classification error.

    The classification error is based on the sign of the ``predictions`` values,
    with respect to the sign of the data ``labels``.

    The function assumes that ``labels`` contains positive values for one
    class and negative values for the other one.

    .. warning::

        For efficiency reasons, the values in ``labels`` are not checked by the function.

    Parameters
    ----------
    labels : array_like, shape (N,)
        Classification labels (usually contains only 1s and -1s).
    predictions : array_like, shape (N,)
        Classification labels predicted.

    Returns
    -------
    error : float
        Classification error evaluated.

    Examples
    --------
    >>> l1l2py.tools.classification_error(labels=[1, 1, 1], predictions=[1, 1, 1])
    0.0
    >>> l1l2py.tools.classification_error(labels=[1, 1, 1], predictions=[1, 1, -1])
    0.33333333333333331
    >>> l1l2py.tools.classification_error(labels=[1, 1, 1], predictions=[1, -1, -1])
    0.66666666666666663
    >>> l1l2py.tools.classification_error(labels=[1, 1, 1], predictions=[-1, -1, -1])
    1.0
    >>> l1l2py.tools.classification_error(labels=[1, 1, 1], predictions=[10, -2, -3])
    0.66666666666666663

    """
    labels = np.asarray(labels).ravel()
    predictions = np.asarray(predictions).ravel()

    difference = (np.sign(labels) != np.sign(predictions))
    return len(*difference.nonzero()) / float(len(labels))


def balanced_classification_error(labels, predictions, error_weights=None):
    r"""Returns the binary classification error balanced
    across the size of classes.

    This function returns a balanced classification error.
    With the default value for ``error_weights``, the function
    assigns greater weight to the errors belonging to the smaller class.

    Parameters
    ----------
    labels : array_like, shape (N,)
        Classification labels (usually contains only 1s and -1s).
    predictions : array_like, shape (N,)
        Classification labels predicted.
    error_weights : array_line, shape (N,), optional (default is None)
        Classification error weigths. If `None` the default weights are calculated
        removing from each value in ``labels`` their mean value.

    Returns
    -------
    error : float
        Classification error calculated.

    Examples
    --------
    >>> l1l2py.tools.balanced_classification_error(labels=[1, 1, 1], predictions=[-1, -1, -1])
    0.0
    >>> l1l2py.tools.balanced_classification_error(labels=[-1, 1, 1], predictions=[-1, 1, 1])
    0.0
    >>> l1l2py.tools.balanced_classification_error(labels=[-1, 1, 1], predictions=[1, -1, -1])
    0.88888888888888895
    >>> l1l2py.tools.balanced_classification_error(labels=[-1, 1, 1], predictions=[1, 1, 1])
    0.44444444444444442
    >>> l1l2py.tools.balanced_classification_error(labels=[-1, 1, 1], predictions=[-1, 1, -1])
    0.22222222222222224
    >>> l1l2py.tools.balanced_classification_error(labels=[-1, 1, 1], predictions=[-1, 1, -1],
    ...                                            error_weights=[1, 1, 1])
    0.33333333333333331

    """
    labels = np.asarray(labels).ravel()
    predictions = np.asarray(predictions).ravel()

    if error_weights is None:
        error_weights = np.abs(center(labels))

    errors = (np.sign(labels) != np.sign(predictions)) * error_weights
    return errors.sum() / float(len(labels))


def regression_error(labels, predictions):
    r"""Returns regression error.

    The regression error is the sum of the quadratic differences between the
    ``labels`` values and the ``predictions`` values, over the number of
    samples.

    Parameters
    ----------
    labels : array_like, shape (N,)
        Regression labels.
    predictions : array_like, shape (N,)
        Regression labels predicted.

    Returns
    -------
    error : float
        Regression error calculated.

    """
    labels = np.asarray(labels).ravel()
    predictions = np.asarray(predictions).ravel()

    difference = labels - predictions
    return np.dot(difference.T, difference).squeeze() / float(len(labels))


# KCV tools -------------------------------------------------------------------
def kfold_splits(labels, k, rseed=0):
    r"""k-fold cross validation splits.

    Given a list of labels, the function produces a list of ``k`` splits.
    Each split is a pair of tuples containing the indexes of the training set
    and the indexes of the test set.

    Parameters
    ----------
    labels : array_like, shape (N,)
        Data labels.
    k : int, greater than `0`
        Number of splits.
    rseed : int, optional (default is `0`)
        Random seed.

    Returns
    -------
    splits : list of ``k`` tuples
        Each tuple contains two lists with the training set and test set
        indexes.

    Raises
    ------
    ValueError
        If ``k`` is less than 2 or greater than `N`.

    Examples
    --------
    >>> labels = range(10)
    >>> l1l2py.tools.kfold_splits(labels, 2)
    [([7, 1, 3, 6, 8], [9, 4, 0, 5, 2]), ([9, 4, 0, 5, 2], [7, 1, 3, 6, 8])]
    >>> l1l2py.tools.kfold_splits(labels, 1)
    Traceback (most recent call last):
        ...
    ValueError: 'k' must be greater than one and smaller or equal than the number of samples

    """
    if not (2 <= k <= len(labels)):
        raise ValueError("'k' must be greater than one and smaller or equal "
                         "than the number of samples")

    import random
    random.seed(rseed)
    indexes = list(range(len(labels)))
    random.shuffle(indexes)
    random.seed()  # restores random generation from a random seed

    return _splits(indexes, k)


def stratified_kfold_splits(labels, k, rseed=0):
    r"""Sstratified k-fold cross validation splits.

    This function is a variation of ``kfold_splits``, which
    returns stratified splits. The divisions are made by preserving
    the percentage of samples for each class, assuming that the problem
    is binary.

    Parameters
    ----------
    labels : array_like, shape (N,)
        Data labels (usually contains only 1s and -1s).
    k : int, greater than `0`
        Number of splits.
    rseed : int, optional (default is `0`)
        Random seed.

    Returns
    -------
    splits : list of ``k`` tuples
        Each tuple contains two lists with the training set and test set
        indexes.

    Raises
    ------
    ValueError
        If `labels` contains more than two classes labels.
    ValueError
        If ``k`` is less than 2 or greater than number of positive or negative
        samples in `labels`.

    Examples
    --------
    >>> labels = range(10)
    >>> l1l2py.tools.stratified_kfold_splits(labels, 2)
    Traceback (most recent call last):
        ...
    ValueError: 'labels' must contains only two class labels
    >>> labels = [1, 1, 1, 1, 1, 1, -1, -1, -1, -1]
    >>> l1l2py.tools.stratified_kfold_splits(labels, 2)
    [([8, 9, 5, 2, 1], [7, 6, 3, 0, 4]), ([7, 6, 3, 0, 4], [8, 9, 5, 2, 1])]
    >>> l1l2py.tools.stratified_kfold_splits(labels, 1)
    Traceback (most recent call last):
        ...
    ValueError: 'k' must be greater than one and smaller or equal than number of positive and negative samples

    """
    classes = np.unique(labels)
    if classes.size != 2:
        raise ValueError("'labels' must contains only two class labels")

    n_indexes = (np.where(labels == classes[0])[0]).tolist()
    p_indexes = (np.where(labels == classes[1])[0]).tolist()

    if not (2 <= k <= min(len(n_indexes), len(p_indexes))):
        raise ValueError("'k' must be greater than oen and smaller or equal "
                         "than number of positive and negative samples")

    import random
    random.seed(rseed)
    random.shuffle(n_indexes)
    n_splits = _splits(n_indexes, k)

    random.shuffle(p_indexes)
    p_splits = _splits(p_indexes, k)
    random.seed()  # restores random generation from a random seed

    splits = list()
    for ns, ps in zip(n_splits, p_splits):
        train = ns[0] + ps[0]
        test = ns[1] + ps[1]
        splits.append((train, test))

    return splits


def _splits(indexes, k):
    r"""Split the 'indexes' list in input in k disjoint chunks.
    """
    return [(indexes[:start] + indexes[end:], indexes[start:end])
            for start, end in _split_dimensions(len(indexes), k)]


def _split_dimensions(num_items, num_splits):
    r"""Generator wich gives the pairs of indexes to split 'num_items' data
       in 'num_splits' chunks.
    """
    start = 0
    remaining_items = float(num_items)

    for remaining_splits in xrange(num_splits, 0, -1):
        split_size = int(round(remaining_items / remaining_splits))
        end = start + split_size

        yield start, end

        start = end
        remaining_items -= split_size
