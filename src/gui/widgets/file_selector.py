"""File selection widget."""
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton, QFileDialog
)
from PyQt6.QtCore import pyqtSignal


class FileSelector(QWidget):
    """Widget for selecting files with browse button."""

    # Signal emitted when file is selected
    fileSelected = pyqtSignal(str)

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        mode: str = "open",
        file_filter: str = "All Files (*.*)",
        placeholder: str = "Select file..."
    ):
        """Initialize file selector.

        Args:
            parent: Parent widget
            mode: 'open' for opening files, 'save' for saving, 'directory' for folders
            file_filter: File filter for dialog
            placeholder: Placeholder text
        """
        super().__init__(parent)

        self.mode = mode
        self.file_filter = file_filter

        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Path input
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(placeholder)
        self.path_input.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.path_input)

        # Browse button
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self._browse)
        self.browse_btn.setFixedWidth(100)
        layout.addWidget(self.browse_btn)

    def _browse(self):
        """Open file browser dialog."""
        if self.mode == "open":
            path, _ = QFileDialog.getOpenFileName(
                self,
                "Select File",
                str(Path.home()),
                self.file_filter
            )
        elif self.mode == "save":
            path, _ = QFileDialog.getSaveFileName(
                self,
                "Save File",
                str(Path.home()),
                self.file_filter
            )
        elif self.mode == "directory":
            path = QFileDialog.getExistingDirectory(
                self,
                "Select Directory",
                str(Path.home())
            )
        else:
            return

        if path:
            self.set_path(path)

    def _on_text_changed(self, text: str):
        """Handle text changed in input."""
        self.fileSelected.emit(text)

    def get_path(self) -> str:
        """Get current path.

        Returns:
            Current path string
        """
        return self.path_input.text()

    def set_path(self, path: str):
        """Set path.

        Args:
            path: Path to set
        """
        self.path_input.setText(path)

    def clear(self):
        """Clear path."""
        self.path_input.clear()

    def set_enabled(self, enabled: bool):
        """Enable or disable widget.

        Args:
            enabled: Whether to enable widget
        """
        self.path_input.setEnabled(enabled)
        self.browse_btn.setEnabled(enabled)
