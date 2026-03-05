"""Audio extraction from video files using ffmpeg."""
import subprocess
import tempfile
from pathlib import Path
from typing import Tuple, Optional

from ..utils.logger import get_logger

logger = get_logger(__name__)


class AudioExtractor:
    """Extract audio from video files."""

    def __init__(self):
        """Initialize audio extractor."""
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        """Check if ffmpeg is available."""
        try:
            subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "ffmpeg not found. Please install ffmpeg and add it to your PATH.\n"
                "Download from: https://ffmpeg.org/download.html"
            )

    def extract_audio(
        self,
        video_path: Path,
        output_path: Optional[Path] = None
    ) -> Path:
        """Extract audio from video file to WAV format.

        Extracts audio and converts to 16kHz mono WAV, which is the format
        required by Whisper for optimal performance.

        Args:
            video_path: Path to input video file
            output_path: Path for output WAV file. If None, creates temp file

        Returns:
            Path to extracted audio file

        Raises:
            RuntimeError: If extraction fails
        """
        logger.info(f"Extracting audio from {video_path}")

        # Create output path if not specified
        if output_path is None:
            temp_dir = Path(tempfile.gettempdir()) / 'subgen'
            temp_dir.mkdir(parents=True, exist_ok=True)
            output_path = temp_dir / f"{video_path.stem}_audio.wav"

        # Extract audio using ffmpeg
        # -vn: no video
        # -acodec pcm_s16le: 16-bit PCM (uncompressed)
        # -ar 16000: resample to 16kHz (Whisper requirement)
        # -ac 1: mono (1 audio channel)
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # 16-bit PCM
            '-ar', '16000',  # 16kHz sample rate
            '-ac', '1',  # Mono
            '-y',  # Overwrite output file
            str(output_path)
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Audio extracted to {output_path}")
            return output_path

        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to extract audio: {e.stderr}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def get_duration(self, video_path: Path) -> float:
        """Get video duration in seconds.

        Args:
            video_path: Path to video file

        Returns:
            Duration in seconds

        Raises:
            RuntimeError: If duration cannot be determined
        """
        logger.debug(f"Getting duration of {video_path}")

        # Use ffprobe to get duration
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(video_path)
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            duration = float(result.stdout.strip())
            logger.debug(f"Duration: {duration:.2f} seconds")
            return duration

        except (subprocess.CalledProcessError, ValueError) as e:
            error_msg = f"Failed to get video duration: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def get_info(self, video_path: Path) -> dict:
        """Get video information.

        Args:
            video_path: Path to video file

        Returns:
            Dictionary with video information (duration, format, etc.)
        """
        info = {
            'path': str(video_path),
            'size': video_path.stat().st_size,
            'format': video_path.suffix,
        }

        try:
            info['duration'] = self.get_duration(video_path)
        except Exception as e:
            logger.warning(f"Could not get duration: {e}")
            info['duration'] = 0

        return info
