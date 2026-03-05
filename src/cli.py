#!/usr/bin/env python3
"""Simple CLI for testing SubGen core functionality."""
import argparse
import sys
from pathlib import Path

from core import AudioExtractor, SRTGenerator, Transcriber, Config
from utils import (
    setup_logger,
    get_logger,
    validate_video_file,
    get_output_path,
    clean_temp_file
)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="SubGen - Generate subtitles from video files"
    )
    parser.add_argument(
        "video",
        type=Path,
        help="Path to video file"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output SRT file path (default: same as video)"
    )
    parser.add_argument(
        "-m", "--model",
        default="base",
        choices=['tiny', 'base', 'small', 'medium'],
        help="Whisper model size (default: base)"
    )
    parser.add_argument(
        "-l", "--language",
        help="Language code (e.g., 'en', 'es'). Auto-detect if not specified"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    import logging
    setup_logger(level=getattr(logging, log_level))
    logger = get_logger(__name__)

    # Load config
    config = Config()

    # Validate input
    video_path = args.video
    error = validate_video_file(video_path)
    if error:
        logger.error(f"Invalid video file: {error}")
        sys.exit(1)

    # Determine output path
    output_path = args.output
    if output_path is None:
        output_path = get_output_path(video_path)

    logger.info("=" * 60)
    logger.info("SubGen - Subtitle Generator")
    logger.info("=" * 60)
    logger.info(f"Video: {video_path}")
    logger.info(f"Output: {output_path}")
    logger.info(f"Model: {args.model}")
    logger.info(f"Language: {args.language or 'auto-detect'}")
    logger.info("=" * 60)

    temp_audio_path = None

    try:
        # Step 1: Extract audio
        logger.info("Step 1/3: Extracting audio from video...")
        extractor = AudioExtractor()
        temp_audio_path = extractor.extract_audio(video_path)
        logger.info(f"Audio extracted: {temp_audio_path}")

        # Get video info
        duration = extractor.get_duration(video_path)
        logger.info(f"Video duration: {duration:.2f} seconds")

        # Step 2: Transcribe
        logger.info("Step 2/3: Transcribing audio (this may take a while)...")
        transcriber = Transcriber(
            model_size=args.model,
            models_dir=config.models_directory,
            cpu_threads=config.cpu_threads
        )

        def progress_callback(progress: float, message: str):
            """Progress callback."""
            logger.info(f"Progress: {progress:.1f}% - {message}")

        segments = transcriber.transcribe(
            temp_audio_path,
            language=args.language,
            progress_callback=progress_callback
        )

        logger.info(f"Transcription complete: {len(segments)} segments")

        # Step 3: Generate SRT
        logger.info("Step 3/3: Generating SRT file...")
        generator = SRTGenerator()
        output_path = generator.generate_srt(segments, output_path)

        # Validate
        if generator.validate_srt(output_path):
            logger.info("=" * 60)
            logger.info(f"✓ Subtitles generated successfully!")
            logger.info(f"✓ Output: {output_path}")
            logger.info("=" * 60)
        else:
            logger.warning("SRT file may have formatting issues")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.verbose)
        sys.exit(1)

    finally:
        # Clean up temporary audio file
        if temp_audio_path:
            logger.debug(f"Cleaning up: {temp_audio_path}")
            clean_temp_file(temp_audio_path)


if __name__ == "__main__":
    main()
