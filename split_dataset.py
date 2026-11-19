
import csv
import random
from pathlib import Path

INPUT = Path("swissdial_dataset.csv")
OUTPUT = Path("data") / "splits"

random.seed(42)

with open(INPUT, "r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

# Split unique sentence IDs to prevent data leakage
sentence_ids = sorted({int(row["sentence_id"]) for row in rows})
random.shuffle(sentence_ids)

total = len(sentence_ids)
train_end = int(total * 0.80)
val_end = int(total * 0.90)

train_ids = set(sentence_ids[:train_end])
val_ids = set(sentence_ids[train_end:val_end])
test_ids = set(sentence_ids[val_end:])

splits = {
    "train": [],
    "validation": [],
    "test": []
}

for row in rows:
    sentence_id = int(row["sentence_id"])

    # Use converted audio, not original audio
    original = Path(row["audio_path"])
    dialect = row["dialect"]
    converted = Path("data") / "converted" / dialect / original.name

    if not converted.exists():
        raise FileNotFoundError(f"Missing converted audio: {converted}")

    row["audio_path"] = str(converted.resolve())

    if sentence_id in train_ids:
        splits["train"].append(row)
    elif sentence_id in val_ids:
        splits["validation"].append(row)
    else:
        splits["test"].append(row)

OUTPUT.mkdir(parents=True, exist_ok=True)

for name, split_rows in splits.items():
    output_file = OUTPUT / f"{name}.csv"

    with open(output_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(split_rows)

    print(f"{name}: {len(split_rows)} audio records")

print("\nUnique sentence IDs:", total)
print("Training IDs:", len(train_ids))
print("Validation IDs:", len(val_ids))
print("Testing IDs:", len(test_ids))
print("\nDataset splits created successfully!")
print("Location:", OUTPUT.resolve())
