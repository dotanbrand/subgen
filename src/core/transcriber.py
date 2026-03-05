"""Whisper transcription with CPU optimization."""
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable

from faster_whisper import WhisperModel

from ..utils.logger import get_logger

logger = get_logger(__name__)


class Transcriber:
    """Transcribe audio using faster-whisper with CPU optimization."""

    def __init__(
        self,
        model_size: str = "base",
        models_dir: Optional[Path] = None,
        cpu_threads: Optional[int] = None
    ):
        """Initialize transcriber.

        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            models_dir: Directory containing downloaded models
            cpu_threads: Number of CPU threads to use (default: all cores)
        """
        self.model_size = model_size
        self.models_dir = models_dir
        self.cpu_threads = cpu_threads or os.cpu_count() or 4
        self.model: Optional[WhisperModel] = None

        logger.info(f"Transcriber initialized with model={model_size}, threads={self.cpu_threads}")

    def load_model(self):
        """Load Whisper model with CPU optimization.

        Raises:
            RuntimeError: If model cannot be loaded
        """
        logger.info(f"Loading {self.model_size} model...")

        try:
            # CPU-optimized configuration
            self.model = WhisperModel(
                self.model_size,
                device="cpu",
                compute_type="int8",  # 8-bit quantization for speed
                cpu_threads=self.cpu_threads,
                num_workers=1,  # Avoid thrashing on modest hardware
                download_root=str(self.models_dir) if self.models_dir else None
            )

            logger.info("Model loaded successfully")

        except Exception as e:
            error_msg = f"Failed to load model: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def transcribe(
        self,
        audio_path: Path,
        language: Optional[str] = None,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> List[Dict[str, Any]]:
        """Transcribe audio file.

        Args:
            audio_path: Path to audio file (WAV, 16kHz mono)
            language: Language code (e.g., 'en', 'es'). None for auto-detect
            progress_callback: Optional callback function(progress: float, message: str)

        Returns:
            List of segment dictionaries with 'start', 'end', 'text' keys

        Raises:
            RuntimeError: If transcription fails
        """
        if self.model is None:
            self.load_model()

        logger.info(f"Transcribing {audio_path}")
        if language:
            logger.info(f"Language: {language}")
        else:
            logger.info("Language: auto-detect")

        try:
            # Transcribe with CPU-optimized settings
            segments, info = self.model.transcribe(
                str(audio_path),
                language=language if language != "auto" else None,
                beam_size=5,  # Balance between accuracy and speed
                vad_filter=True,  # Skip silence (20-30% faster)
                vad_parameters=dict(
                    threshold=0.5,
                    min_speech_duration_ms=250,
                    min_silence_duration_ms=2000
                ),
                word_timestamps=False,  # Faster, not needed for SRT
                condition_on_previous_text=True,  # Better accuracy
            )

            # Log detected language
            logger.info(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")

            # Convert segments to list
            result_segments = []
            total_duration = info.duration if hasattr(info, 'duration') else 0

            for i, segment in enumerate(segments):
                result_segments.append({
                    'start': segment.start,
                    'end': segment.end,
                    'text': segment.text
                })

                # Report progress
                if progress_callback and total_duration > 0:
                    progress = min((segment.end / total_duration) * 100, 100)
                    progress_callback(progress, f"Processing: {self._format_time(segment.end)}")

            logger.info(f"Transcription complete: {len(result_segments)} segments")
            return result_segments

        except Exception as e:
            error_msg = f"Transcription failed: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def _format_time(self, seconds: float) -> str:
        """Format time in MM:SS format.

        Args:
            seconds: Time in seconds

        Returns:
            Formatted time string
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes.

        Returns:
            List of language codes
        """
        # Whisper supported languages
        return [
            'auto',  # Auto-detect
            'en', 'es', 'fr', 'de', 'it', 'pt', 'nl', 'ru', 'zh', 'ja',
            'ko', 'ar', 'hi', 'tr', 'pl', 'uk', 'vi', 'sv', 'no', 'da',
            'fi', 'he', 'th', 'id', 'ms', 'cs', 'ro', 'hu', 'el', 'bg',
        ]
