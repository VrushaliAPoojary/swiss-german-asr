
import wave
from pathlib import Path

ROOT = Path("data") / "converted"
DIALECTS = ["ag", "be", "bs", "gr", "lu", "sg", "vs", "zh"]

total = 0
valid = 0
invalid = []

print("CONVERTED AUDIO VERIFICATION")
print("=" * 45)

for dialect in DIALECTS:
    files = sorted((ROOT / dialect).glob("*.wav"))
    dialect_valid = 0

    for audio in files:
        total += 1
        try:
            with wave.open(str(audio), "rb") as wav:
                correct = (
                    wav.getframerate() == 16000
                    and wav.getnchannels() == 1
                    and wav.getsampwidth() == 2
                )

                if correct:
                    valid += 1
                    dialect_valid += 1
                else:
                    invalid.append(str(audio))

        except Exception as error:
            invalid.append(f"{audio}: {error}")

    print(f"{dialect.upper()}: {dialect_valid}/{len(files)} valid")

print("\nTotal files:", total)
print("Valid files:", valid)
print("Invalid files:", len(invalid))

if invalid:
    print("\nFirst 10 problems:")
    for item in invalid[:10]:
        print(item)

print("\nVerification completed.")
