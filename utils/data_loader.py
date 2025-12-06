import json
import csv


def load_users_from_json(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_invalid_logins_from_csv(path: str):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows
