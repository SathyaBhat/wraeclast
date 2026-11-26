---
name: fitness-training
description: Query Motra workout history, produce weekly training snapshots, and give grounded progression/load recommendations for programmed sessions.
---

# Fitness training with Motra

Use this skill for workout recaps, readiness-adjacent training context, exercise progression, and translating percentage prescriptions into practical loads.

## Core workflow

1. **Identify the exact lift first.** Never infer it from adjacent recent workouts or a generic class schedule. If the user supplies an image/text without a lift name, ask which lift the prescription applies to; first check the calendar only if it may identify a scheduled activity.
2. **Resolve the canonical Motra exercise ID** with `motra_search_exercises` before requesting exercise history.
3. Pull both:
   - `motra_exercise_history` with sufficient scope to capture recent working sets and past heavy exposures;
   - `motra_stats` max weight for that exact exercise.
4. Treat a logged max as historical evidence, not automatically as the current percentage base. Compare it with recent rep work and flag a stale max where appropriate.
5. For a percentage prescription, calculate each load with a tool. State the assumed 1RM/training max, rounding rule, plate increments, and whether the result is a straight-set or ramped plan.
6. Keep recommendations brief and actionable: exact set-by-set load, a conservative fallback, and one clear decision rule for changing load.
7. **Do not pull or cite readiness data by default.** For a straightforward load-target request, base advice on the exact lift history and the programmed-session context. Query health/readiness only when the user asks about recovery/readiness or it is materially necessary to answer. Before relying on any readiness metric, check that the returned sleep/recovery fields are internally coherent; omit questionable data rather than using it as a confidence signal.

## Percentage-programming guidance

- Percentages normally mean the athlete's stated/current 1RM or training max; use a recorded single only if no fresher basis exists, explicitly labelling that assumption.
- If a range is given (e.g. 72–76%), offer either a straight-set load within range or a small progression across sets. Do not prescribe an increment that exceeds the requested ceiling after rounding.
- Use recently completed volume as a reality check. A historical max can overstate present readiness after a break or a low-volume period.
- Do not calculate an estimated 1RM mentally. Use `execute_code` or terminal and label it as an estimate (e.g. Epley), not a tested max.
- Respect session context: Sathya attends programmed group/CrossFit-style classes, so frame the session as part of the weekly programme rather than a standalone custom strength block.

## Weekly blog snapshot workflow

1. Query week-bounded workouts in chronological order.
2. Retrieve details for each listed workout in parallel when highlights or exact movements are needed.
3. Aggregate count, duration, sets, exercise count, calories, and recorded load volume; calculate totals via a tool.
4. Check achievements, but include only those whose dates fall inside the requested window.
5. Produce a postable short narrative plus clean bullets. Do not overstate bodyweight sets as external-load volume.

## Pitfalls

- **Do not assume the target lift.** A previous front-squat session does not establish that a new prescription is for front squat. This caused an incorrect load recommendation in a prior session.
- A calendar without an activity does not identify an exercise; ask rather than guessing.
- Motra's `max weight` is simply the heaviest logged set and may not be a true 1RM.
- Workout/achievement queries may be interrupted by a new user message. Retain completed data, rerun only the missing calls, and then deliver the requested result.

## Training context
- Sathya moved from 2x45-minute individual PT sessions to 3x60-minute gym group/CrossFit-style classes weekly. Assess sessions within that weekly programme, not as standalone self-designed strength workouts.

## References

- `references/motra-percentage-loads.md` — Motra-specific interpretation and a worked back-squat decision pattern.
