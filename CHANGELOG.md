# Changelog

All notable changes to SubGen will be documented in this file.

## [1.0.0] - 2026-03-04

### Added
- Initial release
- Core functionality for subtitle generation
- Support for multiple Whisper models (tiny, base, small, medium)
- CPU-optimized transcription using faster-whisper
- Modern PyQt6 GUI interface
- Model download and management system
- Support for 30+ languages with auto-detection
- Real-time progress tracking with ETA
- CLI interface for testing and automation
- Support for multiple video formats (MP4, AVI, MKV, MOV, etc.)
- SRT subtitle format output
- Offline operation after initial model download
- Configurable settings with persistent storage
- Comprehensive error handling and logging

### Features
- **Phase 1 (Core Functionality)**: Complete
  - Audio extraction from video files
  - Whisper transcription with CPU optimization
  - SRT generation with proper formatting
  - Model management and downloading
  - Configuration system
  - CLI for testing

- **Phase 2 (GUI Development)**: Complete
  - Main window with intuitive layout
  - File selection widgets
  - Progress tracking panel
  - Settings panel for language and model selection
  - Model manager dialog
  - Multi-threaded processing

### Technical Details
- Python 3.9-3.11 support
- PyQt6 for modern GUI
- faster-whisper for 4x speed improvement
- ffmpeg for audio extraction
- Hugging Face for model distribution
- PyInstaller for standalone executables

### Known Issues
- First transcription may be slow while model loads
- Large models (medium) require significant RAM
- Log viewer not yet implemented

### System Requirements
- Windows 10/11 (64-bit), macOS, or Linux
- 4GB RAM minimum (8GB recommended)
- 2-4GB disk space
- Dual-core CPU minimum (quad-core recommended)

## [Unreleased]

### Planned Features
- Log viewer in GUI
- Batch processing for multiple videos
- Additional subtitle formats (VTT, ASS)
- GPU acceleration support (optional)
- Advanced Whisper parameters
- Subtitle editing capabilities
- Real-time preview during generation
- Model accuracy comparison tool
- Custom model support
- Subtitle timing adjustment
- Translation features
