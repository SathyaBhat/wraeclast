# Motra percentage-load recommendations

## Required evidence order

1. Exact lift confirmed by user or a clearly named scheduled workout.
2. Canonical exercise ID from `motra_search_exercises`.
3. Full-enough `motra_exercise_history` plus all-time/relevant-range `motra_stats(max weight)`.
4. Current tested 1RM/training max if known. A historical maximum in Motra is not necessarily current.

## Worked pattern: back squat

When a historical 100 kg single is logged but recent high-rep work is lower (for example, 65 kg × 10 and 55 kg × 14), distinguish:

- **If 100 kg is the active programme training max:** 72–76% = 72–76 kg before rounding.
- **If it is an old tested max:** present this as a conditional result, compare it with recent training, and recommend confirming the coach's current training max rather than quietly treating the old PR as current.

For ordinary 2.5 kg plate loading, explain rounding explicitly. A 72–76 kg window may support 72.5 kg and 75 kg; 77.5 kg exceeds the ceiling. Do not invent an in-range ramp if the available increments do not permit it.

## Estimation

When estimating 1RM from a submaximal set, compute with a tool. For Epley:

```
e1RM = weight * (1 + reps / 30)
```

Call it an estimated 1RM and do not represent it as a measured max.

## Communication standard

Lead with the exact proposed load(s) and their assumption. Then include the smallest caveat necessary: target lift, base max freshness, rounding, and a technical-quality stop rule. Avoid generic warm-up detail unless requested.