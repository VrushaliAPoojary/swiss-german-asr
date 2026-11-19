
import csv
import re
import time
import torch
import whisper
from pathlib import Path

TEST_FILE = Path("data/splits/test.csv")
OUTPUT_FILE = Path("baseline_predictions.csv")
CHECKPOINT_INTERVAL = 50

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s']", "", text)
    return " ".join(text.split())

def edit_distance(a, b):
    previous = list(range(len(b) + 1))

    for i, char_a in enumerate(a, 1):
        current = [i]

        for j, char_b in enumerate(b, 1):
            current.append(min(
                current[-1] + 1,
                previous[j] + 1,
                previous[j - 1] + (char_a != char_b)
            ))

        previous = current

    return previous[-1]

def calculate_errors(reference, hypothesis):
    ref_words = normalize(reference).split()
    hyp_words = normalize(hypothesis).split()

    wer_errors = edit_distance(ref_words, hyp_words)
    cer_errors = edit_distance(
        normalize(reference),
        normalize(hypothesis)
    )

    return wer_errors, len(ref_words), cer_errors, len(normalize(reference))

with open(TEST_FILE, encoding="utf-8-sig", newline="") as f:
    test_rows = list(csv.DictReader(f))

device = "cuda" if torch.cuda.is_available() else "cpu"

print("SWISS GERMAN WHISPER BASELINE")
print("=" * 45)
print("Device:", device)

model = whisper.load_model("base", device=device)

predictions = []
total_wer_errors = 0
total_words = 0
total_cer_errors = 0
total_chars = 0
total_time = 0

start_all = time.time()

for index, row in enumerate(test_rows, 1):
    start = time.time()

    result = model.transcribe(
        row["audio_path"],
        language="de",
        task="transcribe",
        fp16=(device == "cuda"),
        verbose=False
    )

    prediction = result["text"].strip()
    elapsed = time.time() - start
    total_time += elapsed

    we, words, ce, chars = calculate_errors(
        row["transcript"], prediction
    )

    total_wer_errors += we
    total_words += words
    total_cer_errors += ce
    total_chars += chars

    predictions.append({
        "audio_path": row["audio_path"],
        "dialect": row["dialect"],
        "reference": row["transcript"],
        "prediction": prediction,
        "wer_errors": we,
        "reference_words": words,
        "cer_errors": ce,
        "reference_characters": chars,
        "inference_seconds": round(elapsed, 3)
    })

    if index % CHECKPOINT_INTERVAL == 0 or index == len(test_rows):
        with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=predictions[0].keys())
            writer.writeheader()
            writer.writerows(predictions)

        print(f"Progress: {index}/{len(test_rows)}")

wer = total_wer_errors / total_words if total_words else 0
cer = total_cer_errors / total_chars if total_chars else 0

print("\n" + "=" * 45)
print("BASELINE RESULTS")
print("=" * 45)
print(f"WER: {wer * 100:.2f}%")
print(f"CER: {cer * 100:.2f}%")
print(f"Total inference time: {total_time / 60:.2f} minutes")
print(f"Average time per audio: {total_time / len(test_rows):.2f} seconds")
print(f"Total elapsed time: {(time.time() - start_all) / 60:.2f} minutes")
print("Predictions saved:", OUTPUT_FILE.resolve())
