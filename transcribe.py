
import torch
import whisper
from pathlib import Path

print("================================")
print("SWISS GERMAN AUDIO TRANSCRIPTION")
print("================================")

# Audio file location
audio_file = Path("sample_swiss_german.wav")

# Check whether the audio file exists
if not audio_file.exists():
    raise FileNotFoundError(
        "Audio file not found! Place sample_swiss_german.wav "
        "inside the project folder."
    )

# Select GPU or CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print("\nSelected device:", device)

# Load Whisper Base
print("\nLoading Whisper Base model...")
model = whisper.load_model("base", device=device)

print("\nTranscribing audio...")

# Convert speech into text
result = model.transcribe(
    str(audio_file),
    task="transcribe"
)

# Display results
print("\n================================")
print("TRANSCRIPTION RESULT")
print("================================")

print("Detected language:", result["language"])
print("\nRecognized speech:")
print(result["text"])

print("\n================================")
print("TRANSCRIPTION COMPLETED")
print("================================")
