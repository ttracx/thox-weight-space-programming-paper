"""Rank-1 weight edits in factor form (the Experiment 8 patch shape).

Edit:  W_new = W - alpha * outer(u, mask_cols * (u @ W))
Only the listed columns of W change. The patch ships as factors
(u, cols, alpha): a few KB for a 0.8B-class down_proj tensor, instead
of the full 7.3 MB tensor. Applying it and hashing the result is the
verification step (bit-exactness is checked in the result dtype).
"""
import numpy as np

def apply_rank1(W: np.ndarray, u: np.ndarray, cols: list[int], alpha: float) -> np.ndarray:
    W = W.copy()
    sub = W[:, cols].astype(np.float64)
    proj = u.astype(np.float64) @ sub
    sub = sub - alpha * np.outer(u.astype(np.float64), proj)
    W[:, cols] = sub.astype(W.dtype)
    return W

def factor_diff(W_base: np.ndarray, W_edit: np.ndarray):
    """Factor an observed diff: returns (rank, s1/s2, touched_count).
    Used to audit a third-party edit before trusting its factor form."""
    diff = W_edit.astype(np.float64) - W_base.astype(np.float64)
    touched = int((W_edit != W_base).sum())
    s = np.linalg.svd(diff, compute_uv=False)
    ratio = float(s[0] / s[1]) if len(s) > 1 and s[1] > 0 else float("inf")
    return {"touched_entries": touched, "sv_ratio_s1_over_s2": ratio,
            "energy_rank1_pct": float(100 * s[0] ** 2 / (s ** 2).sum())}
