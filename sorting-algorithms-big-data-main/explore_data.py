import pandas as pd
import os

# The 4 files we chose in Step 2, based on check_sizes.py output
files = ['2015.csv', '2016.csv', '2017.csv', '2018.csv']
folder = './data'

total_rows = 0
columns = None
chunk_memory_mb = None

for filename in files:
    path = os.path.join(folder, filename)
    print(f'Processing {filename}...')

    for i, chunk in enumerate(pd.read_csv(path, chunksize=1_000_000)):
        total_rows += len(chunk)

        # Grab columns and memory footprint just once, from the very first chunk
        if columns is None:
            columns = list(chunk.columns)
            chunk_memory_mb = chunk.memory_usage(deep=True).sum() / 1e6
            print(f'  Columns ({len(columns)}): {columns}')
            print(f'  Memory footprint of one chunk: {chunk_memory_mb:.2f} MB')

        if i % 5 == 0:
            print(f'  ...chunk {i}, running total rows: {total_rows:,}')

print(f'\nTOTAL ROWS across all 4 files: {total_rows:,}')
# Basic stats for our chosen numeric column: ARR_DELAY
print('\n--- ARR_DELAY statistics ---')
stats_accum = {'min': [], 'max': [], 'sum': 0, 'count': 0, 'missing': 0}

for filename in files:
    path = os.path.join(folder, filename)
    for chunk in pd.read_csv(path, chunksize=1_000_000, usecols=['ARR_DELAY']):
        col = chunk['ARR_DELAY']
        stats_accum['min'].append(col.min())
        stats_accum['max'].append(col.max())
        stats_accum['sum'] += col.sum()
        stats_accum['count'] += col.notna().sum()
        stats_accum['missing'] += col.isna().sum()

overall_min = min(stats_accum['min'])
overall_max = max(stats_accum['max'])
overall_mean = stats_accum['sum'] / stats_accum['count']
total_values = stats_accum['count'] + stats_accum['missing']
pct_missing = stats_accum['missing'] / total_values * 100

print(f'Min: {overall_min}')
print(f'Max: {overall_max}')
print(f'Mean: {overall_mean:.2f}')
print(f'% Missing: {pct_missing:.2f}%')
