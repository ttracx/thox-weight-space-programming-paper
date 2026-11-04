# Iteration 1 results (honest record, superseded by v2 where noted)
- E1: trained nets 100% task accuracy, but the global-marginal reader scored
  33.3% = chance. Diagnosis: summing |W1| over all hidden units washes out
  the task signature. Reader v2 uses per-unit axis voting.
- E2: written net catch 100%, target MAE ~0 (exact on the reachable range);
  the 0.5 triangle-wave error occurs only outside the reachable input
  range. Trained-oracle baseline also catches 100% but with nonzero MAE
  and 1200 gradient steps on 4096 oracle examples. v2 adds a hard regime
  (slower paddle, tighter window) to separate exact from approximate.
- E3: first surgical edit FAILED (0% after, 11.2% of weights touched).
  Diagnosis: override units were driven by mixed layer-1 features and the
  incoming columns were zeroed wholesale. Edit v2 builds dedicated
  layer-1 velocity detectors and sparse high-gain paths (~2-3% of weights).
