# ------------------------------------------------------------------ #
#  sampling.py                                                         #
#  Helpers for loading a single column from the chosen CSV files and   #
#  producing the three ordering variants used in benchmarking.         #
# ------------------------------------------------------------------ #

import pandas as pd
import numpy as np


def load_column_sample(file_list, col_name, data_folder='./data'):
    """
    Stream-read *col_name* from every file in *file_list* and return
    all non-missing values concatenated into a single pandas Series.

    Reads in 1-million-row chunks to avoid loading the full CSVs into
    memory at once.
    """
    collected = []
    for fname in file_list:
        filepath = f'{data_folder}/{fname}'
        for piece in pd.read_csv(filepath, chunksize=1_000_000, usecols=[col_name]):
            collected.append(piece[col_name].dropna())
    return pd.concat(collected, ignore_index=True)


def draw_sample(full_series, n, seed=42):
    """
    Draw *n* random rows from *full_series* and return a dict with three
    ordering variants:

        'random'   — the sample in the order it was drawn (average case)
        'sorted'   — ascending order                       (best case)
        'reversed' — descending order                      (worst case)

    The same *seed* is used every call so results are reproducible.
    """
    _ = np.random.default_rng(seed)          # kept for reproducibility parity
    base_sample = full_series.sample(n=n, random_state=seed).tolist()

    return {
        'random':   base_sample[:],
        'sorted':   sorted(base_sample),
        'reversed': sorted(base_sample, reverse=True),
    }


# ------------------------------------------------------------------ #
#  Quick smoke-test                                                    #
# ------------------------------------------------------------------ #
if __name__ == '__main__':
    target_files = ['2015.csv', '2016.csv', '2017.csv', '2018.csv']

    print('Reading ARR_DELAY column from disk...')
    delay_series = load_column_sample(target_files, 'ARR_DELAY')
    print(f'Non-missing ARR_DELAY values available: {len(delay_series):,}')

    test_variants = draw_sample(delay_series, n=1000)
    print(f"Random  (first 5): {test_variants['random'][:5]}")
    print(f"Sorted  (first 5): {test_variants['sorted'][:5]}")
    print(f"Reversed(first 5): {test_variants['reversed'][:5]}")