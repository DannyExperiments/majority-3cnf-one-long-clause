# Reproducibility

Run the exact finite verification with Python 3.11 or later. It uses only the standard library.

    python3 -I scripts/verify_repository.py
    python3 -I verification/src/replay.py

The replay enumerates independent sets in 127 prescribed-count graphs and 76 small twin-replacement graphs. It checks the maximum-size coefficient against direct model counts for 32 formulas and checks 128 threshold decisions. It then counts the actual selector formulas for below-threshold, tied and above-threshold joins, and checks four empty or isolated cases. [Recorded results](verification/results/replay.txt).

Open the HTML in the offline explorer ZIP to rotate the graph, choose diagonals and enumerate its independent sets. See the [visualization notes](visualization/README.md) and [paper build instructions](paper/BUILD.md).
