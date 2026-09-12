# Sorting Algorithms on Real-World Big Data

Implementation and empirical benchmarking of three classic O(n²) sorting algorithms — **Bubble Sort**, **Selection Sort**, and **Insertion Sort** — built from scratch and tested against a real-world, multi-gigabyte dataset, to see exactly where and why quadratic-time sorting breaks down at scale.

## Overview

This project benchmarks three from-scratch sorting algorithms on samples drawn from a 24.3-million-row subset of U.S. domestic flight data. It measures runtime across multiple sample sizes and input orderings (random, sorted, reversed), on both a numeric column and a text column, then extrapolates the measured timings to estimate how long a full-scale sort would actually take — and compares that to Python's built-in Timsort.

## Dataset

[Airline Delay and Cancellation Data, 2009–2018](https://www.kaggle.com/datasets/yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018) — U.S. domestic flight records, loaded in chunks via pandas.

This project uses the **2015–2018** yearly files (~24.3M rows), sorting on:
- **ARR_DELAY** (numeric) — arrival delay in minutes
- **OP_CARRIER** (text) — 2-letter airline code

## Project Structure

```
├── check_sizes.py                        # Lists yearly CSV file sizes to help choose which years to use
├── explore_data.py                       # Part A: chunked loading, row counts, column stats
├── sampling.py                           # Part B: draws random samples + random/sorted/reversed variants
├── sort_algorithms.py                    # Part C: bubble_sort, selection_sort, insertion_sort (from scratch)
├── benchmark.py                          # Part D: times all algorithms/sizes/orderings, exports CSV + charts
├── extrapolate.py                        # Part E: full-scale runtime projection (see note below)
├── sort_benchmark_results.csv            # Raw timing results (column, size, ordering, algorithm, time_seconds)
├── chart_runtime_vs_n.png                # Runtime vs n, one line per algorithm (random order)
├── chart_insertion_sort_orderings.png    # Insertion sort: random vs sorted vs reversed
├── Part_F_Written_Analysis.docx          # Written analysis and conclusions
└── data/                                 # Raw yearly CSVs — not tracked in git, download separately
```

> **Note:** `extrapolate.py` currently mirrors `explore_data.py`. The curve-fitting (`time = c × n²`) and full-scale projection shown in the written analysis should be added here for a complete, reproducible pipeline.

## Requirements

- Python 3.9+
- `pandas`, `matplotlib`, `kaggle`

## Setup

```bash
# Clone the repo
git clone https://github.com/<your-username>/sorting-algorithms-big-data.git
cd sorting-algorithms-big-data

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install pandas kaggle matplotlib
```

### Getting the data

1. Create a free Kaggle account and generate an API token (Account → Create New API Token). This downloads `kaggle.json`.
2. Place it at `~/.kaggle/kaggle.json` (macOS/Linux) or `C:\Users\<you>\.kaggle\kaggle.json` (Windows).
3. Download the dataset:
   ```bash
   kaggle datasets download -d yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018 -p ./data --unzip
   ```
4. This project only needs the 2015–2018 files — feel free to remove the others to save space.

## How to Run

```bash
# 1. Check available file sizes before deciding what to load
python check_sizes.py

# 2. Load the data in chunks, get row counts and column stats (Part A)
python explore_data.py

# 3. Sanity-check the sampling logic on a small sample (optional)
python sampling.py

# 4. Run the full benchmark — times every algorithm x size x ordering,
#    writes sort_benchmark_results.csv and both chart PNGs (Part D)
python benchmark.py

# 5. Fit runtime curves and project full-scale runtime (Part E)
python extrapolate.py
```

`benchmark.py` is the longest-running step — bubble sort at n=10,000 alone takes ~9-13 seconds, so the full run across all sizes/orderings/columns takes several minutes. Progress is printed line-by-line as it runs.

## Key Findings

Benchmarked up to n = 10,000, **Selection Sort was fastest** in random order (3.50s) and **Bubble Sort was slowest** (9.47s), consistent with all three being O(n²) on average but with different constants. Insertion Sort showed the widest spread across orderings — 0.0024s sorted vs. 8.08s reversed at n=10,000 — matching its O(n) best case and O(n²) worst case.

Extrapolating to the full 24.3M-row dataset:

| Algorithm | Projected full-scale time |
|---|---|
| Bubble Sort | ~1.78 years |
| Selection Sort | ~239.6 days |
| Insertion Sort | ~281.6 days |
| Python's built-in `sorted()` (Timsort) | ~5.24 seconds |

That's a **speedup of roughly 3.9-10.7 million times** for Timsort over the from-scratch O(n²) implementations — the core reason quadratic sorts are a non-starter at real-world data scale.

## Author

Zoha Ashraf — BS Computer Science, FAST-NUCES