# ------------------------------------------------------------------ #
#  benchmark.py  (Parts B, C, D)                                       #
#  Time bubble / selection / insertion sort on random samples drawn    #
#  from the airline delay dataset, export results to CSV, and produce  #
#  two runtime charts.                                                 #
# ------------------------------------------------------------------ #

import time
import csv
import pandas as pd
import matplotlib.pyplot as plt

from sampling       import load_column_sample, draw_sample
from sort_algorithms import bubble_sort, selection_sort, insertion_sort

# ── Configuration ────────────────────────────────────────────────── #
YEARLY_FILES   = ['2015.csv', '2016.csv', '2017.csv', '2018.csv']
SAMPLE_SIZES   = [100, 500, 1000, 2000, 5000, 10000]

SORT_FUNCTIONS = {
    'bubble_sort':    bubble_sort,
    'selection_sort': selection_sort,
    'insertion_sort': insertion_sort,
}

OUTPUT_CSV = 'sort_benchmark_results.csv'


# ── Helpers ──────────────────────────────────────────────────────── #

def measure_sort(sort_fn, dataset):
    """Return wall-clock seconds taken by sort_fn on dataset."""
    t0 = time.perf_counter()
    sort_fn(dataset)
    return time.perf_counter() - t0


def run_benchmark(series, sizes, col_label):
    """
    Run every (algorithm × size × ordering) combination for one column.
    Returns a list of result dicts ready for CSV export.
    """
    result_rows = []
    for n in sizes:
        variants = draw_sample(series, n=n)
        for order_name, data_list in variants.items():
            for fn_name, fn in SORT_FUNCTIONS.items():
                print(
                    f'  [{col_label}] n={n:<6} ordering={order_name:<8} '
                    f'algo={fn_name:<15}',
                    end=' ',
                )
                elapsed = measure_sort(fn, data_list)
                print(f'{elapsed:.6f}s')
                result_rows.append({
                    'column':       col_label,
                    'size':         n,
                    'ordering':     order_name,
                    'algorithm':    fn_name,
                    'time_seconds': elapsed,
                })
    return result_rows


# ── Main entry point ─────────────────────────────────────────────── #

if __name__ == '__main__':
    all_results = []

    # ── Numeric column: ARR_DELAY — full set of sample sizes ──
    print('Loading ARR_DELAY...')
    delay_series = load_column_sample(YEARLY_FILES, 'ARR_DELAY')
    print(f'Total non-missing ARR_DELAY values: {len(delay_series):,}\n')

    print('Benchmarking ARR_DELAY (numeric)...')
    all_results += run_benchmark(delay_series, SAMPLE_SIZES, 'ARR_DELAY')

    # ── Text column: OP_CARRIER — single size for numeric vs text (Part D §4) ──
    print('\nLoading OP_CARRIER...')
    carrier_series = load_column_sample(YEARLY_FILES, 'OP_CARRIER')
    print(f'Total non-missing OP_CARRIER values: {len(carrier_series):,}\n')

    text_n = 2000          # the one size chosen for the text-vs-numeric comparison
    print(f'Benchmarking OP_CARRIER (text) at n={text_n}...')
    all_results += run_benchmark(carrier_series, [text_n], 'OP_CARRIER')

    # ── Export raw results ───────────────────────────────────────── #
    fieldnames = ['column', 'size', 'ordering', 'algorithm', 'time_seconds']
    with open(OUTPUT_CSV, 'w', newline='') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)
    print(f'\nResults written to {OUTPUT_CSV}')

    # ── Chart 1: runtime vs n — random order, numeric column ─────── #
    df = pd.DataFrame(all_results)
    numeric_rnd = df[(df['column'] == 'ARR_DELAY') & (df['ordering'] == 'random')]

    plt.figure(figsize=(8, 5))
    for fn_name in SORT_FUNCTIONS:
        pts = numeric_rnd[numeric_rnd['algorithm'] == fn_name].sort_values('size')
        plt.plot(pts['size'], pts['time_seconds'], marker='o', label=fn_name)
    plt.xlabel('Sample size (n)')
    plt.ylabel('Time (seconds)')
    plt.title('Runtime vs n (random order, ARR_DELAY)')
    plt.legend()
    plt.grid(True)
    plt.savefig('chart_runtime_vs_n.png')
    print('Saved chart_runtime_vs_n.png')

    # ── Chart 2: insertion sort across all orderings ─────────────── #
    ins_numeric = df[(df['column'] == 'ARR_DELAY') & (df['algorithm'] == 'insertion_sort')]

    plt.figure(figsize=(8, 5))
    for order_name in ('random', 'sorted', 'reversed'):
        pts = ins_numeric[ins_numeric['ordering'] == order_name].sort_values('size')
        plt.plot(pts['size'], pts['time_seconds'], marker='o', label=order_name)
    plt.xlabel('Sample size (n)')
    plt.ylabel('Time (seconds)')
    plt.title('Insertion Sort: random vs sorted vs reversed (ARR_DELAY)')
    plt.legend()
    plt.grid(True)
    plt.savefig('chart_insertion_sort_orderings.png')
    print('Saved chart_insertion_sort_orderings.png')