"""File operation utilities."""
import os
from pathlib import Path
from typing import Optional


def get_output_path(video_path: Path, output_dir: Optional[Path] = None) -> Path:
    """Get output SRT file path based on video file.

    Args:
        video_path: Input video file path
        output_dir: Output directory. If None, uses video's directory

    Returns:
        Output SRT file path
    """
    if output_dir is None:
        output_dir = video_path.parent

    # Change extension to .srt
    srt_filename = video_path.stem + '.srt'
    return output_dir / srt_filename


def ensure_directory(path: Path):
    """Ensure directory exists.

    Args:
        path: Directory path
    """
    path.mkdir(parents=True, exist_ok=True)


def get_file_size(path: Path) -> int:
    """Get file size in bytes.

    Args:
        path: File path

    Returns:
        File size in bytes
    """
    return path.stat().st_size


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def get_available_space(path: Path) -> int:
    """Get available disk space in bytes.

    Args:
        path: Path to check

    Returns:
        Available space in bytes
    """
    stat = os.statvfs(path) if hasattr(os, 'statvfs') else None
    if stat:
        return stat.f_bavail * stat.f_frsize

    # Fallback for Windows
    import shutil
    return shutil.disk_usage(path).free


def clean_temp_file(path: Path):
    """Safely remove temporary file.

    Args:
        path: File path to remove
    """
    try:
        if path.exists():
            path.unlink()
    except Exception as e:
        print(f"Warning: Could not delete temp file {path}: {e}")
