from fractions import Fraction
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from main import build_report, create_multiple_concertos


class GeneratorTests(unittest.TestCase):
    def test_reproducibility_and_shape(self):
        first = create_multiple_concertos(3, 5, seed=42)
        self.assertEqual(first, create_multiple_concertos(3, 5, seed=42))
        self.assertEqual([len(sequence) for sequence in first], [5, 5, 5])

    def test_global_rng_unchanged(self):
        state = random.getstate()
        create_multiple_concertos(3, 5, seed=42)
        self.assertEqual(state, random.getstate())

    def test_invalid_parameters(self):
        for count, length in ((0, 5), (1, -1), (True, 5), (1.5, 3), (1000, 1000)):
            with self.assertRaises(ValueError):
                create_multiple_concertos(count, length)
        with self.assertRaises(ValueError):
            create_multiple_concertos(1, 1, seed='42')

    def test_summary_reconciles(self):
        report = build_report(3, 5, 42)
        self.assertEqual(sum(report['summary']['note_spelling_counts'].values()), 15)
        self.assertEqual(sum(report['summary']['rhythm_counts'].values()), 15)
        for sequence, duration in zip(report['sequences'], report['summary']['sequence_durations_whole_notes']):
            expected = sum((Fraction(event.split('(')[1].rstrip(')')) for event in sequence), Fraction(0))
            self.assertEqual(Fraction(duration), expected)

    def test_cli_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'example.json'
            command = [sys.executable, 'main.py', '--seed', '42', '--output', str(output)]
            subprocess.run(command, capture_output=True, text=True, check=True, timeout=10)
            self.assertEqual(json.loads(output.read_text())['summary']['event_count'], 15)
            before = output.read_bytes()
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_bytes(), before)

    def test_import_is_silent(self):
        result = subprocess.run([sys.executable, '-c', 'import main'], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
