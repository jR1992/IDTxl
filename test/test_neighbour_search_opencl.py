"""Provide unit tests for neighbour searches using OpenCl GPU-code.

Tests are based on unit tests by Pedro Mediano

https://github.com/pmediano/jidt/tree/master/java/source/infodynamics/
measures/continuous/kraskov/cuda
"""
import numpy as np
from idtxl.estimators_opencl import OpenCLKraskovMI, OpenCLKraskovCMI
from test_estimators_opencl import opencl_missing

opts = {'theiler_t': 0,
        'knn_k': 1,
        'gpu_id': 0,
        'debug': True}

EST_MI = OpenCLKraskovMI(opts)
EST_CMI = OpenCLKraskovCMI(opts)


@opencl_missing
def test_knn_one_dim():
    """Test kNN search in 1D."""

    pointset1 = np.expand_dims(np.array([-1, -1.2, 1, 1.1]), axis=1)
    pointset2 = np.expand_dims(np.array([99, 99, 99, 99]), axis=1)  # dummy

    # Call MI estimator
    mi, dist1, npoints_x, d_np_y = EST_MI.estimate(pointset1, pointset2,
                                                   n_chunks=1)
    assert np.isclose(dist1[0], 0.2), 'Distance 0 not correct.'
    assert np.isclose(dist1[1], 0.2), 'Distance 1 not correct.'
    assert np.isclose(dist1[2], 0.1), 'Distance 2 not correct.'
    assert np.isclose(dist1[3], 0.1), 'Distance 3 not correct.'

    # Call CMI estimator
    cmi, dist2, npoints_x, d_np_y = EST_CMI.estimate(pointset1, pointset2,
                                                     n_chunks=1)
    assert np.isclose(dist2[0], 0.2), 'Distance 0 not correct.'
    assert np.isclose(dist2[1], 0.2), 'Distance 1 not correct.'
    assert np.isclose(dist2[2], 0.1), 'Distance 2 not correct.'
    assert np.isclose(dist2[3], 0.1), 'Distance 3 not correct.'


@opencl_missing
def test_knn_two_dim():
    """Test kNN search in 2D."""
    pointset1 = np.array([
        [-1, -1],
        [0.5, 0.5],
        [1.1, 1.1],
        [2, 2]])
    pointset2 = np.ones(pointset1.shape) * 99

    # Call MI estimator
    mi, dist1, npoints_x, d_np_y = EST_MI.estimate(pointset1, pointset2,
                                                   n_chunks=1)
    assert np.isclose(dist1[0], 1.5), 'Distances 0 not correct.'
    assert np.isclose(dist1[1], 0.6), 'Distances 1 not correct.'
    assert np.isclose(dist1[2], 0.6), 'Distances 2 not correct.'
    assert np.isclose(dist1[3], 0.9), 'Distances 3 not correct.'

    # Call CMI estimator
    cmi, dist2, npoints_x, d_np_y = EST_CMI.estimate(pointset1, pointset2,
                                                     n_chunks=1)
    assert np.isclose(dist2[0], 1.5), 'Distances 0 not correct.'
    assert np.isclose(dist2[1], 0.6), 'Distances 1 not correct.'
    assert np.isclose(dist2[2], 0.6), 'Distances 2 not correct.'
    assert np.isclose(dist2[3], 0.9), 'Distances 3 not correct.'


def test_one_dim_longer_sequence():
    """Test kNN search in 1D."""

    pointset1 = np.expand_dims(
                    np.array([-1, -1.2, 1, 1.1, 10, 11, 10.5, -100, -50, 666]),
                    axis=1)
    pointset2 = np.ones(pointset1.shape) * 9999

    # Call MI estimator
    mi, dist1, npoints_x, d_np_y = EST_MI.estimate(pointset1, pointset2,
                                                   n_chunks=1)
    assert np.isclose(dist1[0], 0.2), 'Distance 0 not correct.'
    assert np.isclose(dist1[1], 0.2), 'Distance 1 not correct.'
    assert np.isclose(dist1[2], 0.1), 'Distance 2 not correct.'
    assert np.isclose(dist1[3], 0.1), 'Distance 3 not correct.'

    # Call CMI estimator
    cmi, dist2, npoints_x, d_np_y = EST_CMI.estimate(pointset1, pointset2,
                                                     n_chunks=1)
    assert np.isclose(dist2[0], 0.2), 'Distance 0 not correct.'
    assert np.isclose(dist2[1], 0.2), 'Distance 1 not correct.'
    assert np.isclose(dist2[2], 0.1), 'Distance 2 not correct.'
    assert np.isclose(dist2[3], 0.1), 'Distance 3 not correct.'


def test_two_dim_longer_sequence():
    """Test kNN with longer sequences.

    Note:
        The expected results differ from the C++ unit tests because we use the
        maximum norm when searching for neighbours.
    """

    # This is the same sequence as in the previous test case, padded with a
    # bunch of points very far away.
    pointset1 = np.expand_dims(
                np.array([[-1, 0.5, 1.1, 2, 10, 11, 10.5, -100, -50, 666],
                          [-1, 0.5, 1.1, 2, 98, -9, -200, 45.3, -53, 0.1]]),
                axis=1).T.copy()
    pointset2 = np.ones(pointset1.shape) * 9999

    # Call MI estimator
    mi, dist1, npoints_x, d_np_y = EST_MI.estimate(pointset1, pointset2,
                                                   n_chunks=1)
    assert np.isclose(dist1[0], 1.5), 'Distances 0 not correct.'
    assert np.isclose(dist1[1], 0.6), 'Distances 1 not correct.'
    assert np.isclose(dist1[2], 0.6), 'Distances 2 not correct.'
    assert np.isclose(dist1[3], 0.9), 'Distances 3 not correct.'

    # Call CMI estimator
    cmi, dist2, npoints_x, d_np_y = EST_CMI.estimate(pointset1, pointset2,
                                                     n_chunks=1)
    assert np.isclose(dist2[0], 1.5), 'Distances 0 not correct.'
    assert np.isclose(dist2[1], 0.6), 'Distances 1 not correct.'
    assert np.isclose(dist2[2], 0.6), 'Distances 2 not correct.'
    assert np.isclose(dist2[3], 0.9), 'Distances 3 not correct.'


def test_random_data():
    """Smoke kNN test with big random dataset"""
    n_points = 1000
    n_dims = 5
    pointset1 = np.random.randn(n_points, n_dims).astype('float32')
    pointset2 = pointset1

    # Call MI estimator
    mi, dist1, npoints_x, d_np_y = EST_MI.estimate(pointset1, pointset2,
                                                   n_chunks=1)
    # Call CMI estimator
    cmi, dist2, npoints_x, d_np_y = EST_CMI.estimate(pointset1, pointset2,
                                                     n_chunks=1)
    assert np.all(np.isclose(dist1, dist2)), ('High- and low-level calls '
                                              'returned different distances.')


def test_two_chunks():
    """Run knn search for two chunks."""
    n_chunks = 2
    pointset1 = np.expand_dims(np.array([5, 6, -5, -7, 50, -50, 60, -70]),
                               axis=1)
    pointset2 = np.ones(pointset1.shape) * 9999

    # Call MI estimator
    mi, dist1, npoints_x, d_np_y = EST_MI.estimate(pointset1, pointset2,
                                                   n_chunks=n_chunks)
    assert np.isclose(dist1[0], 1), 'Distance 0 not correct.'
    assert np.isclose(dist1[1], 1), 'Distance 1 not correct.'
    assert np.isclose(dist1[2], 2), 'Distance 2 not correct.'
    assert np.isclose(dist1[3], 2), 'Distance 3 not correct.'
    assert np.isclose(dist1[4], 10), 'Distance 4 not correct.'
    assert np.isclose(dist1[5], 20), 'Distance 5 not correct.'
    assert np.isclose(dist1[6], 10), 'Distance 6 not correct.'
    assert np.isclose(dist1[7], 20), 'Distance 7 not correct.'

    # Call CMI estimator
    cmi, dist2, npoints_x, d_np_y = EST_CMI.estimate(pointset1, pointset2,
                                                     n_chunks=n_chunks)
    assert np.isclose(dist2[0], 1), 'Distance 0 not correct.'
    assert np.isclose(dist2[1], 1), 'Distance 1 not correct.'
    assert np.isclose(dist2[2], 2), 'Distance 2 not correct.'
    assert np.isclose(dist2[3], 2), 'Distance 3 not correct.'
    assert np.isclose(dist2[4], 10), 'Distance 4 not correct.'
    assert np.isclose(dist2[5], 20), 'Distance 5 not correct.'
    assert np.isclose(dist2[6], 10), 'Distance 6 not correct.'
    assert np.isclose(dist2[7], 20), 'Distance 7 not correct.'


def test_three_chunks():
    """Run knn search for three chunks."""
    n_chunks = 3
    pointset1 = np.expand_dims(np.array(
            [5, 6, -5, -7, 50, -50, 60, -70, 500, -500, 600, -700]), axis=1)
    pointset2 = np.ones(pointset1.shape) * 9999

    # Call MI estimator
    mi, dist1, npoints_x, d_np_y = EST_MI.estimate(pointset1, pointset2,
                                                   n_chunks=n_chunks)
    assert np.isclose(dist1[0], 1), 'Distance 0 is not correct.'
    assert np.isclose(dist1[1], 1), 'Distance 1 is not correct.'
    assert np.isclose(dist1[2], 2), 'Distance 2 is not correct.'
    assert np.isclose(dist1[3], 2), 'Distance 3 is not correct.'
    assert np.isclose(dist1[4], 10), 'Distance 4 is not correct.'
    assert np.isclose(dist1[5], 20), 'Distance 5 is not correct.'
    assert np.isclose(dist1[6], 10), 'Distance 6 is not correct.'
    assert np.isclose(dist1[7], 20), 'Distance 7 is not correct.'
    assert np.isclose(dist1[8], 100), 'Distance 8 is not correct.'
    assert np.isclose(dist1[9], 200), 'Distance 9 is not correct.'
    assert np.isclose(dist1[10], 100), 'Distance 10 is not correct.'
    assert np.isclose(dist1[11], 200), 'Distance 11 is not correct.'

    # Call CMI estimator
    cmi, dist2, npoints_x, d_np_y = EST_CMI.estimate(pointset1, pointset2,
                                                     n_chunks=n_chunks)
    assert np.isclose(dist2[0], 1), 'Distance 0 is not correct.'
    assert np.isclose(dist2[1], 1), 'Distance 1 is not correct.'
    assert np.isclose(dist2[2], 2), 'Distance 2 is not correct.'
    assert np.isclose(dist2[3], 2), 'Distance 3 is not correct.'
    assert np.isclose(dist2[4], 10), 'Distance 4 is not correct.'
    assert np.isclose(dist2[5], 20), 'Distance 5 is not correct.'
    assert np.isclose(dist2[6], 10), 'Distance 6 is not correct.'
    assert np.isclose(dist2[7], 20), 'Distance 7 is not correct.'
    assert np.isclose(dist2[8], 100), 'Distance 8 is not correct.'
    assert np.isclose(dist2[9], 200), 'Distance 9 is not correct.'
    assert np.isclose(dist2[10], 100), 'Distance 10 is not correct.'
    assert np.isclose(dist2[11], 200), 'Distance 11 is not correct.'


def test_two_chunks_two_dim():
    """Test kNN with two chunks of 2D data in the same call."""
    n_chunks = 2
    pointset1 = np.array([[1, 1.1, -1, -1.2, 1, 1.1, -1, -1.2],
                          [1, 1, -1, -1, 1, 1, -1, -1]]).T.copy()
    pointset2 = np.ones(pointset1.shape) * 9999

    # Points:       X    Y                   y
    #               1    1                   |  o o
    #             1.1    1                   |
    #              -1   -1               ----+----x
    #            -1.2   -1                   |
    #                                  o  o  |

    # Call MI estimator
    mi, dist1, npoints_x, d_np_y = EST_MI.estimate(pointset1, pointset2,
                                                   n_chunks=n_chunks)

    assert np.isclose(dist1[0], 0.1), 'Distance 0 not correct.'
    assert np.isclose(dist1[1], 0.1), 'Distance 1 not correct.'
    assert np.isclose(dist1[2], 0.2), 'Distance 2 not correct.'
    assert np.isclose(dist1[3], 0.2), 'Distance 3 not correct.'
    assert np.isclose(dist1[4], 0.1), 'Distance 4 not correct.'
    assert np.isclose(dist1[5], 0.1), 'Distance 5 not correct.'
    assert np.isclose(dist1[6], 0.2), 'Distance 6 not correct.'
    assert np.isclose(dist1[7], 0.2), 'Distance 7 not correct.'

    # Call CMI estimator
    cmi, dist2, npoints_x, d_np_y = EST_CMI.estimate(pointset1, pointset2,
                                                     n_chunks=n_chunks)
    assert np.isclose(dist2[0], 0.1), 'Distance 0 not correct.'
    assert np.isclose(dist2[1], 0.1), 'Distance 1 not correct.'
    assert np.isclose(dist2[2], 0.2), 'Distance 2 not correct.'
    assert np.isclose(dist2[3], 0.2), 'Distance 3 not correct.'
    assert np.isclose(dist2[4], 0.1), 'Distance 4 not correct.'
    assert np.isclose(dist2[5], 0.1), 'Distance 5 not correct.'
    assert np.isclose(dist2[6], 0.2), 'Distance 6 not correct.'
    assert np.isclose(dist2[7], 0.2), 'Distance 7 not correct.'


def test_two_chunks_odd_dim():
    """Test kNN with two chunks of data with odd dimension."""
    n_chunks = 2
    pointset1 = np.array([
                    [1,  1.1,   -1, -1.2,    1,  1.1,   -1, -1.2],
                    [1,    1,   -1,   -1,    1,    1,   -1,   -1],
                    [1.02, 1.03, 1.04, 1.05, 1.02, 1.03, 1.04, 1.05]]).T.copy()
    pointset2 = np.ones(pointset1.shape) * 9999

    # Points:       X    Y      Z             y
    #               1    1   1.02            |  o o
    #             1.1    1   1.03            |
    #              -1   -1  -1.04        ----+----x
    #            -1.2   -1  -1.05            |
    #                                  o  o  |

    # Call MI estimator
    mi, dist1, npoints_x, d_np_y = EST_MI.estimate(pointset1, pointset2,
                                                   n_chunks=n_chunks)
    assert np.isclose(dist1[0], 0.1), 'Distance 0 ist not correct.'
    assert np.isclose(dist1[1], 0.1), 'Distance 1 ist not correct.'
    assert np.isclose(dist1[2], 0.2), 'Distance 2 ist not correct.'
    assert np.isclose(dist1[3], 0.2), 'Distance 3 ist not correct.'
    assert np.isclose(dist1[4], 0.1), 'Distance 4 ist not correct.'
    assert np.isclose(dist1[5], 0.1), 'Distance 5 ist not correct.'
    assert np.isclose(dist1[6], 0.2), 'Distance 6 ist not correct.'
    assert np.isclose(dist1[7], 0.2), 'Distance 7 ist not correct.'

    # Call CMI estimator
    cmi, dist2, npoints_x, d_np_y = EST_CMI.estimate(pointset1, pointset2,
                                                     n_chunks=n_chunks)
    assert np.isclose(dist2[0], 0.1), 'Distance 0 ist not correct.'
    assert np.isclose(dist2[1], 0.1), 'Distance 1 ist not correct.'
    assert np.isclose(dist2[2], 0.2), 'Distance 2 ist not correct.'
    assert np.isclose(dist2[3], 0.2), 'Distance 3 ist not correct.'
    assert np.isclose(dist2[4], 0.1), 'Distance 4 ist not correct.'
    assert np.isclose(dist2[5], 0.1), 'Distance 5 ist not correct.'
    assert np.isclose(dist2[6], 0.2), 'Distance 6 ist not correct.'
    assert np.isclose(dist2[7], 0.2), 'Distance 7 ist not correct.'


if __name__ == '__main__':
    test_knn_one_dim()
    test_knn_two_dim()
    test_two_chunks_odd_dim()
    test_two_chunks_two_dim()
    test_two_chunks()
    test_three_chunks()
    test_random_data()
    test_one_dim_longer_sequence
    test_two_dim_longer_sequence()