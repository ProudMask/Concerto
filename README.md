# Concerto: Random Note and Rhythm Generator

A small reproducible Python randomness example that generates note spellings and duration fractions. The historical project name is retained; output is a list of symbolic sequences, not a complete composed concerto or audio recording.

## Run

Python 3.10 or later; no third-party packages required:

```bash
python main.py --count 3 --length 5 --seed 42
python main.py --count 3 --length 5 --seed 42 --output outputs/example.json
python -m unittest discover -s tests -v
```

Both generation commands produce the same sequences on the same Python runtime. A seed fixes the pseudorandom stream; omitting it produces an unseeded run. Existing output files are rejected. JSON records the seed, generator version, configuration, generated sequences, note/rhythm counts, and exact total durations as fractions of a whole note. It contains 15 events for this example.

## Python API

```python
from main import create_multiple_concertos

sequences = create_multiple_concertos(3, 5, seed=42)
assert sequences == create_multiple_concertos(3, 5, seed=42)
```

The existing create_concerto and note/rhythm helper names remain available. An optional local random.Random instance can be passed to the helpers. Importing the module does not generate or print examples. Generation does not reseed or consume Python's global pseudorandom generator.

## Sampling assumptions

Each event independently samples a note letter from A–G, an accidental from natural/sharp/flat, and a duration from `1/4`, `1/8`, `1/16`, `3/8`, using equal selection weights. Durations are fractions of a whole note, not seconds; no tempo is specified. A sequence can end mid-bar because there is no meter constraint.

The 21 possible note spellings are not 21 distinct pitch classes: enharmonic equivalents occur, so uniform spelling choices do not imply uniform pitches. There are no octaves, harmony, key, rests, or instruments. Random output is not guaranteed to be unique, dissonant, or musically pleasing. Summary frequencies describe one realization and are not statistical evidence of generator quality.

Counts and lengths must be positive integers, with at most 100000 total events. Exact sequence reproduction across different Python versions is not promised; record the runtime version for comparisons.

## Verification and next step

Tests cover seed reproducibility, isolation from global RNG state, input limits, summary reconciliation, exact duration accounting, CLI file protection, and silent imports. This is a procedural baseline, not generative AI or a trained music model. A future modeling extension would require a licensed symbolic-music dataset, a defined prediction task, held-out evaluation, and comparison against this random baseline.
