
import wave
from pathlib import Path

ROOT = Path("data") / "data"
DIALECTS = ["ag", "be", "bs", "gr", "lu", "sg", "vs", "zh"]

print("=" * 50)
print("SWISSDIAL AUDIO PROPERTY CHECK")
print("=" * 50)

for dialect in DIALECTS:
    audio = ROOT / dialect / f"ch_{dialect}_0000.wav"

    if not audio.exists():
        print(f"{dialect.upper()}: Sample not found")
        continue

    try:
        with wave.open(str(audio), "rb") as wav:
            channels = wav.getnchannels()
            sample_rate = wav.getframerate()
            sample_width = wav.getsampwidth()
            frames = wav.getnframes()
            duration = frames / sample_rate

            print(f"\n{dialect.upper()}:")
            print("Channels:", channels)
            print("Sample rate:", sample_rate, "Hz")
            print("Bit depth:", sample_width * 8, "bits")
            print("Duration:", round(duration, 2), "seconds")

    except Exception as error:
        print(f"{dialect.upper()}: ERROR - {error}")

print("\nAudio inspection completed.")
