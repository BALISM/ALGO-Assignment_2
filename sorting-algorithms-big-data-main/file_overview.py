# ------------------------------------------------------------------ #
#  file_overview.py                                                    #
#  Print the size (MB) of every CSV in data/ and the combined total.   #
# ------------------------------------------------------------------ #

import os

data_folder = './data'
cumulative_mb = 0.0

for entry in sorted(os.listdir(data_folder)):
    if not entry.endswith('.csv'):
        continue
    full_path  = os.path.join(data_folder, entry)
    file_mb    = os.path.getsize(full_path) / 1e6
    cumulative_mb += file_mb
    print(f'{entry}: {file_mb:.1f} MB')

print(f'\nTotal size of all CSVs: {cumulative_mb / 1000:.2f} GB')
