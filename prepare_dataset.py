
import json
import csv
from pathlib import Path

ROOT = Path("data") / "data"
OUTPUT = Path("swissdial_dataset.csv")

DIALECTS = ["ag", "be", "bs", "gr", "lu", "sg", "vs", "zh"]

with open(ROOT / "sentences_ch_de_transcribed.json", encoding="utf-8") as f:
    transcripts = json.load(f)

transcript_map = {item["id"]: item for item in transcripts}

rows = []

for dialect in DIALECTS:
    folder = ROOT / dialect

    for audio in sorted(folder.glob("*.wav")):
        sentence_id = int(audio.stem.split("_")[-1])
        item = transcript_map.get(sentence_id)

        if item is None:
            continue

        text = item.get(f"ch_{dialect}", "").strip()

        if not text:
            continue

        rows.append({
            "audio_path": str(audio.resolve()),
            "sentence_id": sentence_id,
            "dialect": dialect,
            "transcript": text
        })

with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["audio_path", "sentence_id", "dialect", "transcript"]
    )
    writer.writeheader()
    writer.writerows(rows)

print("================================")
print("SWISSDIAL DATASET PREPARATION")
print("================================")
print("Total dataset rows:", len(rows))
print("Output file:", OUTPUT.resolve())
print("\nFirst 3 records:")

for row in rows[:3]:
    print(row)

print("\nDataset CSV created successfully!")
