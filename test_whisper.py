
import torch
import whisper

print("================================")
print("SWISS GERMAN ASR - WHISPER TEST")
print("================================")

# Check whether GPU is available
if torch.cuda.is_available():
    device = "cuda"
    print("GPU detected:", torch.cuda.get_device_name(0))
else:
    device = "cpu"
    print("GPU not detected. Using CPU.")

# Load Whisper Base model
print("\nLoading Whisper Base model...")

model = whisper.load_model("base", device=device)

print("\nWhisper model loaded successfully!")

# Display selected device
print("Selected device:", device)

# Display GPU memory usage
if device == "cuda":
    memory = torch.cuda.memory_allocated(0) / (1024 ** 2)
    print(f"GPU memory allocated: {memory:.2f} MB")

print("\nWhisper test completed successfully!")
