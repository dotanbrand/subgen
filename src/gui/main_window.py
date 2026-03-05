"""Main application window."""
import time
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox, QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from .widgets import FileSelector, ProgressPanel, ModelManagerDialog, SettingsPanel
from ..core import AudioExtractor, Transcriber, SRTGenerator, Config
from ..utils import (
    get_logger,
    validate_video_file,
    get_output_path,
    clean_temp_file,
    SUPPORTED_VIDEO_FORMATS
)

logger = get_logger(__name__)


class TranscriptionThread(QThread):
    """Thread for running transcription process."""

    # Signals
    progressUpdate = pyqtSignal(int, str, str, str)  # progress, status, details, eta
    finished = pyqtSignal(bool, str, str)  # success, message, output_path
    error = pyqtSignal(str)

    def __init__(
        self,
        video_path: Path,
        output_path: Path,
        model: str,
        language: str,
        config: Config
    ):
        """Initialize transcription thread.

        Args:
            video_path: Input video path
            output_path: Output SRT path
            model: Model size
            language: Language code
            config: Application config
        """
        super().__init__()

        self.video_path = video_path
        self.output_path = output_path
        self.model = model
        self.language = language if language != "auto" else None
        self.config = config

        self.temp_audio_path: Optional[Path] = None
        self.start_time = 0
        self.video_duration = 0
        self._cancelled = False

    def cancel(self):
        """Cancel transcription."""
        self._cancelled = True

    def run(self):
        """Run transcription process."""
        try:
            self.start_time = time.time()

            # Stage 1: Extract audio (10% of progress)
            self.progressUpdate.emit(0, "Extracting audio...", "", "")

            extractor = AudioExtractor()
            self.temp_audio_path = extractor.extract_audio(self.video_path)
            self.video_duration = extractor.get_duration(self.video_path)

            if self._cancelled:
                self._cleanup()
                return

            self.progressUpdate.emit(10, "Audio extracted", "", "")

            # Stage 2: Load model (5% of progress)
            self.progressUpdate.emit(15, "Loading model...", f"Model: {self.model}", "")

            transcriber = Transcriber(
                model_size=self.model,
                models_dir=self.config.models_directory,
                cpu_threads=self.config.cpu_threads
            )
            transcriber.load_model()

            if self._cancelled:
                self._cleanup()
                return

            self.progressUpdate.emit(20, "Model loaded", "", "")

            # Stage 3: Transcribe (75% of progress)
            self.progressUpdate.emit(
                20,
                "Transcribing...",
                "This may take a while",
                self._estimate_eta(20)
            )

            def progress_callback(progress: float, message: str):
                """Handle transcription progress."""
                # Map 0-100% transcription to 20-95% overall progress
                overall_progress = int(20 + (progress * 0.75))
                eta = self._estimate_eta(overall_progress)

                self.progressUpdate.emit(
                    overall_progress,
                    "Transcribing...",
                    message,
                    eta
                )

            segments = transcriber.transcribe(
                self.temp_audio_path,
                language=self.language,
                progress_callback=progress_callback
            )

            if self._cancelled:
                self._cleanup()
                return

            self.progressUpdate.emit(95, "Transcription complete", "", "")

            # Stage 4: Generate SRT (5% of progress)
            self.progressUpdate.emit(95, "Generating subtitles...", "", "")

            generator = SRTGenerator()
            output_path = generator.generate_srt(segments, self.output_path)

            # Validate
            if not generator.validate_srt(output_path):
                logger.warning("SRT validation failed")

            # Complete
            self.progressUpdate.emit(100, "Complete!", f"{len(segments)} subtitles generated", "")

            elapsed = time.time() - self.start_time
            message = f"Subtitles generated successfully!\n\nTime: {self._format_time(elapsed)}\nSegments: {len(segments)}"

            self.finished.emit(True, message, str(output_path))

        except Exception as e:
            logger.error(f"Transcription error: {e}", exc_info=True)
            self.error.emit(str(e))

        finally:
            self._cleanup()

    def _cleanup(self):
        """Clean up temporary files."""
        if self.temp_audio_path:
            clean_temp_file(self.temp_audio_path)

    def _estimate_eta(self, current_progress: int) -> str:
        """Estimate time remaining.

        Args:
            current_progress: Current progress (0-100)

        Returns:
            ETA string
        """
        if current_progress <= 0:
            return ""

        elapsed = time.time() - self.start_time
        if elapsed < 5:  # Need some samples
            return "Calculating..."

        # Estimate total time
        estimated_total = (elapsed / current_progress) * 100
        remaining = estimated_total - elapsed

        if remaining < 60:
            return f"ETA: {int(remaining)} seconds"
        elif remaining < 3600:
            return f"ETA: {int(remaining / 60)} minutes"
        else:
            hours = int(remaining / 3600)
            minutes = int((remaining % 3600) / 60)
            return f"ETA: {hours}h {minutes}m"

    def _format_time(self, seconds: float) -> str:
        """Format time duration.

        Args:
            seconds: Time in seconds

        Returns:
            Formatted string
        """
        if seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, config: Config):
        """Initialize main window.

        Args:
            config: Application configuration
        """
        super().__init__()

        self.config = config
        self.transcription_thread: Optional[TranscriptionThread] = None

        self.setWindowTitle("SubGen - Offline Subtitle Generator")
        self.resize(700, 550)

        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        """Set up user interface."""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)

        # Title
        title = QLabel("SubGen - Offline Subtitle Generator")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Model management button
        model_btn_layout = QHBoxLayout()
        model_btn_layout.addStretch()

        self.manage_models_btn = QPushButton("Manage Models")
        self.manage_models_btn.clicked.connect(self._open_model_manager)
        self.manage_models_btn.setFixedWidth(150)
        model_btn_layout.addWidget(self.manage_models_btn)

        layout.addLayout(model_btn_layout)

        # Settings panel
        self.settings_panel = SettingsPanel()
        layout.addWidget(self.settings_panel)

        # Video file selector
        layout.addWidget(QLabel("Video File:"))
        self.video_selector = FileSelector(
            mode="open",
            file_filter=f"Video Files ({' '.join(['*' + ext for ext in SUPPORTED_VIDEO_FORMATS])})",
            placeholder="Select video file..."
        )
        self.video_selector.fileSelected.connect(self._on_video_selected)
        layout.addWidget(self.video_selector)

        # Output directory selector
        layout.addWidget(QLabel("Output Location:"))
        self.output_selector = FileSelector(
            mode="directory",
            placeholder="Output directory (default: same as video)..."
        )
        layout.addWidget(self.output_selector)

        # Generate button
        self.generate_btn = QPushButton("Generate Subtitles")
        self.generate_btn.setFixedHeight(40)
        self.generate_btn.clicked.connect(self._start_generation)
        self.generate_btn.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.generate_btn)

        # Progress panel
        self.progress_panel = ProgressPanel()
        layout.addWidget(self.progress_panel)

        # Action buttons
        action_layout = QHBoxLayout()

        self.view_log_btn = QPushButton("View Log")
        self.view_log_btn.clicked.connect(self._view_log)
        action_layout.addWidget(self.view_log_btn)

        action_layout.addStretch()

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self._cancel_generation)
        self.cancel_btn.setEnabled(False)
        action_layout.addWidget(self.cancel_btn)

        layout.addLayout(action_layout)

        layout.addStretch()

    def _load_settings(self):
        """Load settings from config."""
        # Set default model
        self.settings_panel.set_model(self.config.default_model)

        # Set last output directory
        last_dir = self.config.get('last_output_directory')
        if last_dir:
            self.output_selector.set_path(last_dir)

    def _on_video_selected(self, path: str):
        """Handle video file selection.

        Args:
            path: Video file path
        """
        if not path:
            return

        # Auto-populate output directory if empty
        if not self.output_selector.get_path():
            video_path = Path(path)
            if video_path.exists():
                self.output_selector.set_path(str(video_path.parent))

    def _open_model_manager(self):
        """Open model manager dialog."""
        dialog = ModelManagerDialog(self.config, self)
        dialog.exec()

    def _start_generation(self):
        """Start subtitle generation."""
        # Validate input
        video_path = Path(self.video_selector.get_path())
        error = validate_video_file(video_path)
        if error:
            QMessageBox.warning(self, "Invalid Video", error)
            return

        # Get output path
        output_dir = self.output_selector.get_path()
        if output_dir:
            output_path = Path(output_dir) / f"{video_path.stem}.srt"
        else:
            output_path = get_output_path(video_path)

        # Check if output exists
        if output_path.exists():
            reply = QMessageBox.question(
                self,
                "File Exists",
                f"Output file already exists:\n{output_path}\n\nOverwrite?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        # Get settings
        model = self.settings_panel.get_model()
        language = self.settings_panel.get_language()

        # Check if model is downloaded
        from ..core.model_downloader import ModelDownloader
        downloader = ModelDownloader(self.config.models_directory)
        if not downloader.is_model_downloaded(model):
            reply = QMessageBox.question(
                self,
                "Model Not Downloaded",
                f"The {model} model is not downloaded.\n\n"
                f"Would you like to download it now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._open_model_manager()
            return

        # Disable UI
        self._set_ui_enabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_panel.reset()

        # Save settings
        self.config.set('last_output_directory', str(output_path.parent))

        # Start transcription thread
        self.transcription_thread = TranscriptionThread(
            video_path,
            output_path,
            model,
            language,
            self.config
        )

        # Connect signals
        self.transcription_thread.progressUpdate.connect(self._on_progress_update)
        self.transcription_thread.finished.connect(self._on_generation_finished)
        self.transcription_thread.error.connect(self._on_generation_error)

        # Start
        self.transcription_thread.start()
        logger.info(f"Started generation: {video_path} -> {output_path}")

    def _cancel_generation(self):
        """Cancel subtitle generation."""
        if not self.transcription_thread:
            return

        reply = QMessageBox.question(
            self,
            "Cancel Generation",
            "Are you sure you want to cancel?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.transcription_thread.cancel()
            self.progress_panel.set_status("Cancelling...")
            self.cancel_btn.setEnabled(False)

    def _on_progress_update(self, progress: int, status: str, details: str, eta: str):
        """Handle progress update.

        Args:
            progress: Progress value (0-100)
            status: Status message
            details: Details message
            eta: ETA message
        """
        self.progress_panel.update_progress(progress, status, details, eta)

    def _on_generation_finished(self, success: bool, message: str, output_path: str):
        """Handle generation completion.

        Args:
            success: Whether generation succeeded
            message: Result message
            output_path: Output file path
        """
        self._set_ui_enabled(True)
        self.cancel_btn.setEnabled(False)

        if success:
            # Show success message with option to open
            reply = QMessageBox.information(
                self,
                "Success",
                f"{message}\n\nOutput: {output_path}",
                QMessageBox.StandardButton.Ok
            )

            logger.info("Generation completed successfully")
        else:
            QMessageBox.warning(self, "Cancelled", "Generation was cancelled")

    def _on_generation_error(self, error: str):
        """Handle generation error.

        Args:
            error: Error message
        """
        self._set_ui_enabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_panel.set_status("Error")

        QMessageBox.critical(
            self,
            "Error",
            f"An error occurred during generation:\n\n{error}\n\n"
            f"Check the log for more details."
        )

        logger.error(f"Generation failed: {error}")

    def _set_ui_enabled(self, enabled: bool):
        """Enable or disable UI elements.

        Args:
            enabled: Whether to enable UI
        """
        self.video_selector.set_enabled(enabled)
        self.output_selector.set_enabled(enabled)
        self.settings_panel.set_enabled(enabled)
        self.generate_btn.setEnabled(enabled)
        self.manage_models_btn.setEnabled(enabled)

    def _view_log(self):
        """View application log."""
        # Create log viewer dialog
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Application Log")
        dialog.setText("Log viewing not yet implemented")
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.exec()

    def closeEvent(self, event):
        """Handle window close event."""
        # Check if generation is in progress
        if self.transcription_thread and self.transcription_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "Generation in Progress",
                "Subtitle generation is in progress.\n\n"
                "Are you sure you want to quit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.transcription_thread.cancel()
                self.transcription_thread.wait(5000)  # Wait up to 5 seconds
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
