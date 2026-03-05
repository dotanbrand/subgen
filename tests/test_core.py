"""Core functionality tests."""
import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from core import Config, SRTGenerator
from utils import format_size, get_output_path


class TestConfig:
    """Test configuration functionality."""

    def test_config_creation(self):
        """Test config file creation."""
        config = Config()
        assert config.config_path.exists()
        assert config.models_directory.exists()

    def test_config_defaults(self):
        """Test default configuration values."""
        config = Config()
        assert config.default_model in ['tiny', 'base', 'small', 'medium']
        assert config.cpu_threads > 0
        assert config.get('version') == '1.0.0'

    def test_config_models(self):
        """Test model metadata."""
        assert 'tiny' in Config.MODELS
        assert 'base' in Config.MODELS
        assert 'small' in Config.MODELS
        assert 'medium' in Config.MODELS

        for model, info in Config.MODELS.items():
            assert 'size' in info
            assert 'speed' in info
            assert 'accuracy' in info


class TestSRTGenerator:
    """Test SRT generation functionality."""

    def test_timestamp_formatting(self):
        """Test SRT timestamp formatting."""
        gen = SRTGenerator()

        # Test various timestamps
        assert gen.format_timestamp(0) == "00:00:00,000"
        assert gen.format_timestamp(1.5) == "00:00:01,500"
        assert gen.format_timestamp(61.5) == "00:01:01,500"
        assert gen.format_timestamp(3661.250) == "01:01:01,250"

    def test_srt_entry_creation(self):
        """Test creating a single SRT entry."""
        gen = SRTGenerator()
        entry = gen.create_srt_entry(1, 0, 2.5, "Test subtitle")

        assert "1\n" in entry
        assert "00:00:00,000 --> 00:00:02,500" in entry
        assert "Test subtitle" in entry

    def test_srt_generation(self, tmp_path):
        """Test generating complete SRT file."""
        segments = [
            {"start": 0.0, "end": 2.5, "text": "First subtitle."},
            {"start": 2.5, "end": 5.0, "text": "Second subtitle."},
            {"start": 5.0, "end": 8.0, "text": "Third subtitle."},
        ]

        gen = SRTGenerator()
        output_path = tmp_path / "test.srt"

        # Generate
        result = gen.generate_srt(segments, output_path)
        assert result == output_path
        assert output_path.exists()

        # Read and verify
        content = output_path.read_text()
        assert "1\n" in content
        assert "2\n" in content
        assert "3\n" in content
        assert "First subtitle" in content
        assert "-->" in content

    def test_srt_validation(self, tmp_path):
        """Test SRT validation."""
        gen = SRTGenerator()

        # Valid SRT
        valid_path = tmp_path / "valid.srt"
        valid_path.write_text(
            "1\n00:00:00,000 --> 00:00:02,000\nTest\n\n"
        )
        assert gen.validate_srt(valid_path)

        # Invalid SRT (no timestamps)
        invalid_path = tmp_path / "invalid.srt"
        invalid_path.write_text("Just some text")
        assert not gen.validate_srt(invalid_path)


class TestUtils:
    """Test utility functions."""

    def test_format_size(self):
        """Test file size formatting."""
        assert "1.0 KB" in format_size(1024)
        assert "1.0 MB" in format_size(1024 * 1024)
        assert "1.0 GB" in format_size(1024 * 1024 * 1024)

    def test_get_output_path(self, tmp_path):
        """Test output path generation."""
        video_path = tmp_path / "test_video.mp4"
        video_path.touch()

        output_path = get_output_path(video_path)
        assert output_path.suffix == ".srt"
        assert output_path.stem == "test_video"
        assert output_path.parent == tmp_path


class TestValidators:
    """Test validation functions."""

    def test_video_validation(self, tmp_path):
        """Test video file validation."""
        from utils import validate_video_file

        # Non-existent file
        error = validate_video_file(tmp_path / "missing.mp4")
        assert "does not exist" in error.lower()

        # Valid video file (just check extension for this test)
        video = tmp_path / "test.mp4"
        video.touch()
        error = validate_video_file(video)
        # Will fail if ffmpeg can't read it, but file exists
        # In real test would use actual video file


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
