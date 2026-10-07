# Week 06 observations

## Task 1 — A-Priori and association rules

At support 1, the directional rules for `{beer, cola}` were beer → cola = 0.20 and cola → beer = 0.50, so cola → beer is the more useful claim; confidence is not symmetric. At support 3 the highest-confidence rule included diaper → beer at 0.80 confidence and 1.12 lift.

For 2,000 items, brute force needs 2,000 × 1,999 / 2 = 1,999,000 pair counters; on the 20,000-basket benchmark at support 50, A-Priori held 820,259 observed pair counters after singleton pruning.

## Task 2 — Lower the threshold until the machine says no

The practical stopping point was support 1: peak Python allocation reached 334.3 MB, and all 893,456 observed pairs were frequent, so memory—not CPU or a crash—became the limiting resource. Peak counters grew from 10,585 at support 400 to 893,456 at support 1, with 5.54×, 4.67×, and 3.00× growth on the first halvings before saturating.

Frequent pairs grew differently, from 249 at support 400 to 893,456 at support 1; after counters saturated at 893,456 by support 25, answers still grew 2.66×, 2.53×, 2.36×, 2.45×, and 3.57× on later decreases, showing why finding the answers costs much more than storing the final answers.

## Task 3 — PCY

The default PCY used 1,000,003 buckets: 4,000,012 bytes for the pass-one integer array and a 1,000,003-byte bitmap after conversion. It returned the same 6,397 pairs as baseline while reducing peak counters from 820,259 to 23,356 (97.2%); the fixed bucket cost is larger than baseline around 10,585 counters/support 400, but PCY starts winning between support 400 and 200, where baseline reached 58,626 counters.

With only 10,007 buckets (40,028-byte counts plus a 10,007-byte bitmap), every candidate bucket was effectively frequent: the result was still exactly 6,397 pairs but peak counters returned to 820,259, so the smaller array saved bucket memory but removed PCY's filtering benefit.
