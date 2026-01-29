import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.problem5_smoothing_simulation import smooth_once, smooth_until_stable

def almost_equal_list(a, b, tol=1e-9):
    assert len(a) == len(b)
    for x, y in zip(a, b):
        assert abs(x - y) <= tol

def test_smooth_once_known():
    vals = [0.0, 0.0, 10.0, 0.0, 0.0]
    out = smooth_once(vals)
    expected = [0.0, (0+0+10)/3, (0+10+0)/3, (10+0+0)/3, 0.0]
    almost_equal_list(out, expected)

def test_smooth_until_stable_converges_to_constant():
    vals = [0.0, 0.0, 10.0, 0.0, 0.0]
    iters, final_vals = smooth_until_stable(vals, max_iters=1000, tol=1e-10)
    assert iters > 0
    assert all(abs(final_vals[i] - final_vals[0]) <= 1e-8 for i in range(len(final_vals)))

def test_smooth_until_stable_edge_cases():
    assert smooth_until_stable([]) == (0, [])
    iters, final_vals = smooth_until_stable([5.0])
    assert iters == 0
    assert final_vals == [5.0]
