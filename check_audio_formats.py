
import subprocess
import json
from pathlib import Path
from collections import Counter

ROOT = Path("data") / "data"
DIALECTS = ["ag", "be", "bs", "gr", "lu", "sg", "vs", "zh"]

print("SWISSDIAL AUDIO FORMAT INSPECTION")
print("=" * 45)

for dialect in DIALECTS:
    folder = ROOT / dialect
    files = sorted(folder.glob("*.wav"))

    formats = Counter()

    for audio in files:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "a:0",
                "-show_entries",
                "stream=codec_name,sample_rate,channels,bits_per_sample",
                "-of", "json",
                str(audio)
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            info = json.loads(result.stdout)
            if info.get("streams"):
                stream = info["streams"][0]
                key = (
                    stream.get("codec_name"),
                    stream.get("sample_rate"),
                    stream.get("channels"),
                    stream.get("bits_per_sample")
                )
                formats[key] += 1
            else:
                formats["No audio stream"] += 1
        else:
            formats["Error"] += 1

    print(f"\n{dialect.upper()} - {len(files)} files")
    for audio_format, count in formats.items():
        print(audio_format, ":", count)

print("\nInspection completed.")
