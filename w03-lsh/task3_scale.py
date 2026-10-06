#!/usr/bin/env python3
"""Week 3 · Task 3 — Find the same pairs without comparing everything.

Textbook §3.4.

`BruteForce` compares every pair. On 3,000 documents that is 4.5 million
comparisons and it is completely correct. On 3 million documents it is 4.5
trillion and it is completely useless.

Beat it. Find the same near-duplicate pairs while making far fewer comparisons.

    python3 bench.py
    python3 bench.py --yours

The harness counts every call you make to `similarity()`. That is your score.
It also checks **recall** - which of the truly similar pairs you found. Skipping
comparisons is easy; skipping comparisons without losing the pairs is the task.
"""

PRIME = 10007
HASHES = 120
BANDS = 30


class BruteForce:
    """Correct, and quadratic."""

    def __init__(self, threshold):
        self.threshold = threshold

    def find(self, docs, similarity):
        """docs is [set_of_shingles, ...]. Return {(i, j), ...} with i < j."""
        out = set()
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                if similarity(docs[i], docs[j]) >= self.threshold:
                    out.add((i, j))
        return out


class YourFinder:
    """Your near-duplicate finder.

        __init__(threshold)
        find(docs, similarity) -> {(i, j), ...}

    `similarity(a, b)` is the only way to compare two documents, and every call
    is counted. Everything else - signatures, banding, bucketing - is free, in
    the sense that the harness does not charge you for it. That is deliberate:
    it is also roughly true at scale, where the comparison is the expensive
    part and the hashing is linear.

    Two knobs decide everything:

        the number of hashes in a signature
        how many bands you split it into

    §3.4.2 gives you the relationship between those and the probability that a
    pair at similarity s becomes a candidate. It is an S-curve, and where its
    step sits is something you choose. Choose it on purpose and be able to say
    why in observation.md - a threshold of 0.8 does not mean bands should be
    anything in particular until you have done the arithmetic.

    You may reuse your Task 1 code.
    """

    def __init__(self, threshold):
        self.threshold = threshold
        self.hashes = [((i * 37 + 1) % PRIME, (i * 101 + 17) % PRIME)
                       for i in range(HASHES)]

    def find(self, docs, similarity):
        signatures = [[PRIME] * HASHES for _ in docs]
        for doc_index, doc in enumerate(docs):
            signature = signatures[doc_index]
            for shingle in doc:
                for h, (a, b) in enumerate(self.hashes):
                    value = (a * shingle + b) % PRIME
                    if value < signature[h]:
                        signature[h] = value

        rows_per_band = HASHES // BANDS
        candidates = set()
        for band in range(BANDS):
            start = band * rows_per_band
            buckets = {}
            for index, signature in enumerate(signatures):
                key = tuple(signature[start:start + rows_per_band])
                buckets.setdefault(key, []).append(index)
            for bucket in buckets.values():
                for left, i in enumerate(bucket):
                    for j in bucket[left + 1:]:
                        candidates.add((i, j) if i < j else (j, i))

        return {pair for pair in candidates
                if similarity(docs[pair[0]], docs[pair[1]]) >= self.threshold}
