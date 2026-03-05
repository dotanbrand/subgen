"""Application configuration."""
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    """Application configuration manager."""

    VERSION = "1.0.0"

    # Default configuration
    DEFAULTS = {
        "version": VERSION,
        "models_directory": None,  # Will be set to AppData/SubGen/models
        "default_model": "base",
        "default_language": "auto",
        "last_output_directory": None,
        "cpu_threads": os.cpu_count() or 4,
        "auto_open_srt": False
    }

    # Whisper model information
    MODELS = {
        'tiny': {
            'size': '75 MB',
            'size_bytes': 75 * 1024 * 1024,
            'speed': 'fastest',
            'accuracy': 'lowest',
            'recommended': 'Quick drafts, testing'
        },
        'base': {
            'size': '145 MB',
            'size_bytes': 145 * 1024 * 1024,
            'speed': 'fast',
            'accuracy': 'good',
            'recommended': 'Best balance (Recommended)'
        },
        'small': {
            'size': '466 MB',
            'size_bytes': 466 * 1024 * 1024,
            'speed': 'medium',
            'accuracy': 'better',
            'recommended': 'Higher accuracy'
        },
        'medium': {
            'size': '1.5 GB',
            'size_bytes': 1536 * 1024 * 1024,
            'speed': 'slow',
            'accuracy': 'best',
            'recommended': 'Best quality, slow'
        }
    }

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration.

        Args:
            config_path: Path to config file. If None, uses default location.
        """
        if config_path is None:
            config_path = self._get_default_config_path()

        self.config_path = Path(config_path)
        self.config_dir = self.config_path.parent
        self._data: Dict[str, Any] = {}

        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Load or create config
        self.load()

    def _get_default_config_path(self) -> Path:
        """Get default configuration file path."""
        if os.name == 'nt':  # Windows
            app_data = os.getenv('APPDATA')
            base_dir = Path(app_data) / 'SubGen'
        else:  # macOS, Linux
            home = Path.home()
            base_dir = home / '.subgen'

        return base_dir / 'config.json'

    def load(self):
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)

                # Merge with defaults (add any new keys)
                for key, value in self.DEFAULTS.items():
                    if key not in self._data:
                        self._data[key] = value

                # Update version
                self._data['version'] = self.VERSION

            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using defaults.")
                self._data = self.DEFAULTS.copy()
        else:
            self._data = self.DEFAULTS.copy()

        # Set models directory if not set
        if self._data['models_directory'] is None:
            self._data['models_directory'] = str(self.config_dir / 'models')

    def save(self):
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self._data[key] = value
        self.save()

    @property
    def models_directory(self) -> Path:
        """Get models directory path."""
        path = Path(self._data['models_directory'])
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def default_model(self) -> str:
        """Get default model name."""
        return self._data['default_model']

    @property
    def cpu_threads(self) -> int:
        """Get number of CPU threads to use."""
        return self._data['cpu_threads']
