import time
import csv
import pandas as pd
import matplotlib.pyplot as plt

from sampling import load_column_sample, draw_sample
from sort_algorithms import bubble_sort, selection_sort, insertion_sort

FILES = ['2015.csv', '2016.csv', '2017.csv', '2018.csv']
SAMPLE_SIZES = [100, 500, 1000, 2000, 5000, 10000]
ALGORITHMS = {
    'bubble_sort': bubble_sort,
    'selection_sort': selection_sort,
    'insertion_sort': insertion_sort,
}
RESULTS_CSV = 'sort_benchmark_results.csv'


def time_sort(fn, data):
    """Time a single sort call using perf_counter."""
    start = time.perf_counter()
    fn(data)
    end = time.perf_counter()
    return end - start


def run_benchmark(full_series, sizes, column_label):
    """Run all algorithms on all sizes/orderings for one column. Returns list of result rows."""
    rows = []
    for n in sizes:
        variants = draw_sample(full_series, n=n)
        for ordering, data in variants.items():
            for algo_name, algo_fn in ALGORITHMS.items():
                print(f'  [{column_label}] n={n:<6} ordering={ordering:<8} algo={algo_name:<15}', end=' ')
                elapsed = time_sort(algo_fn, data)
                print(f'{elapsed:.6f}s')
                rows.append({
                    'column': column_label,
                    'size': n,
                    'ordering': ordering,
                    'algorithm': algo_name,
                    'time_seconds': elapsed,
                })
    return rows


if __name__ == '__main__':
    all_rows = []

    # --- Numeric column: ARR_DELAY, full set of sample sizes ---
    print('Loading ARR_DELAY...')
    arr_delay_full = load_column_sample(FILES, 'ARR_DELAY')
    print(f'Total non-missing ARR_DELAY values: {len(arr_delay_full):,}\n')

    print('Benchmarking ARR_DELAY (numeric)...')
    all_rows += run_benchmark(arr_delay_full, SAMPLE_SIZES, 'ARR_DELAY')

    # --- Text column: OP_CARRIER, just ONE sample size for comparison (Part D task 4) ---
    print('\nLoading OP_CARRIER...')
    carrier_full = load_column_sample(FILES, 'OP_CARRIER')
    print(f'Total non-missing OP_CARRIER values: {len(carrier_full):,}\n')

    text_compare_size = 2000  # pick one size to compare numeric vs text directly
    print(f'Benchmarking OP_CARRIER (text) at n={text_compare_size}...')
    all_rows += run_benchmark(carrier_full, [text_compare_size], 'OP_CARRIER')

    # --- Export to CSV ---
    with open(RESULTS_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['column', 'size', 'ordering', 'algorithm', 'time_seconds'])
        writer.writeheader()
        writer.writerows(all_rows)
    print(f'\nResults written to {RESULTS_CSV}')

    # --- Chart 1: runtime vs n, one line per algorithm, random ordering, ARR_DELAY only ---
    df = pd.DataFrame(all_rows)
    numeric_random = df[(df['column'] == 'ARR_DELAY') & (df['ordering'] == 'random')]

    plt.figure(figsize=(8, 5))
    for algo_name in ALGORITHMS:
        subset = numeric_random[numeric_random['algorithm'] == algo_name].sort_values('size')
        plt.plot(subset['size'], subset['time_seconds'], marker='o', label=algo_name)
    plt.xlabel('Sample size (n)')
    plt.ylabel('Time (seconds)')
    plt.title('Runtime vs n (random order, ARR_DELAY)')
    plt.legend()
    plt.grid(True)
    plt.savefig('chart_runtime_vs_n.png')
    print('Saved chart_runtime_vs_n.png')

    # --- Chart 2: insertion sort, random vs sorted vs reversed, ARR_DELAY only ---
    insertion_numeric = df[(df['column'] == 'ARR_DELAY') & (df['algorithm'] == 'insertion_sort')]

    plt.figure(figsize=(8, 5))
    for ordering in ['random', 'sorted', 'reversed']:
        subset = insertion_numeric[insertion_numeric['ordering'] == ordering].sort_values('size')
        plt.plot(subset['size'], subset['time_seconds'], marker='o', label=ordering)
    plt.xlabel('Sample size (n)')
    plt.ylabel('Time (seconds)')
    plt.title('Insertion Sort: random vs sorted vs reversed (ARR_DELAY)')
    plt.legend()
    plt.grid(True)
    plt.savefig('chart_insertion_sort_orderings.png')
    print('Saved chart_insertion_sort_orderings.png')