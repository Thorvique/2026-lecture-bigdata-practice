# Task 2 · Explosion curve

The experiment uses the fixed `bench.build()` workload: 20,000 baskets and 2,000 possible items. `peak_counters` is the largest live pair dictionary observed during PlainApriori pass two; `peak_bytes` is the peak Python allocation reported by `tracemalloc`.

## Machine and conditions

- **platform:** Windows-11-10.0.26200-SP0
- **processor:** Intel64 Family 6 Model 183 Stepping 1, GenuineIntel
- **logical_cpus:** 32
- **ram_gb:** 34.05
- **python:** 3.14.0
- **started_at:** 2026-10-07T06:15:49.889792+02:00
- **conditions:** Interactive Windows desktop with Codex and PowerShell active; no deliberate background load.

## Measurements

| support | frequent pairs | peak counters | peak Python MB | seconds | status |
|---:|---:|---:|---:|---:|:---|
| 400 | 249 | 10,585 | 1.1 | 0.73 | completed |
| 200 | 776 | 58,626 | 6.7 | 1.67 | completed |
| 100 | 2,244 | 273,701 | 28.6 | 4.32 | completed |
| 50 | 6,397 | 820,259 | 107.7 | 7.97 | completed |
| 25 | 17,045 | 893,456 | 107.7 | 8.42 | completed |
| 12 | 43,116 | 893,456 | 109.8 | 8.54 | completed |
| 6 | 101,938 | 893,456 | 126.5 | 8.26 | completed |
| 3 | 250,054 | 893,456 | 163.9 | 8.09 | completed |
| 1 | 893,456 | 893,456 | 334.3 | 9.90 | completed |

### Growth when support is halved

| from → to | counter growth | frequent-pair growth |
|:---|---:|---:|
| 400 → 200 | 5.54× | 3.12× |
| 200 → 100 | 4.67× | 2.89× |
| 100 → 50 | 3.00× | 2.85× |
| 50 → 25 | 1.09× | 2.66× |
| 25 → 12 | 1.00× | 2.53× |
| 12 → 6 | 1.00× | 2.36× |
| 6 → 3 | 1.00× | 2.45× |
| 3 → 1 | 1.00× | 3.57× |

## Interpretation

Lower support expands the set of singleton survivors, so the candidate pair dictionary grows faster than the final answer set. That gap is the memory problem PCY is designed to reduce.

## Stopping point

- **Support:** 1
- **What happened:** Support 1 was the stopping point: all 893,456 observed pairs became frequent, so the counter set saturated and the run was no longer a useful threshold experiment.
- **Limiting resource:** Memory became the limiting resource: peak Python allocation was 334.3 MB at support 1, although the run completed safely.
