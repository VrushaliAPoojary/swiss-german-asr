
import subprocess
from pathlib import Path

ROOT = Path("data") / "data"
OUTPUT = Path("data") / "converted"
DIALECTS = ["ag", "be", "bs", "gr", "lu", "sg", "vs", "zh"]

total = 0
failed = []

print("SWISSDIAL AUDIO CONVERSION")
print("=" * 45)

for dialect in DIALECTS:
    source_folder = ROOT / dialect
    output_folder = OUTPUT / dialect
    output_folder.mkdir(parents=True, exist_ok=True)

    files = sorted(source_folder.glob("*.wav"))
    print(f"\nConverting {dialect.upper()}: {len(files)} files")

    for index, audio in enumerate(files, 1):
        destination = output_folder / audio.name

        result = subprocess.run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-i", str(audio),
                "-ar", "16000",
                "-ac", "1",
                "-c:a", "pcm_s16le",
                str(destination)
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            total += 1
        else:
            failed.append(str(audio))
        
        if index % 250 == 0 or index == len(files):
            print(f"  Progress: {index}/{len(files)}")

print("\n" + "=" * 45)
print("CONVERSION FINISHED")
print("Successfully converted:", total)
print("Failed:", len(failed))
print("Output folder:", OUTPUT.resolve())

if failed:
    print("\nFirst failed files:")
    for file in failed[:10]:
        print(file)
