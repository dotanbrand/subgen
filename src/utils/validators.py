"""Input validation utilities."""
from pathlib import Path
from typing import List


# Supported video formats
SUPPORTED_VIDEO_FORMATS = [
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
    '.m4v', '.mpg', '.mpeg', '.3gp', '.ts'
]


def is_valid_video_file(path: Path) -> bool:
    """Check if file is a valid video file.

    Args:
        path: File path to check

    Returns:
        True if valid video file
    """
    if not path.exists():
        return False

    if not path.is_file():
        return False

    return path.suffix.lower() in SUPPORTED_VIDEO_FORMATS


def validate_video_file(path: Path) -> str:
    """Validate video file and return error message if invalid.

    Args:
        path: Video file path

    Returns:
        Error message if invalid, empty string if valid
    """
    if not path.exists():
        return "File does not exist"

    if not path.is_file():
        return "Path is not a file"

    if not is_valid_video_file(path):
        ext = path.suffix or "no extension"
        return f"Unsupported video format: {ext}\nSupported formats: {', '.join(SUPPORTED_VIDEO_FORMATS)}"

    return ""


def validate_output_directory(path: Path) -> str:
    """Validate output directory and return error message if invalid.

    Args:
        path: Output directory path

    Returns:
        Error message if invalid, empty string if valid
    """
    if path.exists() and not path.is_dir():
        return "Path exists but is not a directory"

    # Try to create directory
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return f"Cannot create output directory: {e}"

    # Check write permissions
    if not os.access(path, os.W_OK):
        return "No write permission for output directory"

    return ""


import os
