#!/usr/bin/env python3
"""Week 6 · Task 3 — Make pass two fit.

Textbook §6.3 (PCY), §6.3.2 - §6.3.4.

`PlainApriori` does what Task 1 asked: use pass one to drop infrequent items,
then count every pair of surviving items. That is already much better than
counting all pairs. It is still not enough, because the surviving items are the
common ones, and the common ones appear together constantly.

The harness measures **the peak number of pair counters you held**, because
that is the thing that decides whether the algorithm runs at all. §6.3 is about
spending pass one's spare memory to shrink it.

    python3 bench.py
    python3 bench.py --yours

Correctness first: you must find exactly the same frequent pairs. Finding fewer
is not an optimisation.
"""
from array import array
from collections import Counter
from itertools import combinations


class PlainApriori:
    """Pass one drops infrequent items. Pass two counts every surviving pair."""

    def __init__(self, support):
        self.support = support
        self.peak_counters = 0

    def run(self, baskets):
        counts = Counter()
        for basket in baskets:
            counts.update(basket)
        frequent = {i for i, c in counts.items() if c >= self.support}

        pair_counts = Counter()
        for basket in baskets:
            items = sorted(basket & frequent)
            for pair in combinations(items, 2):
                pair_counts[pair] += 1
            self.peak_counters = max(self.peak_counters, len(pair_counts))

        return {frozenset(p): c for p, c in pair_counts.items()
                if c >= self.support}


class YourAlgorithm:
    """Your frequent-pair finder.

        __init__(support)
        run(baskets) -> {frozenset({a, b}): count}
        .peak_counters -> the most pair counters you ever held at once

    Same pairs as the baseline. Fewer counters.

    Pass one only needs one integer per item, and there are not many items. The
    rest of your memory is sitting idle while you do it. §6.3 spends it: hash
    every pair you see in pass one into a fixed array of buckets, and count the
    buckets rather than the pairs.

    A bucket whose total is below the support threshold cannot contain a
    frequent pair. In pass two you skip every pair landing in such a bucket -
    and the bucket array collapses to a bitmap, one bit each, before you need
    the memory for counters.

    Two things to be careful of:

      * a bucket being frequent does not make its pairs frequent. It is a
        filter, not an answer
      * `peak_counters` is on your honour. Count the pair counters you hold at
        the same time. The bitmap is not a pair counter, but if you keep the
        full bucket counts alive into pass two, that is not free either -
        observation.md asks about it
    """

    DEFAULT_BUCKETS = 1_000_003

    def __init__(self, support, bucket_count=DEFAULT_BUCKETS):
        if bucket_count < 1:
            raise ValueError("bucket_count must be positive")
        self.support = support
        self.bucket_count = int(bucket_count)
        self.peak_counters = 0
        self.bucket_counter_bytes = 0
        self.bitmap_bytes = 0

    def _bucket(self, a, b):
        # Tuple hashing avoids Python's randomized string hash issue while
        # remaining valid for any hashable item values.
        return hash((a, b)) % self.bucket_count

    def run(self, baskets):
        # Pass one: count singletons and hash every observed pair into a fixed
        # array.  Hashing is deliberately done before singleton filtering: it
        # is the PCY pass-one bucket count, not a second pair-counting pass.
        singleton_counts = Counter()
        bucket_counts = array("I", [0]) * self.bucket_count
        for basket in baskets:
            items = sorted(set(basket))
            singleton_counts.update(items)
            for a, b in combinations(items, 2):
                bucket_counts[self._bucket(a, b)] += 1

        frequent = {item for item, count in singleton_counts.items()
                    if count >= self.support}

        # Collapse the integer bucket counts to the bitmap used by pass two;
        # the full bucket counters are not kept alive while pair counters grow.
        bitmap = bytearray(
            1 if count >= self.support else 0 for count in bucket_counts
        )
        self.bucket_counter_bytes = len(bucket_counts) * bucket_counts.itemsize
        self.bitmap_bytes = len(bitmap)
        del bucket_counts

        pair_counts = Counter()
        for basket in baskets:
            items = sorted(set(basket) & frequent)
            for a, b in combinations(items, 2):
                if bitmap[self._bucket(a, b)]:
                    pair_counts[(a, b)] += 1
            self.peak_counters = max(self.peak_counters, len(pair_counts))

        return {frozenset(pair): count for pair, count in pair_counts.items()
                if count >= self.support}
