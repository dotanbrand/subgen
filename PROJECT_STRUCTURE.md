# SubGen - Project Structure

Complete overview of the SubGen project structure and file organization.

## Directory Tree

```
subgen/
├── src/                           # Source code
│   ├── __init__.py               # Package init
│   ├── main.py                   # GUI entry point ⭐
│   ├── cli.py                    # CLI entry point
│   │
│   ├── core/                     # Core functionality
│   │   ├── __init__.py
│   │   ├── audio_extractor.py   # Extract audio from video (ffmpeg)
│   │   ├── transcriber.py       # Whisper transcription (CPU-optimized)
│   │   ├── srt_generator.py     # Generate SRT subtitle files
│   │   ├── model_downloader.py  # Download & manage Whisper models
│   │   └── config.py            # Application configuration
│   │
│   ├── gui/                      # GUI components (PyQt6)
│   │   ├── __init__.py
│   │   ├── main_window.py       # Main application window
│   │   └── widgets/             # Custom widgets
│   │       ├── __init__.py
│   │       ├── file_selector.py      # File/directory picker
│   │       ├── progress_panel.py     # Progress display
│   │       ├── settings_panel.py     # Language & model settings
│   │       └── model_manager.py      # Model management dialog
│   │
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       ├── logger.py            # Logging configuration
│       ├── file_utils.py        # File operations
│       └── validators.py        # Input validation
│
├── resources/                    # Application resources
│   ├── icons/                   # Icons (empty, ready for use)
│   ├── styles/
│   │   └── main.qss            # PyQt6 stylesheet
│   └── languages.json          # Supported languages
│
├── tests/                       # Test suite
│   ├── __init__.py
│   └── test_core.py            # Core functionality tests
│
├── models/                      # Downloaded Whisper models (gitignored)
│
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
├── subgen.spec                  # PyInstaller configuration
│
└── Documentation:
    ├── README.md                # User guide & overview ⭐
    ├── QUICKSTART.md            # 5-minute quick start
    ├── IMPLEMENTATION_SUMMARY.md # Complete implementation details
    ├── TESTING.md               # Testing guide
    ├── BUILD.md                 # Build & packaging guide
    ├── CHANGELOG.md             # Version history
    ├── LICENSE                  # MIT License
    └── PROJECT_STRUCTURE.md     # This file
```

## File Descriptions

### Entry Points

| File | Purpose | Usage |
|------|---------|-------|
| `src/main.py` | GUI application launcher | `python src/main.py` |
| `src/cli.py` | Command-line interface | `python src/cli.py video.mp4` |

### Core Modules (`src/core/`)

| File | Lines | Purpose |
|------|-------|---------|
| `audio_extractor.py` | ~150 | Extract & convert audio from video using ffmpeg |
| `transcriber.py` | ~180 | CPU-optimized Whisper transcription with progress |
| `srt_generator.py` | ~120 | Generate & validate SRT subtitle files |
| `model_downloader.py` | ~200 | Download & manage Whisper models from HuggingFace |
| `config.py` | ~150 | Configuration management with persistent storage |

### GUI Modules (`src/gui/`)

| File | Lines | Purpose |
|------|-------|---------|
| `main_window.py` | ~450 | Main application window & processing coordinator |
| `widgets/file_selector.py` | ~100 | File/directory picker widget |
| `widgets/progress_panel.py` | ~130 | Progress display with status & ETA |
| `widgets/settings_panel.py` | ~150 | Language & model selection |
| `widgets/model_manager.py` | ~250 | Model download & management dialog |

### Utility Modules (`src/utils/`)

| File | Lines | Purpose |
|------|-------|---------|
| `logger.py` | ~60 | Logging setup & configuration |
| `file_utils.py` | ~80 | File operations & utilities |
| `validators.py` | ~70 | Input validation functions |

### Tests (`tests/`)

| File | Purpose |
|------|---------|
| `test_core.py` | Unit tests for core functionality (config, SRT, utils) |

### Resources (`resources/`)

| File | Purpose |
|------|---------|
| `languages.json` | 30+ supported languages with codes |
| `styles/main.qss` | Qt stylesheet for modern UI theme |
| `icons/` | Application icons (ready for use) |

### Documentation

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Main user guide & overview | End users |
| `QUICKSTART.md` | 5-minute setup guide | New users |
| `IMPLEMENTATION_SUMMARY.md` | Complete technical details | Developers |
| `TESTING.md` | Testing procedures | QA/Developers |
| `BUILD.md` | Build & packaging | Developers |
| `CHANGELOG.md` | Version history | All |
| `PROJECT_STRUCTURE.md` | This file | Developers |

### Configuration Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python package dependencies |
| `setup.py` | Python package configuration |
| `subgen.spec` | PyInstaller build configuration |
| `.gitignore` | Git ignore rules |

## Data Flow

```
User Input (Video File)
         ↓
   Main Window
         ↓
   Transcription Thread (Background)
         ↓
   ┌─────────────────────────────────────┐
   │  1. Audio Extractor                 │
   │     video → 16kHz mono WAV          │
   └─────────────────────────────────────┘
         ↓
   ┌─────────────────────────────────────┐
   │  2. Transcriber                     │
   │     Load model from models/         │
   │     Audio → Text segments           │
   │     (with timestamps)               │
   └─────────────────────────────────────┘
         ↓
   ┌─────────────────────────────────────┐
   │  3. SRT Generator                   │
   │     Segments → Formatted SRT        │
   └─────────────────────────────────────┘
         ↓
   Output (SRT File)
```

## Module Dependencies

```
main.py
  ↓
gui/main_window.py
  ↓
  ├─→ gui/widgets/*         (UI components)
  ├─→ core/audio_extractor  (audio processing)
  ├─→ core/transcriber      (transcription)
  ├─→ core/srt_generator    (subtitle generation)
  ├─→ core/model_downloader (model management)
  ├─→ core/config           (configuration)
  └─→ utils/*               (utilities)
```

## Configuration & Data Storage

### User Data Locations

**Windows:**
- Config: `%APPDATA%\SubGen\config.json`
- Models: `%APPDATA%\SubGen\models\`
- Logs: `%APPDATA%\SubGen\subgen.log`

**macOS/Linux:**
- Config: `~/.subgen/config.json`
- Models: `~/.subgen/models/`
- Logs: `~/.subgen/subgen.log`

### Temporary Files

- Audio extraction: `%TEMP%/subgen/` or `/tmp/subgen/`
- Automatically cleaned up after processing

## Code Statistics

| Category | Files | Lines of Code (approx) |
|----------|-------|------------------------|
| Core | 5 | ~800 |
| GUI | 6 | ~1,200 |
| Utils | 3 | ~210 |
| Tests | 1 | ~200 |
| **Total** | **15** | **~2,410** |

*Plus ~1,500 lines of documentation*

## Key Design Patterns

1. **MVC-like Architecture**
   - Models: `core/` modules
   - Views: `gui/` modules
   - Controllers: `main_window.py`

2. **Multi-threading**
   - Main thread: GUI (Qt event loop)
   - Worker threads: Transcription processing
   - Communication: Qt signals/slots

3. **Separation of Concerns**
   - Core: Business logic (framework-agnostic)
   - GUI: Presentation layer (Qt-specific)
   - Utils: Shared utilities

4. **Configuration Management**
   - Persistent user settings
   - Default values with overrides
   - Platform-specific paths

## External Dependencies

### Python Packages
- `faster-whisper` - CPU-optimized Whisper
- `PyQt6` - GUI framework
- `ffmpeg-python` - Audio extraction
- `huggingface-hub` - Model downloading

### System Dependencies
- `ffmpeg` - Audio/video processing
- `ffprobe` - Video information

## Build Artifacts

When built with PyInstaller:

```
dist/SubGen/
├── SubGen.exe           # Main executable (Windows)
├── SubGen               # Main executable (macOS/Linux)
├── ffmpeg/
│   ├── ffmpeg(.exe)    # Bundled ffmpeg
│   └── ffprobe(.exe)   # Bundled ffprobe
├── resources/
│   ├── languages.json
│   └── styles/
│       └── main.qss
└── [Python runtime & dependencies]
```

## Development Workflow

1. **Setup**: `pip install -r requirements.txt`
2. **Develop**: Edit source files in `src/`
3. **Test**: `pytest tests/` or `python src/cli.py`
4. **Run GUI**: `python src/main.py`
5. **Build**: `pyinstaller subgen.spec`
6. **Distribute**: Package `dist/SubGen/`

## Adding New Features

### Adding a New Widget

1. Create `src/gui/widgets/new_widget.py`
2. Add to `src/gui/widgets/__init__.py`
3. Import in `main_window.py`
4. Add to layout in `_setup_ui()`

### Adding a New Core Module

1. Create `src/core/new_module.py`
2. Add to `src/core/__init__.py`
3. Add tests in `tests/test_new_module.py`
4. Update documentation

### Adding a New Subtitle Format

1. Create `src/core/vtt_generator.py` (example)
2. Follow same pattern as `srt_generator.py`
3. Add format selection to GUI settings
4. Add tests

## Performance Characteristics

### Memory Usage
- Base model: ~500-800 MB RAM
- Small model: ~1-2 GB RAM
- Medium model: ~2-4 GB RAM

### Disk Space
- Application: ~250-300 MB
- Models: 75 MB - 1.5 GB each
- Temp files: ~10-100 MB during processing

### CPU Usage
- During transcription: 80-100% (all cores)
- During GUI idle: <5%
- During audio extraction: 20-40%

## Security Considerations

- No network communication after model download
- No telemetry or tracking
- Local file processing only
- No user data collected
- Open source for audit

## Future Expansion Points

Ready for:
- [ ] Additional subtitle formats (VTT, ASS)
- [ ] GPU acceleration support
- [ ] Batch processing queue
- [ ] Subtitle editor
- [ ] Translation features
- [ ] Real-time preview
- [ ] Plugin system

---

*Last updated: 2026-03-04*
*SubGen v1.0.0*
