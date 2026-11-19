
import json
from pathlib import Path

# Dataset location
ROOT = Path("data") / "data"

DIALECTS = ["ag", "be", "bs", "gr", "lu", "sg", "vs", "zh"]

NUMERICS_FILE = ROOT / "sentences_ch_de_numerics.json"
TRANSCRIBED_FILE = ROOT / "sentences_ch_de_transcribed.json"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    print("=" * 55)
    print("SWISSDIAL DATASET INSPECTION")
    print("=" * 55)

    # Check dataset files
    for file_path in [NUMERICS_FILE, TRANSCRIBED_FILE]:
        if not file_path.exists():
            raise FileNotFoundError(f"Missing dataset file: {file_path}")

    numerics = load_json(NUMERICS_FILE)
    transcripts = load_json(TRANSCRIBED_FILE)

    print("\n1. TRANSCRIPT INFORMATION")
    print("-" * 55)
    print("Numerics entries:", len(numerics))
    print("Transcribed entries:", len(transcripts))
    print("First sentence:", transcripts[0])

    # Build transcript lookup using sentence IDs
    transcript_by_id = {
        item["id"]: item for item in transcripts
    }
    transcript_ids = set(transcript_by_id.keys())

    print("\n2. AUDIO FILE COUNTS")
    print("-" * 55)

    total_audio = 0
    total_matched = 0
    total_unmatched = 0

    for dialect in DIALECTS:
        folder = ROOT / dialect

        if not folder.exists():
            print(f"{dialect.upper()}: FOLDER MISSING")
            continue

        audio_files = sorted(folder.glob("*.wav"))

        matched = 0
        unmatched = 0

        for audio in audio_files:
            try:
                sentence_id = int(audio.stem.split("_")[-1])
                if sentence_id in transcript_ids:
                    matched += 1
                else:
                    unmatched += 1
            except ValueError:
                unmatched += 1

        total_audio += len(audio_files)
        total_matched += matched
        total_unmatched += unmatched

        print(f"\n{dialect.upper()} dialect:")
        print("  Audio files:", len(audio_files))
        print("  Matched IDs:", matched)
        print("  Unmatched IDs:", unmatched)

    print("\n3. OVERALL RESULTS")
    print("-" * 55)
    print("Total audio files:", total_audio)
    print("Total matched:", total_matched)
    print("Total unmatched:", total_unmatched)
    print("Unique transcript IDs:", len(transcript_ids))

    print("\n4. SAMPLE AUDIO-TRANSCRIPT PAIR")
    print("-" * 55)

    sample_id = 0
    sample = transcript_by_id.get(sample_id)

    if sample:
        audio = ROOT / "ag" / "ch_ag_0000.wav"

        print("Audio:", audio)
        print("Audio exists:", audio.exists())
        print("Sentence ID:", sample_id)
        print("Aargau transcript:", sample["ch_ag"])
        print("High German reference:", sample["de"])

    print("\n" + "=" * 55)
    print("DATASET INSPECTION COMPLETED")
    print("=" * 55)


if __name__ == "__main__":
    main()
