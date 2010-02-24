r"""Various useful tools.

The :mod:`tools` module defines four type of functions:

* Range generators
    - :func:`linear_range`
    - :func:`geometric_range`
* Data Normalization 
    - :func:`center`
    - :func:`standardize`  
* Error calculation 
    - :func:`classification_error` 
    - :func:`balanced_classification_error`
    - :func:`regression_error`
* Cross Validation utilities
    - :func:`kfold_splits`  
    - :func:`stratified_kfold_splits` 

"""

import numpy as np

__all__ = ['linear_range', 'geometric_range',
           'standardize', 'center',
           'classification_error', 'balanced_classification_error',
           'regression_error',
           'kfold_splits', 'stratified_kfold_splits']

# Ranges functions ------------------------------------------------------------
def linear_range(min_value, max_value, number):
    r"""Returns a linear range of values.

    Returns ``number`` evenly spaced values from 
    ``min_value`` to ``max_value``.

    Parameters
    ----------
    min_value : float
    max_value : float
    number : int
    
    Returns
    -------
    range : ndarray

    See Also
    --------
    geometric_range
    numpy.linspace

    Examples
    --------
    >>> biolearning.tools.linear_range(0.0, 10.0, 4)
    array([  0.        ,   3.33333333,   6.66666667,  10.        ])
    >>> biolearning.tools.linear_range(0.0, 10.0, 2)
    array([  0.,  10.])
    >>> biolearning.tools.linear_range(0.0, 10.0, 1)
    array([ 0.])
    >>> biolearning.tools.linear_range(0.0, 10.0, 0)
    array([], dtype=float64)

    """
    return np.linspace(min_value, max_value, number)

def geometric_range(min_value, max_value, number):
    r"""Returns a geometric range of values.

    Returns ``number`` values from ``min_value`` 
    to ``max_value`` generated by a geometric sequence (see ``Notes``).

    Parameters
    ----------
    min_value : float
    max_value : float
    number : int

    Returns
    -------
    range : ndarray

    Raises
    ------
    ZeroDivisionError
        If ``min_value`` is ``0.0`` or ``number`` is ``1``

    See Also
    --------
    linear_range

    Notes
    -----
    The geometric sequence of :math:`n` elements 
    between :math:`a` and :math:`b` is 

    .. math:: 

        a,\ ar^1,\ ar^2,\ \dots,\ ar^{n-1}

    where the ratio :math:`r` is

    .. math:: 

        r = \left(\frac{b}{a}\right)^{\frac{1}{n-1}}

    Examples
    --------
    >>> biolearning.tools.geometric_range(0.0, 10.0, 4)
    Traceback (most recent call last):
        ...  
    ZeroDivisionError: float division
    >>> biolearning.tools.geometric_range(0.1, 10.0, 4)
    array([ 0.1       ,  0.46415888,  2.15443469, 10.        ])
    >>> biolearning.tools.geometric_range(0.1, 10.0, 2)
    array([  0.1,  10. ])
    >>> biolearning.tools.geometric_range(0.1, 10.0, 1)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: float division
    >>> biolearning.tools.geometric_range(0.1, 10.0, 0)
    array([], dtype=float64)

    """
    ratio = (max_value/float(min_value))**(1.0/(number-1))
    return min_value * (ratio ** np.arange(number))

# Normalization ---------------------------------------------------------------
def standardize(matrix, optional_matrix=None, return_factors=False):
    r"""Standardize columns of a matrix.

    Returns the standardized ``matrix`` given in input.
    Optionally standardizes an ``optional_matrix`` respect 
    mean and standard deviation calculated on ``matrix``.

    Parameters
    ----------
    matrix : (N,) or (N, D) ndarray
        Input matrix whose columns are to be standardize 
        to mean=0 and standard deviation=1. 
    optional_matrix : (N,) or (N, D) ndarray, optional (default is `None`)
        Optional matrix whose columns are to be standardize
        using mean and standard deviation of ``matrix``.
        It must have same columns number of ``matrix``.
    return_factors : bool, optional (default is `False`)
        If `True` returns used mean and standard deviation.

    Returns
    -------
    matrix_standardized : (N,) or (N, D) ndarray
        Standardized ``matrix``.
        If ``matrix`` is an (N,) ndarray then returns its standardization.
    optional_matrix_standardized : (N,) or (N, D) ndarray, optional
        Standardized ``optional_matrix`` respect to ``matrix``
    mean : float or (D,) ndarray, optional
        Mean of ``matrix`` columns.
    std : float or (D,) ndarray, optional
        Standard deviation of ``matrix`` columns.

    See Also
    --------
    center

    Examples
    --------
    >>> X = numpy.array([[1, 2, 3], [4, 5, 6]])
    >>> biolearning.tools.standardize(X)
    array([[-0.70710678, -0.70710678, -0.70710678],
           [ 0.70710678,  0.70710678,  0.70710678]])
    >>> biolearning.tools.standardize(X, return_factors=True)
    (array([[-0.70710678, -0.70710678, -0.70710678],
           [ 0.70710678,  0.70710678,  0.70710678]]), array([ 2.5,  3.5,  4.5]), array([ 2.12132034,  2.12132034,  2.12132034]))
    >>> x = numpy.array([1, 2, 3])
    >>> biolearning.tools.standardize(x)
    array([-1.,  0.,  1.])

    """
    mean = matrix.mean(axis=0)
    std = matrix.std(axis=0, ddof=1)

    # Simple case
    if optional_matrix is None and return_factors is False:
        return (matrix - mean)/std
                
    if optional_matrix is None: # than return_factors is True
        return (matrix - mean)/std, mean, std
        
    if return_factors is False: # ... with p not None
        return (matrix - mean)/std, (optional_matrix - mean)/std
        
    # Full case
    return (matrix - mean)/std, (optional_matrix - mean)/std, mean, std
    
def center(matrix, optional_matrix=None, return_mean=False):
    r"""Center columns of a matrix.

    Returns the centered ``matrix`` given in input.
    Optionally centers an ``optional_matrix`` respect 
    mean calculated on ``matrix``.

    Parameters
    ----------
    matrix : (N,) or (N, D) ndarray
        Input matrix whose columns are to be center.
    optional_matrix : (N,) or (N, D) ndarray, optional (default is `None`)
        Optional matrix whose columns are to be center
        using mean of ``matrix``.
        It must have same columns number of ``matrix``.
    return_mean : bool, optional (default is `False`)
        If `True` returns used mean.

    Returns
    -------
    matrix_centered : (N,) or (N, D) ndarray
        Centered ``matrix``.
        If ``matrix`` is an (N,) ndarray then returns its centering.
    optional_matrix_centered : (N,) or (N, D) ndarray, optional
        Centered ``optional_matrix`` respect to ``matrix``
    mean : float or (D,) ndarray, optional
        Mean of ``matrix`` columns.

    See Also
    --------
    standardize

    Examples
    --------
    >>> X = numpy.array([[1, 2, 3], [4, 5, 6]])
    >>> biolearning.tools.center(X)
    array([[-1.5, -1.5, -1.5],
           [ 1.5,  1.5,  1.5]])
    >>> biolearning.tools.center(X, return_mean=True)
    (array([[-1.5, -1.5, -1.5],
           [ 1.5,  1.5,  1.5]]), array([ 2.5,  3.5,  4.5]))
    >>> x = numpy.array([1, 2, 3])
    >>> biolearning.tools.center(x)
    array([-1.,  0.,  1.])

    """
    mean = matrix.mean(axis=0)
    
    # Simple case
    if optional_matrix is None and return_mean is False:
        return matrix - mean
    
    if optional_matrix is None: # than return_mean is True
        return (matrix - mean, mean)
    
    if return_mean is False: # ...with p not None
        return (matrix - mean, optional_matrix - mean)
    
    # Full case
    return (matrix - mean, optional_matrix - mean, mean)
    
# Error functions -------------------------------------------------------------
def classification_error(labels, predicted):
    r"""Returns classification error.

    The classification error is based on the sign of the ``predicted`` values
    respect the sign of the data ``labels``.
    The functions assumes that ``labels`` contains positive number for one
    class and negative numbers for the other one (see ``Notes``).

    Parameters
    ----------
    labels : array_like, shape (N,)
        Classification labels (usually contains only 1s and -1s).
    predicted : array_like, shape (N,)
        Classification labels predicted.

    Returns
    -------
    error : float
        Classification error calculated.
        
    See Also
    --------
    balanced_classification_error
    regression_error    

    Notes
    ------
    The classification error is calculated using this formula
    
    .. math::

        error = \frac{\sum_{i=1}^N{f(l_i, p_i)}}{N} \qquad 
                l_i \in\ labels,\, p_i \in\ predicted

    where :math:`f(l_i, p_i)=1` if :math:`sign(l_i) \neq sign(p_i)`;
    otherwise :math:`f(l_i, p_i)=0`

    Examples
    --------
    >>> biolearning.tools.classification_error([1, 1, 1], [1, 1, 1])
    0.0
    >>> biolearning.tools.classification_error([1, 1, 1], [1, 1, -1])
    0.33333333333333331
    >>> biolearning.tools.classification_error([1, 1, 1], [1, -1, -1])
    0.66666666666666663
    >>> biolearning.tools.classification_error([1, 1, 1], [-1, -1, -1])
    1.0
    >>> biolearning.tools.classification_error([1, 1, 1], [10, -2, -3])
    0.66666666666666663
    
    """
    difference = (np.sign(labels) != np.sign(predicted))
    return difference[difference].size / float(len(labels))
    
def balanced_classification_error(labels, predicted):
    r"""Returns classification error balanced across the size of classes.
    
    This function is a variation of :func:`classification_error` which
    returns a biased classification error, weighing more the errors
    belonging to the smaller class.
    
    Parameters
    ----------
    labels : array_like, shape (N,)
        Classification labels (usually contains only 1s and -1s).
    predicted : array_like, shape (N,)
        Classification labels predicted.

    Returns
    -------
    error : float
        Classification error calculated.
        
    See Also
    --------
    classification_error
    regression_error    
    
    Notes
    ------
    The balanced classification error is calculated using this formula
    
    .. math::

        error = \frac{\sum_{i=1}^N{f(l_i, p_i)} |l_i - mean(labels)|}
                      {N}
                \qquad 
                l_i \in\ labels,\, p_i \in\ predicted

    where :math:`f(l_i, p_i)=1` if :math:`sign(l_i) \neq sign(p_i)`;
    otherwise :math:`f(l_i, p_i)=0`
    
    .. warning::

        If ``labels`` contains single class labels, the functions returns
        always `0.0` because :math:`l_i - \overline{labels} = 0`.
    
    Examples
    --------
    >>> biolearning.tools.balanced_classification_error([1, 1, 1], [-1, -1, -1])
    0.0
    >>> biolearning.tools.balanced_classification_error([-1, 1, 1], [-1, 1, 1])
    0.0
    >>> biolearning.tools.balanced_classification_error([-1, 1, 1], [1, -1, -1])
    0.88888888888888895
    >>> biolearning.tools.balanced_classification_error([-1, 1, 1], [1, 1, 1])
    0.44444444444444442
    >>> biolearning.tools.balanced_classification_error([-1, 1, 1], [-1, 1, -1])
    0.22222222222222224
    
    """
    balance_factors = np.abs(center(np.asarray(labels)))
   
    errors = (np.sign(labels) != np.sign(predicted)) * balance_factors
    return errors.sum() / float(len(labels))
    
def regression_error(labels, predicted):
    r"""Returns regression.
    
    The regression is the sum of the quadratic difference between the '`labels``
    value and the ``predicted`` values, over the number of
    samples (see ``Notes``).
    
    Parameters
    ----------
    labels : array_like, shape (N,)
        Regression labels.
    predicted : array_like, shape (N,)
        Regression labels predicted.

    Returns
    -------
    error : float
        Regression error calculated.
        
    See Also
    --------
    classification_error
    balanced_classification_error
    
    Notes
    -----
    The classification error is calculated using this formula
    
    .. math::
        
        error = \frac{\sum_{i=1}^N{|l_i - p_i|^2}} {N}
            \qquad 
            l_i \in\ labels,\, p_i \in\ predicted
            
    """  
    difference = np.asarray(labels) - np.asarray(predicted)
    return np.dot(difference.T, difference) / float(len(labels))
    
# KCV tools -------------------------------------------------------------------
def kfold_splits(labels, k, rseed=0):
    r"""Returns k-fold cross validation splits.
    
    Given the list of labels, the function produces a list of ``k`` splits.
    Each split is a pair of tuples containing the indexes of the training set
    and the indexes of the testing set.

    Parameters
    ----------
    labels : array_like, shape (N,)
        Data labels (for this function is important only its length).
    k : int, greater than `0`
        Number of splits.
    rseed : int, optional (default is `0`)
        Random seed.
    
    Returns
    -------
    splits : list of ``k`` tuples
        Each tuple contains two lists with the training set and testing set
        indexes.
    
    See Also
    --------
    stratified_kfold_splits
    
    Examples
    --------
    >>> labels = range(10)
    >>> biolearning.tools.kfold_splits(labels, 2)
    [([7, 1, 3, 6, 8], [9, 4, 0, 5, 2]), ([9, 4, 0, 5, 2], [7, 1, 3, 6, 8])]
    >>> biolearning.tools.kfold_splits(labels, 1)
    [([], [9, 4, 0, 5, 2, 7, 1, 3, 6, 8])]
    >>> biolearning.tools.kfold_splits(labels, 0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: float division
    
    """
    import mlpy
    return mlpy.kfold(len(labels), k, rseed)

def stratified_kfold_splits(labels, k, rseed=0):
    r"""Returns k-fold cross validation stratified splits.
    
    This function is a variation of :func:`kfold_splits` which
    returns stratified splits. The divisions are made by holding
    the percentage of samples for each class, supposing to have a
    two class problem.

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
        Each tuple contains two lists with the training set and testing set
        indexes.
    
    See Also
    --------
    kfold_splits
    
    Examples
    --------
    >>> labels = range(10)
    >>> biolearning.tools.stratified_kfold_splits(labels, 2)
    Traceback (most recent call last):
        ...
    ValueError: pncl() works only for two-classes
    >>> labels = [1, 1, 1, 1, 1, 1, -1, -1, -1, -1]
    >>> biolearning.tools.stratified_kfold_splits(labels, 2)
    [([1, 3, 5, 8, 7], [2, 4, 0, 9, 6]), ([2, 4, 0, 9, 6], [1, 3, 5, 8, 7])]
    >>> biolearning.tools.stratified_kfold_splits(labels, 1)
    [([], [2, 4, 0, 1, 3, 5, 9, 6, 8, 7])]
    >>> biolearning.tools.stratified_kfold_splits(labels, 0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: float division
    
    """
    import mlpy
    return mlpy.kfoldS(labels, k, rseed)
