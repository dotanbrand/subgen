"""Settings panel widget."""
import json
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
)
from PyQt6.QtCore import pyqtSignal


class SettingsPanel(QWidget):
    """Panel for application settings (language, model)."""

    # Signals
    languageChanged = pyqtSignal(str)
    modelChanged = pyqtSignal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize settings panel.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Language selection
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Language:")
        lang_label.setFixedWidth(100)
        lang_layout.addWidget(lang_label)

        self.language_combo = QComboBox()
        self.language_combo.currentTextChanged.connect(self._on_language_changed)
        lang_layout.addWidget(self.language_combo)

        layout.addLayout(lang_layout)

        # Model selection
        model_layout = QHBoxLayout()
        model_label = QLabel("Model:")
        model_label.setFixedWidth(100)
        model_layout.addWidget(model_label)

        self.model_combo = QComboBox()
        self.model_combo.currentTextChanged.connect(self._on_model_changed)
        model_layout.addWidget(self.model_combo)

        layout.addLayout(model_layout)

        # Load default languages
        self._load_languages()
        self._load_models()

    def _load_languages(self):
        """Load languages from resource file."""
        try:
            # Get path to languages.json
            resource_path = Path(__file__).parent.parent.parent.parent / 'resources' / 'languages.json'

            with open(resource_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Add languages to combo box
            for lang in data['languages']:
                display = f"{lang['name']} ({lang['code']})" if lang['code'] != 'auto' else lang['name']
                self.language_combo.addItem(display, lang['code'])

        except Exception as e:
            print(f"Warning: Could not load languages: {e}")
            # Add fallback languages
            self.language_combo.addItem("Auto-detect", "auto")
            self.language_combo.addItem("English", "en")
            self.language_combo.addItem("Spanish", "es")

    def _load_models(self):
        """Load available models."""
        models = [
            ("Tiny (75 MB, Fastest)", "tiny"),
            ("Base (145 MB, Recommended)", "base"),
            ("Small (466 MB, Better)", "small"),
            ("Medium (1.5 GB, Best)", "medium"),
        ]

        for display, code in models:
            self.model_combo.addItem(display, code)

        # Set base as default
        self.model_combo.setCurrentIndex(1)

    def _on_language_changed(self, text: str):
        """Handle language change."""
        code = self.language_combo.currentData()
        if code:
            self.languageChanged.emit(code)

    def _on_model_changed(self, text: str):
        """Handle model change."""
        code = self.model_combo.currentData()
        if code:
            self.modelChanged.emit(code)

    def get_language(self) -> str:
        """Get selected language code.

        Returns:
            Language code
        """
        return self.language_combo.currentData() or "auto"

    def get_model(self) -> str:
        """Get selected model.

        Returns:
            Model name
        """
        return self.model_combo.currentData() or "base"

    def set_language(self, code: str):
        """Set selected language.

        Args:
            code: Language code
        """
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == code:
                self.language_combo.setCurrentIndex(i)
                break

    def set_model(self, model: str):
        """Set selected model.

        Args:
            model: Model name
        """
        for i in range(self.model_combo.count()):
            if self.model_combo.itemData(i) == model:
                self.model_combo.setCurrentIndex(i)
                break

    def set_enabled(self, enabled: bool):
        """Enable or disable settings.

        Args:
            enabled: Whether to enable settings
        """
        self.language_combo.setEnabled(enabled)
        self.model_combo.setEnabled(enabled)
