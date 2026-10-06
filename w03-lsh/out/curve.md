# Task 2 · Measured curve

Machine: Windows 11, Intel Core i9-14900HX (24 cores / 32 logical processors),
Python 3.14.0, 31.7 GiB RAM. No other deliberate workload was running during
the measurements. The data and timings below are from `task2_crossover.py` on
this machine; the harness uses the fixed synthetic generator from `bench.py`.

| documents | brute time (s) | brute comparisons | brute peak (MiB) | LSH time (s) | LSH comparisons | LSH peak (MiB) |
|---:|---:|---:|---:|---:|---:|---:|
| 125 | 0.092 | 7,750 | 0.006 | 0.872 | 1 | 0.249 |
| 250 | 0.337 | 31,125 | 0.007 | 1.786 | 2 | 0.482 |
| 500 | 1.492 | 124,750 | 0.007 | 3.719 | 19 | 0.959 |
| 1,000 | 5.961 | 499,500 | 0.009 | 7.453 | 126 | 1.930 |
| 1,250 | 10.905 | 780,625 | 0.012 | 10.888 | 153 | 2.457 |
| 1,500 | 15.786 | 1,124,250 | 0.009 | 13.004 | 197 | 2.886 |
| 2,000 | 25.018 | 1,999,000 | 0.017 | 17.419 | 367 | 3.903 |
| 2,120 | 32.693 | 2,246,140 | 0.018 | 18.880 | 384 | 4.043 |

The brute-force timing ratios when doubling n were 3.66× (125→250), 4.42×
(250→500), and 4.00× (500→1,000), which is consistent with a quadratic curve.
The crossover is approximately n=1,250: at 1,000 brute force is faster, while
at 1,250 LSH is marginally faster. At the largest tested size the unpleasant
part was time (32.7 s for brute force), not memory pressure; LSH used 4.043 MiB
of traced peak memory versus 0.018 MiB for the comparison loop.

