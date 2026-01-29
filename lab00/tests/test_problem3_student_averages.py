import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import csv
import pathlib
from src.problem3_student_averages import compute_student_averages

DATA = pathlib.Path(__file__).resolve().parents[1] / "data"

def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.reader(f))

def test_compute_student_averages(tmp_path):
    input_csv = DATA / "students_scores.csv"
    out_csv = tmp_path / "out.csv"
    compute_student_averages(str(input_csv), str(out_csv))

    rows = read_csv(out_csv)
    expected = [
        ["student_id", "average_score"],
        ["s004", "100.00"],
        ["s001", "91.00"],
        ["s002", "88.00"],
        ["s003", "75.00"],
        ["s005", "66.67"],
    ]
    assert rows == expected
