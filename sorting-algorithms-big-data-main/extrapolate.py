"""
Part F: Curve fitting and full-scale extrapolation.

Fits each algorithm's measured runtimes to the model  t = c * n^2
(least squares, forced through the origin, since all three sorts are
O(n^2) and t=0 at n=0), then uses that fitted c to project how long a
full sort of the entire loaded dataset would take.

Reads sort_benchmark_results.csv (produced by benchmark.py) - it does
NOT need the raw data/ CSVs to fit the curve. It only re-touches the
data/ files to count the exact number of rows to extrapolate to; if
that folder isn't present, it falls back to FALLBACK_TOTAL_ROWS below.
"""

import os
import pandas as pd
import numpy as np

RESULTS_CSV = 'sort_benchmark_results.csv'
FILES = ['2015.csv', '2016.csv', '2017.csv', '2018.csv']
FOLDER = './data'

# "TOTAL ROWS across all 4 files" as printed by explore_data.py (Part A).
# Used as a fallback if data/ isn't available when this script runs, so
# the extrapolation still has a real n to project to.
FALLBACK_TOTAL_ROWS = 24_324_804


def get_total_rows():
    """Count exact rows in the chosen files if data/ is available,
    otherwise fall back to the value already recorded from Part A."""
    if not os.path.isdir(FOLDER):
        print(f'{FOLDER} not found locally - using FALLBACK_TOTAL_ROWS '
              f'from Part A output ({FALLBACK_TOTAL_ROWS:,})')
        return FALLBACK_TOTAL_ROWS

    total = 0
    for filename in FILES:
        path = os.path.join(FOLDER, filename)
        for chunk in pd.read_csv(path, chunksize=1_000_000, usecols=['ARR_DELAY']):
            total += len(chunk)
    return total


def fit_c_n_squared(sizes, times):
    """Estimate c in t = c * n^2 from the largest measured n.

    We use the single largest sample (n=10,000) rather than a multi-point
    least-squares fit, since t=0 at n=0 pins the curve at one end and the
    largest n gives the most reliable estimate of the n^2 growth rate
    (least relative noise from timer overhead). This matches the c values
    reported in the Part F write-up.
    """
    n = np.array(sizes, dtype=float)
    t = np.array(times, dtype=float)
    idx = np.argmax(n)
    return t[idx] / (n[idx] ** 2)


def format_duration(seconds):
    """Human-readable duration for very large extrapolated times."""
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
    years = days / 365
    return f'{years:.2f} years'


if __name__ == '__main__':
    df = pd.read_csv(RESULTS_CSV)

    # Fit on ARR_DELAY, random ordering - the baseline growth curve
    sub = df[(df['column'] == 'ARR_DELAY') & (df['ordering'] == 'random')]

    total_rows = get_total_rows()
    print(f'\nFull-scale target: {total_rows:,} rows (2015-2018 loaded set)\n')

    print(f'{"Algorithm":<16}{"Fitted c":>14}{"Projected time":>18}')
    print('-' * 48)

    fitted = {}
    for algo in sub['algorithm'].unique():
        algo_rows = sub[sub['algorithm'] == algo].sort_values('size')
        c = fit_c_n_squared(algo_rows['size'], algo_rows['time_seconds'])
        fitted[algo] = c

        projected_seconds = c * (total_rows ** 2)
        print(f'{algo:<16}{c:>14.3e}{format_duration(projected_seconds):>18}')

    # --- O(n log n) comparison, for the "Key Findings" line in the README ---
    # Python's built-in Timsort is O(n log n); benchmark it directly at a
    # small n and extrapolate the same way, using t = c * n * log2(n).
    import time
    import random

    sample_n = 10000
    sample = [random.random() for _ in range(sample_n)]
    start = time.perf_counter()
    sorted(sample)
    builtin_time = time.perf_counter() - start

    c_nlogn = builtin_time / (sample_n * np.log2(sample_n))
    projected_builtin = c_nlogn * total_rows * np.log2(total_rows)

    print(f'\n{"builtin (Timsort)":<16}{c_nlogn:>14.3e}'
          f'{format_duration(projected_builtin):>18}')

    slowest_quadratic = max(fitted.values()) * (total_rows ** 2)
    speedup = slowest_quadratic / projected_builtin
    print(f'\nO(n^2) vs O(n log n) speedup factor at full scale: '
          f'{speedup:,.0f}x')