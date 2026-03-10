#!/usr/bin/env python3
"""
Audio transcription to SRT subtitle format using OpenAI Whisper
"""
import whisper
from whisper.utils import get_writer
from pathlib import Path

def transcribe_to_srt(audio_path, model_name="large", output_dir=None):
    """
    Transcribe an audio file and create SRT subtitle file

    Args:
        audio_path: Path to the audio file
        model_name: Whisper model to use (tiny, base, small, medium, large)
        output_dir: Directory to save the output files
    """
    audio_path = Path(audio_path)
    if output_dir is None:
        output_dir = audio_path.parent
    else:
        output_dir = Path(output_dir)

    print(f"Loading Whisper '{model_name}' model...")
    print("(This model is larger and will take time to download on first use)")
    model = whisper.load_model(model_name)

    print(f"\nTranscribing: {audio_path.name}")
    print("This may take a while for large files...\n")

    # Transcribe with word-level timestamps for better subtitles
    result = model.transcribe(
        str(audio_path),
        verbose=True,
        language="he",  # Hebrew
        task="transcribe",
        word_timestamps=True  # Better subtitle timing
    )

    print("\n" + "="*80)
    print("TRANSCRIPTION COMPLETE")
    print("="*80)
    print(f"\nDetected language: {result.get('language', 'unknown')}")

    # Save as SRT subtitle file
    srt_writer = get_writer("srt", str(output_dir))
    srt_writer(result, audio_path.stem)

    srt_path = output_dir / f"{audio_path.stem}.srt"
    print(f"\n✓ SRT subtitle file saved to: {srt_path}")

    # Also save as VTT (alternative YouTube format)
    vtt_writer = get_writer("vtt", str(output_dir))
    vtt_writer(result, audio_path.stem)

    vtt_path = output_dir / f"{audio_path.stem}.vtt"
    print(f"✓ VTT subtitle file saved to: {vtt_path}")

    # Save plain text as well
    txt_writer = get_writer("txt", str(output_dir))
    txt_writer(result, audio_path.stem)

    txt_path = output_dir / f"{audio_path.stem}.txt"
    print(f"✓ Text file saved to: {txt_path}")

    print(f"\nTotal segments: {len(result['segments'])}")
    print(f"\nYou can upload the .srt or .vtt file to YouTube as subtitles!")

    return result

if __name__ == "__main__":
    audio_file = '/Users/dotan.brand/Downloads/===ערוצים 2_mixdown.wav'
    output_directory = '/Users/dotan.brand/Downloads'

    # Using 'large' model for best accuracy with Hebrew
    # Options: tiny, base, small, medium, large
    # 'large' gives the best results but takes longer
    model = "large"

    print("="*80)
    print(f"TRANSCRIBING WITH {model.upper()} MODEL")
    print("This will provide much better accuracy for Hebrew audio")
    print("="*80 + "\n")

    transcribe_to_srt(audio_file, model_name=model, output_dir=output_directory)
