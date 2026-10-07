#!/usr/bin/env python3
"""Week 6 · Task 2 — Lower the threshold until your machine says no.

Textbook §6.1, §6.2.

Support is a knob, and turning it down is how you find the interesting rules.
It is also how you run out of memory, and where that happens is a fact about
your laptop rather than about the algorithm.

    python3 task2_explosion.py --supports 400,200,100,50,25
    python3 task2_explosion.py --supports 12,6            # careful

Lower the threshold until something gives. Write down where and what.
"""
import argparse, ctypes, datetime, json, os, platform, time, tracemalloc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def machine():
    ram_bytes = None
    if os.name == "nt":
        class MemoryStatus(ctypes.Structure):
            _fields_ = [("length", ctypes.c_ulong),
                        ("memory_load", ctypes.c_ulong),
                        ("total_phys", ctypes.c_ulonglong),
                        ("avail_phys", ctypes.c_ulonglong),
                        ("total_page", ctypes.c_ulonglong),
                        ("avail_page", ctypes.c_ulonglong),
                        ("total_virtual", ctypes.c_ulonglong),
                        ("avail_virtual", ctypes.c_ulonglong),
                        ("avail_extended", ctypes.c_ulonglong)]
        status = MemoryStatus()
        status.length = ctypes.sizeof(MemoryStatus)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            ram_bytes = status.total_phys

    return {
        "platform": platform.platform(),
        "processor": platform.processor() or platform.machine(),
        "logical_cpus": os.cpu_count(),
        "ram_gb": round(ram_bytes / 1e9, 2) if ram_bytes else None,
        "python": platform.python_version(),
        "started_at": datetime.datetime.now().astimezone().isoformat(),
    }


def write_report(path, data):
    runs = sorted(data.get("runs", []), key=lambda row: row["support"],
                  reverse=True)
    lines = [
        "# Task 2 · Explosion curve",
        "",
        "The experiment uses the fixed `bench.build()` workload: 20,000 baskets "
        "and 2,000 possible items. `peak_counters` is the largest live pair "
        "dictionary observed during PlainApriori pass two; `peak_bytes` is the "
        "peak Python allocation reported by `tracemalloc`.",
        "",
        "## Machine and conditions",
        "",
    ]
    machine_info = data.get("machine", {})
    for key in ("platform", "processor", "logical_cpus", "ram_gb", "python",
                "started_at", "conditions"):
        if key in machine_info and machine_info[key] not in (None, ""):
            lines.append(f"- **{key}:** {machine_info[key]}")
    lines += ["", "## Measurements", "",
              "| support | frequent pairs | peak counters | peak Python MB | seconds | status |",
              "|---:|---:|---:|---:|---:|:---|"]
    for row in runs:
        lines.append(
            f"| {row['support']} | {row.get('frequent_pairs', '—'):,} | "
            f"{row.get('peak_counters', '—'):,} | "
            f"{row.get('peak_bytes', 0) / 1e6:.1f} | "
            f"{row.get('seconds', 0):.2f} | {row.get('status', 'completed')} |"
        )

    if len(runs) >= 2:
        lines += ["", "### Growth when support is halved", "",
                  "| from → to | counter growth | frequent-pair growth |",
                  "|:---|---:|---:|"]
        by_support = {row["support"]: row for row in runs
                      if row.get("status", "completed") == "completed"}
        supports = sorted(by_support, reverse=True)
        for high, low in zip(supports, supports[1:]):
            hi, lo = by_support[high], by_support[low]
            counter_ratio = (lo["peak_counters"] / hi["peak_counters"]
                             if hi["peak_counters"] else 0)
            pair_ratio = (lo["frequent_pairs"] / hi["frequent_pairs"]
                          if hi["frequent_pairs"] else 0)
            lines.append(f"| {high} → {low} | {counter_ratio:.2f}× | "
                         f"{pair_ratio:.2f}× |")

    lines += ["", "## Interpretation", "",
              "Lower support expands the set of singleton survivors, so the "
              "candidate pair dictionary grows faster than the final answer "
              "set. That gap is the memory problem PCY is designed to reduce."]
    stopping = data.get("stopping", {})
    if stopping:
        lines += ["", "## Stopping point", "",
                  f"- **Support:** {stopping.get('support', 'not recorded')}",
                  f"- **What happened:** {stopping.get('reason', 'not recorded')}",
                  f"- **Limiting resource:** {stopping.get('resource', 'not recorded')}"]

    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--supports", default="400,200,100,50,25")
    p.add_argument("--conditions", default=(
        "Interactive Windows desktop with Codex and PowerShell active; "
        "no deliberate background load."))
    p.add_argument("--stopped-at", type=int, default=None)
    p.add_argument("--stop-reason", default="")
    p.add_argument("--limiting-resource", default="")
    a = p.parse_args()
    os.makedirs(OUT, exist_ok=True)

    import bench
    from task3_pcy import PlainApriori
    baskets = bench.build()

    rows = []
    for support in dict.fromkeys(int(x) for x in a.supports.split(",")):
        algo = PlainApriori(support)
        tracemalloc.start()
        t0 = time.perf_counter()
        try:
            pairs = algo.run(baskets)
            elapsed = time.perf_counter() - t0
            _, peak_bytes = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()

        row = {"support": support, "frequent_pairs": len(pairs),
               "peak_counters": algo.peak_counters, "seconds": elapsed,
               "peak_bytes": peak_bytes, "status": "completed"}
        rows.append(row)
        print(f"  support {support:>5}   pairs {len(pairs):>7,}   "
              f"counters {algo.peak_counters:>10,}   "
              f"{elapsed:>7.2f}s   {peak_bytes / 1e6:>8.1f} MB")

    path = os.path.join(OUT, "explosion.json")
    prior = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    prior["machine"] = machine()
    prior["machine"]["conditions"] = a.conditions
    old_runs = {row["support"]: row for row in prior.get("runs", [])}
    old_runs.update({row["support"]: row for row in rows})
    prior["runs"] = list(old_runs.values())
    if a.stopped_at is not None or a.stop_reason or a.limiting_resource:
        prior["stopping"] = {
            "support": a.stopped_at,
            "reason": a.stop_reason,
            "resource": a.limiting_resource,
        }
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(prior, handle, indent=2)
    write_report(os.path.join(OUT, "explosion.md"), prior)
    print(f"\n  -> out/explosion.json and out/explosion.md  "
          f"({len(prior['runs'])} run(s))")
    print("  Keep halving the support until it is unbearable. Record where.")


if __name__ == "__main__":
    main()
