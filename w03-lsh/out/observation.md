# Week 03 observations

## Task 1

Minhashing visits each row once and updates only the columns containing a 1, so it avoids rescanning the matrix once per column. For a non-divisible signature/band count I chose to reject the input with `ValueError` rather than silently discard or pad rows. The two-hash estimate for S1–S4 was 1.0 versus the true 2/3; more hashes would narrow the sampling error, at the cost of a longer signature and more hashing.

## Task 2

On my Windows 11 machine (Core i9-14900HX, 31.7 GiB RAM), brute force was faster through n=1,000 and the crossover was approximately n=1,250 (10.905 s brute force versus 10.888 s LSH). Doubling n gave brute-force time ratios 3.66×, 4.42×, and 4.00×, supporting quadratic growth; n=2,120 was unpleasant because brute force took 32.693 s, while memory was not the limiting factor.

## Task 3

I used 120 hashes, 30 bands, and 4 rows per band: the S-curve step is `(1/30)^(1/4) ≈ 0.427`, below the 0.6 target so pairs above the threshold are likely candidates. The real run found all 121 pairs with 100% recall and precision using 384 comparisons instead of 2,246,140 (99.98% avoided); moving the step to ≈0.825 with 10 bands reduced recall to 29.8%.

