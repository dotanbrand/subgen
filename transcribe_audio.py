#!/usr/bin/env python3
"""
Simple audio transcription script using OpenAI Whisper
"""
import whisper
import sys
from pathlib import Path

def transcribe_audio(audio_path, model_name="base", output_path=None):
    """
    Transcribe an audio file using Whisper

    Args:
        audio_path: Path to the audio file
        model_name: Whisper model to use (tiny, base, small, medium, large)
        output_path: Optional path to save the transcription
    """
    print(f"Loading Whisper '{model_name}' model...")
    model = whisper.load_model(model_name)

    print(f"Transcribing: {audio_path}")
    print("This may take a while depending on the file size...")

    # Transcribe with options for better accuracy
    result = model.transcribe(
        str(audio_path),
        verbose=True,
        language="he",  # Hebrew
        task="transcribe"
    )

    # Print results
    print("\n" + "="*80)
    print("TRANSCRIPTION COMPLETE")
    print("="*80)
    print(f"\nDetected language: {result.get('language', 'unknown')}")
    print(f"\nTranscription:\n{result['text']}")

    # Save to file if output path provided
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Language: {result.get('language', 'unknown')}\n\n")
            f.write(result['text'])
        print(f"\n✓ Transcription saved to: {output_path}")

    return result

if __name__ == "__main__":
    audio_file = '/Users/dotan.brand/Downloads/===ערוצים 2_mixdown.wav'
    output_file = '/Users/dotan.brand/Downloads/transcription.txt'

    # You can change the model here: tiny, base, small, medium, large
    model = "base"

    transcribe_audio(audio_file, model_name=model, output_path=output_file)
