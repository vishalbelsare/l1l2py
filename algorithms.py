r"""Internal algorithms implementations.

The :mod:`algorithms` module defines core numerical optimizazion algorithms:

* :func:`ridge_regression`
* :func:`elastic_net`
* :func:`elastic_net_regpath`

"""

import numpy as np

__all__ = ['ridge_regression', 'elastic_net', 'elastic_net_regpath']

def ridge_regression(data, labels, mu=0.0):
    r"""Regularized Least Squares.

    Finds the RLS model with ``mu`` parameter associated with its
    :math:`\ell_2` norm (see `Notes`).

    Parameters
    ----------
    data : (N, D) ndarray
        Data matrix.
    labels : (N,)  or (N, 1) ndarray
        Labels vector.
    mu : float, optional (default is `0.0`)
        :math:`\ell_2` norm penalty.

    Returns
    -------
    beta : (D,) or (D, 1) ndarray
        RLS model.

    Notes
    -----
    RLS minimizes the following objective function:

    .. math::

        \frac{1}{N} \| Y - X\beta \|_2^2 + \mu \|\beta\|_2^2

    finding the optimal model :math:`\beta^*`, where

    =============== ===============
    :math:`X`       ``data``
    --------------- ---------------
    :math:`Y`       ``labels``
    --------------- ---------------
    :math:`\mu`     ``mu``
    --------------- ---------------
    :math:`\beta^*` ``beta``
    =============== ===============

    Using ``mu`` = `0.0` the algorithm performs Ordinary Least Squares (OLS).

    Examples
    --------
    >>> X = numpy.array([[0.1, 1.1, 0.3], [0.2, 1.2, 1.6], [0.3, 1.3, -0.6]])
    >>> beta = numpy.array([0.1, 0.1, 0.0])
    >>> y = numpy.dot(X, beta)
    >>> biolearning.algorithms.ridge_regression(X, y)
    array([  1.00000000e-01,   1.00000000e-01,   6.62515290e-17])

    """
    n, d = data.shape

    if n < d:
        tmp = np.dot(data, data.T)
        if mu:
            tmp += mu*n*np.eye(n)
        tmp = np.linalg.pinv(tmp)

        return np.dot(np.dot(data.T, tmp), labels)
    else:
        tmp = np.dot(data.T, data)
        if mu:
            tmp += mu*n*np.eye(d)
        tmp = np.linalg.pinv(tmp)

        return np.dot(tmp, np.dot(data.T, labels))

def elastic_net_regpath(data, labels, mu, tau_range, beta=None, kmax=1e5,
                        step_size=None):
    r"""Elastic Net regularization path.

    Find the EN regularization path for each value in ``tau_range`` and
    fixed value of ``mu``.

    Parameters
    ----------
    data : (N, D) ndarray
        Data matrix.
    labels : (N,) or (N, 1) ndarray
        Labels vector.
    mu : float
        :math:`\ell_2` norm penalty.
    tau_range : array_like of float
        :math:`\ell_1` norm penalties.
    beta : (D,) or (D, 1) ndarray, optional (default is `None`)
        Starting value of the iterations (see :func:`elastic_net` `Notes`).
        If is `None` iterations starts from the OLS solution.
    kmax : int, optional (default is :math:`10^5`)
        Maximum number of iterations.
    step_size : float, optional (default is `None`)
        Iterations step size.
        If is `None` the algorithm use default value
        (see :func:`elastic_net` `Notes`).

    Returns
    -------
    beta_path : list of (D,) or (D, 1) ndarray
        EN models. The number of models can differ the number of `tau` values.
        The functions returns only the model with at least one nonzero value.
        For very high value of tau a model can have all `0s`.

    See Also
    --------
    elastic_net

    """
    from collections import deque
    n, d = data.shape

    if mu == 0.0:
        beta_ls = ridge_regression(data, labels)
    if beta is None:
        beta = np.zeros((d, 1))

    out = deque()
    nonzero = 0
    for tau in reversed(tau_range):
        if mu == 0.0 and nonzero >= n: # lasso saturation
            beta_next = beta_ls
        else:
            beta_next = elastic_net(data, labels, mu, tau, beta,
                                    kmax, step_size)

        if len(beta_next.nonzero()[0]) > 0:
            out.appendleft(beta_next)

        beta = beta_next

    return out

def elastic_net(data, labels, mu, tau, beta=None, kmax=1e5, step_size=None,
                returns_iterations=False):
    r"""Elastic Net regularization.

    Finds the EN model with ``mu`` parameter associated with its
    :math:`\ell_2` norm and ``tau`` parameter associated with its
    :math:`\ell_1` norm (see `Notes`).

    Parameters
    ----------
    data : (N, D) ndarray
        Data matrix.
    labels : (N,) or (N, 1) ndarray
        Labels vector.
    mu : float
        :math:`\ell_2` norm penalty.
    tau : float
        :math:`\ell_1` norm penalty.
    beta : (D,) or (D, 1) ndarray, optional (default is `None`)
        Starting value of the iterations (see `Notes`).
        If is `None` iterations starts from the OLS solution.
    kmax : int, optional (default is :math:`10^5`)
        Maximum number of iterations.
    step_size : float, optional (default is `None`)
        Iterations step size.
        If is `None` the algorithm use default value (see `Notes`).
    returns_iterations : bool, optional (default is `False`)
        If True, return the number of iterations performed.
        The algorithm has a predefined minimum number of iterations
        equal to `100`.

    Returns
    -------
    beta : (D,) or (D, 1) ndarray
        EN model.
    k : int, optional
        Number of iterations performed.

    Notes
    -----
    EN minimizes the following objective function:

    .. math::

        \frac{1}{N} \| Y - X\beta \|_2^2 + \mu \|\beta\|_2^2 + \tau \|\beta\|_1

    finding the optimal model :math:`\beta^*`, where

    =============== ===============
    :math:`X`       ``data``
    --------------- ---------------
    :math:`Y`       ``labels``
    --------------- ---------------
    :math:`\mu`     ``mu``
    --------------- ---------------
    :math:`\beta^*` ``beta``
    =============== ===============

    Using ``mu`` = `0.0` the algorithm performs LASSO.

    The computation is iterative, each step updates the value of beta until
    the convergence is reached:

    .. math::

        \beta^{(k+1)} = \frac{1}{1 + \frac{N\mu}{C}}
                        \mathbf{S}_{\frac{N\tau}{C}} (
                            \beta^k + \frac{1}{C}[X^TY - X^TX\beta^k]
                        )


    where we have to choice :math:`\frac{1}{C} < \frac{2}{\|X^T X\|}`.

    The default value is close to the maximum step size:

    .. math::

        \frac{1}{C} = \frac{2}{\|X^T X\| + 10^{-5}} < \frac{2}{\|X^T X\|}

    See Also
    --------
    elastic_net_regpath

    Examples
    --------
    >>> X = numpy.array([[0.1, 1.1, 0.3], [0.2, 1.2, 1.6], [0.3, 1.3, -0.6]])
    >>> beta = numpy.array([0.1, 0.1, 0.0])
    >>> y = numpy.dot(X, beta)
    >>> biolearning.algorithms.elastic_net(X, y, 0.0, 0.0)
    array([  1.00000000e-01,   1.00000000e-01,   6.24500451e-17])
    >>> biolearning.algorithms.elastic_net(X, y, 0.1, 0.1)
    array([ 0.        ,  0.07715517,  0.        ])

    """
    n = data.shape[0]

    if step_size is None:
        step_size = _step_size(data)    # 1/C
    mu_s = (n * mu) * step_size         # (n mu)/C
    tau_s = (n * tau) * step_size       # (n tau)/C

    # Initializations
    XT = data.T * step_size             # X^T / C
    XTY = np.dot(XT, labels)            # (X^T Y) / C

    if beta is None:
        beta = ridge_regression(data, labels)

    k, kmin, tol = 0, 100, 0.01
    th, difference = -np.inf, np.inf
    while k < kmin or ((difference > th).any() and k < kmax):
        k += 1

        value = beta +  XTY - np.dot(XT, np.dot(data, beta))
        beta_next = _soft_thresholding(value, tau_s) / (1.0 + mu_s)

        difference = np.abs(beta_next - beta)
        th = np.abs(beta) * (tol / k)
        beta = beta_next

    if returns_iterations:
        return beta_next, k
    else:
        return beta

def _step_size(matrix):
    n, d = matrix.shape

    if d > n:
        tmp = np.dot(matrix, matrix.T)
    else:
        tmp = np.dot(matrix.T, matrix)
    max_eig = np.linalg.eigvalsh(tmp).max()

    return 2.0/(max_eig + 1e-5)

def _soft_thresholding(x, th):
    """ TODO: Add docstring """
    out = x - (np.sign(x) * (th / 2.0))
    out[np.abs(x) < (th / 2.0)] = 0.0
    return out
