"""Model manager dialog."""
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QProgressDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from ...core.model_downloader import ModelDownloader
from ...core.config import Config
from ...utils.logger import get_logger

logger = get_logger(__name__)


class DownloadThread(QThread):
    """Thread for downloading models."""

    progressUpdate = pyqtSignal(int, int, str)
    finished = pyqtSignal(bool, str)

    def __init__(self, downloader: ModelDownloader, model_size: str):
        """Initialize download thread.

        Args:
            downloader: Model downloader instance
            model_size: Model size to download
        """
        super().__init__()
        self.downloader = downloader
        self.model_size = model_size

    def run(self):
        """Run download."""
        try:
            self.downloader.download_model(
                self.model_size,
                progress_callback=self._progress_callback
            )
            self.finished.emit(True, f"Model {self.model_size} downloaded successfully")
        except Exception as e:
            logger.error(f"Download failed: {e}")
            self.finished.emit(False, str(e))

    def _progress_callback(self, downloaded: int, total: int, status: str):
        """Progress callback."""
        self.progressUpdate.emit(downloaded, total, status)


class ModelManagerDialog(QDialog):
    """Dialog for managing Whisper models."""

    def __init__(self, config: Config, parent: Optional[QDialog] = None):
        """Initialize model manager.

        Args:
            config: Application configuration
            parent: Parent widget
        """
        super().__init__(parent)

        self.config = config
        self.downloader = ModelDownloader(config.models_directory)
        self.download_thread: Optional[DownloadThread] = None

        self.setWindowTitle("Model Manager")
        self.setModal(True)
        self.resize(500, 400)

        self._setup_ui()
        self._refresh_model_list()

    def _setup_ui(self):
        """Set up user interface."""
        layout = QVBoxLayout(self)

        # Info label
        info_label = QLabel(
            "Whisper models are downloaded from Hugging Face and stored locally.\n"
            "Internet connection required only for initial download."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Model list
        self.model_list = QListWidget()
        layout.addWidget(self.model_list)

        # Buttons
        button_layout = QHBoxLayout()

        self.download_btn = QPushButton("Download Selected")
        self.download_btn.clicked.connect(self._download_selected)
        button_layout.addWidget(self.download_btn)

        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self._delete_selected)
        button_layout.addWidget(self.delete_btn)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self._refresh_model_list)
        button_layout.addWidget(self.refresh_btn)

        button_layout.addStretch()

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)

    def _refresh_model_list(self):
        """Refresh list of models."""
        self.model_list.clear()

        for model_name, model_info in Config.MODELS.items():
            # Get model info
            info = self.downloader.get_model_info(model_name)

            # Create display text
            status = "✓ Downloaded" if info['downloaded'] else "⬇ Not downloaded"
            text = f"{model_name.upper():<8} {model_info['size']:<10} {status:<20} - {model_info['recommended']}"

            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, model_name)

            # Color based on status
            if info['downloaded']:
                item.setForeground(Qt.GlobalColor.darkGreen)

            self.model_list.addItem(item)

    def _get_selected_model(self) -> Optional[str]:
        """Get currently selected model.

        Returns:
            Selected model name or None
        """
        current = self.model_list.currentItem()
        if current:
            return current.data(Qt.ItemDataRole.UserRole)
        return None

    def _download_selected(self):
        """Download selected model."""
        model = self._get_selected_model()
        if not model:
            QMessageBox.warning(self, "No Selection", "Please select a model to download")
            return

        # Check if already downloaded
        if self.downloader.is_model_downloaded(model):
            QMessageBox.information(
                self,
                "Already Downloaded",
                f"Model {model} is already downloaded"
            )
            return

        # Confirm download
        model_info = Config.MODELS[model]
        reply = QMessageBox.question(
            self,
            "Confirm Download",
            f"Download {model} model ({model_info['size']})?\n\n"
            f"This will require an internet connection.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        # Start download
        self._start_download(model)

    def _start_download(self, model: str):
        """Start downloading model.

        Args:
            model: Model name
        """
        # Create progress dialog
        progress = QProgressDialog(
            f"Downloading {model} model...",
            "Cancel",
            0,
            100,
            self
        )
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setAutoClose(True)

        # Create download thread
        self.download_thread = DownloadThread(self.downloader, model)

        # Connect signals
        self.download_thread.progressUpdate.connect(
            lambda downloaded, total, status: progress.setLabelText(status)
        )

        self.download_thread.finished.connect(
            lambda success, msg: self._on_download_finished(success, msg, progress)
        )

        # Start download
        self.download_thread.start()
        progress.exec()

    def _on_download_finished(self, success: bool, message: str, progress: QProgressDialog):
        """Handle download completion.

        Args:
            success: Whether download succeeded
            message: Result message
            progress: Progress dialog
        """
        progress.close()

        if success:
            QMessageBox.information(self, "Download Complete", message)
            self._refresh_model_list()
        else:
            QMessageBox.critical(self, "Download Failed", f"Failed to download model:\n{message}")

    def _delete_selected(self):
        """Delete selected model."""
        model = self._get_selected_model()
        if not model:
            QMessageBox.warning(self, "No Selection", "Please select a model to delete")
            return

        # Check if downloaded
        if not self.downloader.is_model_downloaded(model):
            QMessageBox.information(self, "Not Downloaded", f"Model {model} is not downloaded")
            return

        # Confirm deletion
        model_info = self.downloader.get_model_info(model)
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete {model} model?\n\n"
            f"This will free {model_info.get('actual_size', 'unknown')} of disk space.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        # Delete model
        try:
            self.downloader.delete_model(model)
            QMessageBox.information(self, "Deleted", f"Model {model} deleted successfully")
            self._refresh_model_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete model:\n{e}")
