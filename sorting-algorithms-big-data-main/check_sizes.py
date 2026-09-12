import os

folder = './data'
total_size = 0

for f in sorted(os.listdir(folder)):
    if f.endswith('.csv'):
        path = os.path.join(folder, f)
        size_mb = os.path.getsize(path) / 1e6
        total_size += size_mb
        print(f'{f}: {size_mb:.1f} MB')

print(f'\nTotal size of all CSVs: {total_size/1000:.2f} GB')