"""SRT subtitle file generation."""
from pathlib import Path
from typing import List, Dict, Any
from datetime import timedelta

from ..utils.logger import get_logger

logger = get_logger(__name__)


class SRTGenerator:
    """Generate SRT subtitle files from transcription segments."""

    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """Format timestamp in SRT format (HH:MM:SS,mmm).

        Args:
            seconds: Time in seconds

        Returns:
            Formatted timestamp string
        """
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((td.total_seconds() % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    @staticmethod
    def create_srt_entry(index: int, start: float, end: float, text: str) -> str:
        """Create a single SRT entry.

        Args:
            index: Subtitle number (1-indexed)
            start: Start time in seconds
            end: End time in seconds
            text: Subtitle text

        Returns:
            Formatted SRT entry
        """
        start_ts = SRTGenerator.format_timestamp(start)
        end_ts = SRTGenerator.format_timestamp(end)

        return f"{index}\n{start_ts} --> {end_ts}\n{text.strip()}\n"

    def generate_srt(
        self,
        segments: List[Dict[str, Any]],
        output_path: Path
    ) -> Path:
        """Generate SRT file from transcription segments.

        Args:
            segments: List of transcription segments with 'start', 'end', 'text'
            output_path: Path for output SRT file

        Returns:
            Path to generated SRT file

        Raises:
            IOError: If file cannot be written
        """
        logger.info(f"Generating SRT file: {output_path}")

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(segments, start=1):
                    start = segment['start']
                    end = segment['end']
                    text = segment['text']

                    entry = self.create_srt_entry(i, start, end, text)
                    f.write(entry)
                    f.write('\n')  # Blank line between entries

            logger.info(f"SRT file created with {len(segments)} subtitles")
            return output_path

        except IOError as e:
            error_msg = f"Failed to write SRT file: {e}"
            logger.error(error_msg)
            raise IOError(error_msg)

    def validate_srt(self, srt_path: Path) -> bool:
        """Validate SRT file format.

        Args:
            srt_path: Path to SRT file

        Returns:
            True if valid SRT format
        """
        try:
            with open(srt_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Basic validation: check for timestamp format
            if '-->' not in content:
                logger.error("Invalid SRT: No timestamp arrows found")
                return False

            # Check for sequential numbering
            lines = content.strip().split('\n')
            entry_numbers = []

            for line in lines:
                line = line.strip()
                if line.isdigit():
                    entry_numbers.append(int(line))

            if not entry_numbers:
                logger.error("Invalid SRT: No entry numbers found")
                return False

            # Check if numbers are sequential starting from 1
            expected = list(range(1, len(entry_numbers) + 1))
            if entry_numbers != expected:
                logger.warning("SRT entry numbers are not sequential")

            logger.info(f"SRT file validated: {len(entry_numbers)} entries")
            return True

        except Exception as e:
            logger.error(f"SRT validation failed: {e}")
            return False
