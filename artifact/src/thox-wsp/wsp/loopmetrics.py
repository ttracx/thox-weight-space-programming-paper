"""Loop / repetition metrics for generation baselines (whitepaper E4b).

A generation 'loops' under the adiant211-style test when at least 90%
of 300 consecutive 8-word n-grams have appeared before. We also record
cap hits (generation reached the token limit without an EOS/close).
"""
def repetition_score(words: list[str], n: int = 8, window: int = 300) -> float:
    if len(words) < n + 10:
        return 0.0
    seen = set(); repeated = 0; total = 0
    grams = [tuple(words[i:i + n]) for i in range(len(words) - n + 1)]
    for i, g in enumerate(grams):
        if i >= window:
            break
        total += 1
        if g in seen: repeated += 1
        seen.add(g)
    return repeated / max(total, 1)

def is_loop(text: str) -> bool:
    return repetition_score(text.split()) >= 0.9

def summarize(records: list[dict]) -> dict:
    """records: {text, hit_cap} per generation."""
    n = len(records)
    return {"n": n,
            "cap_hit_rate": sum(r["hit_cap"] for r in records) / max(n, 1),
            "loop_rate": sum(is_loop(r["text"]) for r in records) / max(n, 1)}
