# ------------------------------------------------------------------ #
#  dataset_analysis.py  (Part A)                                       #
#  Load all chosen yearly CSV files in chunks, report row counts,      #
#  column names, memory usage, and basic statistics for ARR_DELAY.     #
# ------------------------------------------------------------------ #

import pandas as pd
import os

# Four files selected after checking sizes with file_overview.py.
# Together they cover 2015-2018 and total roughly 4 GB.
chosen_files = ['2015.csv', '2016.csv', '2017.csv', '2018.csv']
data_dir = './data'

row_total       = 0
col_names       = None
mem_per_chunk   = None          # MB for one 1M-row chunk

# ── Pass 1: count rows and capture schema from the very first chunk ──
for fname in chosen_files:
    fpath = os.path.join(data_dir, fname)
    print(f'Processing {fname}...')

    for chunk_idx, chunk in enumerate(pd.read_csv(fpath, chunksize=1_000_000)):
        row_total += len(chunk)

        if col_names is None:
            col_names     = list(chunk.columns)
            mem_per_chunk = chunk.memory_usage(deep=True).sum() / 1e6
            print(f'  Columns ({len(col_names)}): {col_names}')
            print(f'  Memory footprint of one chunk: {mem_per_chunk:.2f} MB')

        if chunk_idx % 5 == 0:
            print(f'  ...chunk {chunk_idx}, running total: {row_total:,}')

print(f'\nTOTAL ROWS across all 4 files: {row_total:,}')

# ── Pass 2: accumulate ARR_DELAY statistics without loading all at once ──
print('\n--- ARR_DELAY statistics ---')
accum = {'min_vals': [], 'max_vals': [], 'running_sum': 0,
         'valid_count': 0, 'missing_count': 0}

for fname in chosen_files:
    fpath = os.path.join(data_dir, fname)
    for chunk in pd.read_csv(fpath, chunksize=1_000_000, usecols=['ARR_DELAY']):
        col = chunk['ARR_DELAY']
        accum['min_vals'].append(col.min())
        accum['max_vals'].append(col.max())
        accum['running_sum']  += col.sum()
        accum['valid_count']  += col.notna().sum()
        accum['missing_count'] += col.isna().sum()

global_min  = min(accum['min_vals'])
global_max  = max(accum['max_vals'])
global_mean = accum['running_sum'] / accum['valid_count']
all_vals    = accum['valid_count'] + accum['missing_count']
pct_missing = accum['missing_count'] / all_vals * 100

print(f'Min:       {global_min}')
print(f'Max:       {global_max}')
print(f'Mean:      {global_mean:.2f}')
print(f'% Missing: {pct_missing:.2f}%')
