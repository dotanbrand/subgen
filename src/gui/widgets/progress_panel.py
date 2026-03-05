"""Progress tracking panel widget."""
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QProgressBar, QGroupBox
)
from PyQt6.QtCore import Qt


class ProgressPanel(QWidget):
    """Panel for displaying progress with detailed information."""

    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize progress panel.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Create group box
        group = QGroupBox("Progress")
        layout = QVBoxLayout(group)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Details label
        self.details_label = QLabel("")
        self.details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.details_label.setStyleSheet("color: #666;")
        layout.addWidget(self.details_label)

        # ETA label
        self.eta_label = QLabel("")
        self.eta_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.eta_label.setStyleSheet("color: #666;")
        layout.addWidget(self.eta_label)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(group)

    def set_progress(self, value: int):
        """Set progress value.

        Args:
            value: Progress value (0-100)
        """
        self.progress_bar.setValue(max(0, min(100, value)))

    def set_status(self, message: str):
        """Set status message.

        Args:
            message: Status message
        """
        self.status_label.setText(message)

    def set_details(self, message: str):
        """Set details message.

        Args:
            message: Details message
        """
        self.details_label.setText(message)

    def set_eta(self, message: str):
        """Set ETA message.

        Args:
            message: ETA message
        """
        self.eta_label.setText(message)

    def reset(self):
        """Reset progress panel."""
        self.progress_bar.setValue(0)
        self.status_label.setText("Ready")
        self.details_label.setText("")
        self.eta_label.setText("")

    def set_indeterminate(self, indeterminate: bool):
        """Set progress bar to indeterminate mode.

        Args:
            indeterminate: Whether to use indeterminate mode
        """
        if indeterminate:
            self.progress_bar.setRange(0, 0)  # Indeterminate
        else:
            self.progress_bar.setRange(0, 100)  # Normal

    def update_progress(
        self,
        value: int,
        status: Optional[str] = None,
        details: Optional[str] = None,
        eta: Optional[str] = None
    ):
        """Update all progress information at once.

        Args:
            value: Progress value (0-100)
            status: Optional status message
            details: Optional details message
            eta: Optional ETA message
        """
        self.set_progress(value)
        if status:
            self.set_status(status)
        if details:
            self.set_details(details)
        if eta:
            self.set_eta(eta)
