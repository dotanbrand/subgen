"""Whisper model downloading and management."""
import os
from pathlib import Path
from typing import Optional, Callable, Dict, List
from huggingface_hub import snapshot_download, hf_hub_download
import shutil

from ..utils.logger import get_logger
from ..utils.file_utils import format_size, get_file_size

logger = get_logger(__name__)


class ModelDownloader:
    """Download and manage Whisper models."""

    # Model repository on Hugging Face
    REPO_PREFIX = "guillaumekln/faster-whisper"

    # Available models with metadata
    MODELS = {
        'tiny': {'size': '75 MB', 'size_bytes': 75 * 1024 * 1024},
        'tiny.en': {'size': '75 MB', 'size_bytes': 75 * 1024 * 1024},
        'base': {'size': '145 MB', 'size_bytes': 145 * 1024 * 1024},
        'base.en': {'size': '145 MB', 'size_bytes': 145 * 1024 * 1024},
        'small': {'size': '466 MB', 'size_bytes': 466 * 1024 * 1024},
        'small.en': {'size': '466 MB', 'size_bytes': 466 * 1024 * 1024},
        'medium': {'size': '1.5 GB', 'size_bytes': 1536 * 1024 * 1024},
        'medium.en': {'size': '1.5 GB', 'size_bytes': 1536 * 1024 * 1024},
    }

    def __init__(self, models_dir: Path):
        """Initialize model downloader.

        Args:
            models_dir: Directory to store downloaded models
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Model downloader initialized: {self.models_dir}")

    def is_model_downloaded(self, model_size: str) -> bool:
        """Check if model is already downloaded.

        Args:
            model_size: Model size (e.g., 'base', 'small')

        Returns:
            True if model exists locally
        """
        model_path = self.models_dir / f"faster-whisper-{model_size}"
        return model_path.exists()

    def get_downloaded_models(self) -> List[str]:
        """Get list of downloaded models.

        Returns:
            List of model names
        """
        downloaded = []
        for model_name in self.MODELS.keys():
            if self.is_model_downloaded(model_name):
                downloaded.append(model_name)
        return downloaded

    def download_model(
        self,
        model_size: str,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> Path:
        """Download Whisper model from Hugging Face.

        Args:
            model_size: Model size (e.g., 'base', 'small')
            progress_callback: Optional callback(downloaded_bytes, total_bytes, status)

        Returns:
            Path to downloaded model directory

        Raises:
            ValueError: If model size is invalid
            RuntimeError: If download fails
        """
        if model_size not in self.MODELS:
            raise ValueError(f"Invalid model size: {model_size}")

        if self.is_model_downloaded(model_size):
            logger.info(f"Model {model_size} already downloaded")
            return self.models_dir / f"faster-whisper-{model_size}"

        logger.info(f"Downloading model: {model_size}")

        repo_id = f"{self.REPO_PREFIX}-{model_size}"
        local_dir = self.models_dir / f"faster-whisper-{model_size}"

        try:
            # Download model
            if progress_callback:
                progress_callback(0, 100, f"Starting download: {model_size}")

            snapshot_download(
                repo_id=repo_id,
                local_dir=str(local_dir),
                local_dir_use_symlinks=False
            )

            if progress_callback:
                progress_callback(100, 100, "Download complete")

            logger.info(f"Model {model_size} downloaded successfully")
            return local_dir

        except Exception as e:
            error_msg = f"Failed to download model {model_size}: {e}"
            logger.error(error_msg)

            # Clean up partial download
            if local_dir.exists():
                shutil.rmtree(local_dir, ignore_errors=True)

            raise RuntimeError(error_msg)

    def delete_model(self, model_size: str):
        """Delete downloaded model.

        Args:
            model_size: Model size to delete

        Raises:
            ValueError: If model doesn't exist
        """
        if not self.is_model_downloaded(model_size):
            raise ValueError(f"Model {model_size} is not downloaded")

        model_path = self.models_dir / f"faster-whisper-{model_size}"

        try:
            shutil.rmtree(model_path)
            logger.info(f"Model {model_size} deleted")
        except Exception as e:
            error_msg = f"Failed to delete model {model_size}: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    def get_model_size(self, model_size: str) -> int:
        """Get size of downloaded model in bytes.

        Args:
            model_size: Model size

        Returns:
            Size in bytes, or 0 if not downloaded
        """
        if not self.is_model_downloaded(model_size):
            return 0

        model_path = self.models_dir / f"faster-whisper-{model_size}"
        total_size = 0

        for dirpath, dirnames, filenames in os.walk(model_path):
            for filename in filenames:
                filepath = Path(dirpath) / filename
                total_size += get_file_size(filepath)

        return total_size

    def get_model_info(self, model_size: str) -> Dict:
        """Get model information.

        Args:
            model_size: Model size

        Returns:
            Dictionary with model information
        """
        info = self.MODELS.get(model_size, {}).copy()
        info['name'] = model_size
        info['downloaded'] = self.is_model_downloaded(model_size)

        if info['downloaded']:
            actual_size = self.get_model_size(model_size)
            info['actual_size'] = format_size(actual_size)
            info['actual_size_bytes'] = actual_size

        return info
