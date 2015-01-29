import pickle

from hessianbackprop import HessianBackprop
import numpy as np


def test_xor():
    bp = HessianBackprop([2, 5, 1], debug=True, use_GPU=False)
    inputs = np.asarray([[0.1, 0.1], [0.1, 0.9], [0.9, 0.1], [0.9, 0.9]],
                        dtype=np.float32)
    targets = np.asarray([[0.1], [0.9], [0.9], [0.1]], dtype=np.float32)

    bp.run_batches(inputs, targets, CG_iter=4, max_epochs=40,
                   plotting=True)

    # using gradient descent (for comparison)
#     for i in range(10000):
#         if i % 100 == 0:
#             print "iteration", i
#         bp.gradient_descent(inputs, targets, l_rate=20)

    for i, t in zip(inputs, targets):
        print "input", i
        print "target", t
        print "output", bp.forward(i, bp.W)[-1]


def test_mnist():
    # download dataset at http://deeplearning.net/data/mnist/mnist.pkl.gz
    with open("mnist.pkl", "rb") as f:
        train, _, test = pickle.load(f)

    bp = HessianBackprop([28 * 28, 1000, 500, 250, 30, 10], use_GPU=True,
                         debug=False)

    inputs = train[0]
    targets = np.ones((inputs.shape[0], 10), dtype=np.float32) * 0.1
    targets[np.arange(inputs.shape[0]), train[1]] = 0.9

    tmp = np.ones((test[0].shape[0], 10), dtype=np.float32) * 0.1
    tmp[np.arange(test[0].shape[0]), test[1]] = 0.9
    test = (test[0], tmp)

    bp.run_batches(inputs, targets, CG_iter=100, batch_size=7500,
                   test=test, max_epochs=1000,
                   load_weights=None, plotting=True)


def test_profile():
    np.random.seed(0)
    import cProfile
    import pstats

    cProfile.run("test_mnist()", "profilestats")
    p = pstats.Stats("profilestats")
    p.strip_dirs().sort_stats('time').print_stats(20)


test_xor()
# test_mnist()
# test_profile()