#!/usr/bin/env python3
"""
Test transcription with 3-minute clip
"""
import whisper
from whisper.utils import get_writer
from pathlib import Path

audio_file = '/Users/dotan.brand/Downloads/test_3min.wav'
output_dir = '/Users/dotan.brand/Downloads'
model_name = "large"

print(f"Loading Whisper '{model_name}' model...")
print("(First time will download ~3GB model)\n")
model = whisper.load_model(model_name)

print(f"Transcribing 3-minute test clip...")
print("This should take 2-5 minutes...\n")

result = model.transcribe(
    audio_file,
    verbose=True,
    language="he",
    task="transcribe",
    word_timestamps=True
)

print("\n" + "="*80)
print("TEST TRANSCRIPTION COMPLETE")
print("="*80)

# Save as SRT
srt_writer = get_writer("srt", output_dir)
srt_writer(result, "test_3min")
print(f"\n✓ SRT: {output_dir}/test_3min.srt")

# Save as text
txt_writer = get_writer("txt", output_dir)
txt_writer(result, "test_3min")
print(f"✓ TXT: {output_dir}/test_3min.txt")

print(f"\n✓ Total segments: {len(result['segments'])}")
print("\nReview the quality and let me know if you want to process the full file!")
