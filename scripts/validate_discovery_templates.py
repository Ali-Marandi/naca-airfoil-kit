"""Validate the column integrity of reusable discovery and pilot CSV templates."""

import csv
from pathlib import Path


TEMPLATES = (
    Path("templates/problem_discovery_interviews_template.csv"),
    Path("templates/pilot_qualification_scorecard_template.csv"),
)


def validate_template(path: Path) -> tuple[int, int]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if len(rows) < 2:
        raise ValueError(f"{path}: expected a header and at least one template row")
    header = rows[0]
    if not all(header):
        raise ValueError(f"{path}: header contains an empty column name")
    if len(set(header)) != len(header):
        raise ValueError(f"{path}: header contains duplicate column names")
    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(header):
            raise ValueError(
                f"{path}: row {row_number} has {len(row)} columns; expected {len(header)}"
            )
    return len(rows) - 1, len(header)


def main() -> None:
    for template in TEMPLATES:
        row_count, column_count = validate_template(template)
        print(f"{template}: {row_count} template rows; {column_count} columns; valid")


if __name__ == "__main__":
    main()
