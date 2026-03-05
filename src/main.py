#!/usr/bin/env python3
"""SubGen main entry point."""
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from gui import MainWindow
from core import Config
from utils import setup_logger


def main():
    """Main application entry point."""
    # Setup logging
    config = Config()
    log_file = config.config_dir / 'subgen.log'
    setup_logger(name="subgen", log_file=log_file)

    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("SubGen")
    app.setOrganizationName("SubGen")

    # Load stylesheet if exists
    stylesheet_path = Path(__file__).parent.parent / 'resources' / 'styles' / 'main.qss'
    if stylesheet_path.exists():
        try:
            with open(stylesheet_path, 'r', encoding='utf-8') as f:
                app.setStyleSheet(f.read())
        except Exception as e:
            print(f"Warning: Could not load stylesheet: {e}")

    # Create and show main window
    window = MainWindow(config)
    window.show()

    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
