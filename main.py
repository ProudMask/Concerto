"""Reproducible random note/rhythm sequences; no trained music model."""
import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import random

NOTES = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
ACCIDENTALS = ('', '#', 'b')
RHYTHMS = ('1/4', '1/8', '1/16', '3/8')
MAX_EVENTS = 100000


def positive_integer(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f'{name} must be a positive integer')


def generate_random_note(rng=None):
    rng = rng if rng is not None else random.SystemRandom()
    return rng.choice(NOTES) + rng.choice(ACCIDENTALS)


def generate_uncomfortable_rhythm(rng=None):
    """Historical name: samples duration fractions without judging musical quality."""
    rng = rng if rng is not None else random.SystemRandom()
    return rng.choice(RHYTHMS)


def create_concerto(length, rng=None):
    positive_integer(length, 'length')
    if length > MAX_EVENTS:
        raise ValueError(f'At most {MAX_EVENTS} events are supported')
    rng = rng if rng is not None else random.Random()
    return [f'{generate_random_note(rng)} ({generate_uncomfortable_rhythm(rng)})' for _ in range(length)]


def create_multiple_concertos(number_of_concertos, length_of_each, seed=None):
    positive_integer(number_of_concertos, 'number_of_concertos')
    positive_integer(length_of_each, 'length_of_each')
    if number_of_concertos * length_of_each > MAX_EVENTS:
        raise ValueError(f'At most {MAX_EVENTS} total events are supported')
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise ValueError('seed must be an integer or None')
    rng = random.Random(seed)
    return [create_concerto(length_of_each, rng) for _ in range(number_of_concertos)]


def build_report(count, length, seed=None):
    sequences = create_multiple_concertos(count, length, seed)
    notes, rhythms, durations = Counter(), Counter(), []
    for sequence in sequences:
        total = Fraction(0)
        for event in sequence:
            note, rhythm = event.split(' ')
            rhythm = rhythm.strip('()')
            notes[note] += 1
            rhythms[rhythm] += 1
            total += Fraction(rhythm)
        durations.append(str(total))
    return {'generator_version': 1, 'config': {'count': count, 'length': length, 'seed': seed}, 'sequences': sequences, 'summary': {'event_count': count * length, 'note_spelling_counts': dict(sorted(notes.items())), 'rhythm_counts': dict(sorted(rhythms.items())), 'sequence_durations_whole_notes': durations}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--count', type=int, default=3)
    parser.add_argument('--length', type=int, default=5)
    parser.add_argument('--seed', type=int)
    parser.add_argument('--output', type=Path, help='Optional new JSON output file')
    args = parser.parse_args()
    try:
        report = build_report(args.count, args.length, args.seed)
        serialized = json.dumps(report, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open('x', encoding='utf-8') as handle:
                handle.write(serialized + '\n')
        else:
            print(serialized)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
