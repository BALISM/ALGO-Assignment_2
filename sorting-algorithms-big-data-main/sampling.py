import pandas as pd
import numpy as np

def load_column_sample(files, column, folder='./data'):
    """Load one column across all chosen files into a single Series."""
    all_values = []
    for filename in files:
        path = f'{folder}/{filename}'
        for chunk in pd.read_csv(path, chunksize=1_000_000, usecols=[column]):
            all_values.append(chunk[column].dropna())
    return pd.concat(all_values, ignore_index=True)


def draw_sample(full_series, n, seed=42):
    """Draw a random sample of size n, and return random/sorted/reversed variants."""
    rng = np.random.default_rng(seed)
    sample = full_series.sample(n=n, random_state=seed).tolist()

    random_order = sample.copy()
    sorted_order = sorted(sample)
    reversed_order = sorted(sample, reverse=True)

    return {
        'random': random_order,
        'sorted': sorted_order,
        'reversed': reversed_order
    }


if __name__ == '__main__':
    files = ['2015.csv', '2016.csv', '2017.csv', '2018.csv']

    print('Loading ARR_DELAY column...')
    arr_delay_full = load_column_sample(files, 'ARR_DELAY')
    print(f'Total non-missing ARR_DELAY values available: {len(arr_delay_full):,}')

    # Quick test with a small sample size
    variants = draw_sample(arr_delay_full, n=1000)
    print(f"Random sample (first 5): {variants['random'][:5]}")
    print(f"Sorted sample (first 5): {variants['sorted'][:5]}")
    print(f"Reversed sample (first 5): {variants['reversed'][:5]}")