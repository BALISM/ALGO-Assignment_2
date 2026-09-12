# ------------------------------------------------------------------ #
#  extrapolate.py  (Part E)                                            #
#  Fit each algorithm's measured growth to t = c × n² and project     #
#  runtime for the full loaded dataset.  Also benchmarks Python's      #
#  built-in sorted() to show the O(n log n) speedup factor.           #
#                                                                      #
#  Input:  sort_benchmark_results.csv  (produced by benchmark.py)      #
#  The raw data/ CSV files are only re-read if available locally;      #
#  otherwise a hard-coded fallback row count is used.                  #
# ------------------------------------------------------------------ #

import os
import time
import random

import numpy as np
import pandas as pd

RESULTS_FILE = 'sort_benchmark_results.csv'
YEARLY_FILES = ['2015.csv', '2016.csv', '2017.csv', '2018.csv']
DATA_DIR     = './data'

# Row count recorded from explore_data.py (Part A).  Used when the
# data/ folder is absent so the projection still has a meaningful n.
KNOWN_TOTAL_ROWS = 24_324_804


def count_dataset_rows():
    """
    Return the total row count of the loaded dataset.

    Re-reads the files if data/ is present; otherwise returns the
    pre-recorded value from Part A to keep the script portable.
    """
    if not os.path.isdir(DATA_DIR):
        print(
            f'Note: {DATA_DIR}/ not found on this machine — '
            f'using pre-recorded row count ({KNOWN_TOTAL_ROWS:,})'
        )
        return KNOWN_TOTAL_ROWS

    total = 0
    for fname in YEARLY_FILES:
        fpath = os.path.join(DATA_DIR, fname)
        for piece in pd.read_csv(fpath, chunksize=1_000_000, usecols=['ARR_DELAY']):
            total += len(piece)
    return total


def estimate_c(sizes, times):
    """
    Estimate the constant c in  t = c × n²  from empirical measurements.

    Uses the single largest measured n (most reliable signal-to-noise
    ratio; timer overhead is proportionally smallest at large n).
    """
    sizes_arr = np.array(sizes, dtype=float)
    times_arr = np.array(times, dtype=float)
    best_idx  = np.argmax(sizes_arr)
    return times_arr[best_idx] / (sizes_arr[best_idx] ** 2)


def human_readable(seconds):
    """Convert a duration in seconds to the most readable unit."""
    if seconds < 60:
        return f'{seconds:.2f} sec'
    minutes = seconds / 60
    if minutes < 60:
        return f'{minutes:.2f} min'
    hours = minutes / 60
    if hours < 24:
        return f'{hours:.2f} hrs'
    days = hours / 24
    if days < 365:
        return f'{days:.2f} days'
    return f'{days / 365:.2f} years'


# ── Main ─────────────────────────────────────────────────────────── #

if __name__ == '__main__':
    bench_df = pd.read_csv(RESULTS_FILE)

    # Use ARR_DELAY random-order data as the representative growth curve
    baseline = bench_df[
        (bench_df['column']   == 'ARR_DELAY') &
        (bench_df['ordering'] == 'random')
    ]

    full_n = count_dataset_rows()
    print(f'\nFull-scale target: {full_n:,} rows (2015-2018 loaded set)\n')

    header = f'{"Algorithm":<16}{"Fitted c":>14}{"Projected time":>18}'
    print(header)
    print('-' * 48)

    c_values = {}
    for algo in baseline['algorithm'].unique():
        algo_df = baseline[baseline['algorithm'] == algo].sort_values('size')
        c = estimate_c(algo_df['size'].tolist(), algo_df['time_seconds'].tolist())
        c_values[algo] = c
        projected = c * (full_n ** 2)
        print(f'{algo:<16}{c:>14.3e}{human_readable(projected):>18}')

    # ── O(n log n) baseline: time Python's built-in sorted() ────── #
    probe_n    = 10_000
    probe_data = [random.random() for _ in range(probe_n)]
    t_start    = time.perf_counter()
    sorted(probe_data)
    builtin_elapsed = time.perf_counter() - t_start

    c_nlogn          = builtin_elapsed / (probe_n * np.log2(probe_n))
    projected_builtin = c_nlogn * full_n * np.log2(full_n)

    print(
        f'\n{"builtin (Timsort)":<16}{c_nlogn:>14.3e}'
        f'{human_readable(projected_builtin):>18}'
    )

    slowest_quad = max(c_values.values()) * (full_n ** 2)
    speedup      = slowest_quad / projected_builtin
    print(f'\nO(n²) vs O(n log n) speedup factor at full scale: {speedup:,.0f}x')