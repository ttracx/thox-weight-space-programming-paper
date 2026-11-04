"""Weight-reading tools: the readers and head scores from the THOX
recreation experiments (E1 and E4 of the whitepaper).

read_effective_per_class: the only one of four tested readers that beat
chance on the E1 task suite (100% vs 33% chance); the three simpler
readers are kept here as negative controls.
"""
import numpy as np

def _conc(profile):
    return float(profile.std() / (profile.mean() + 1e-12))

def _axis_scores(A):
    return {"col": _conc(A.sum(axis=0)), "row": _conc(A.sum(axis=1)),
            "diag": max(_conc(np.array([A.diagonal(k).sum() for k in range(-7, 8)])),
                        _conc(np.array([np.fliplr(A).diagonal(k).sum() for k in range(-7, 8)])))}

def read_effective_per_class(W1: np.ndarray, W2: np.ndarray) -> str:
    """Task-axis read from the composed per-class input->logit maps.
    Pure weight algebra: E = W2^T W1^T, no forward passes."""
    E = W2.T @ W1.T
    votes = {"col": 0.0, "row": 0.0, "diag": 0.0}
    for c in range(E.shape[0]):
        sc = _axis_scores(np.abs(E[c]).reshape(8, 8))
        win = max(sc, key=sc.get)
        votes[win] += sc[win] - sorted(sc.values())[1]
    return max(votes, key=votes.get)
