# SubGen - Offline Subtitle Generator

Generate SRT subtitle files from video files using local Whisper models. **No internet required** after initial setup. Optimized for **CPU-only processing** on modest hardware.

## Features

- 🎬 Generate subtitles from video files (MP4, AVI, MKV, MOV, etc.)
- 🔌 **100% offline** after model download
- 💻 **CPU optimized** - no GPU required
- 🌍 Support for 30+ languages with auto-detection
- 📝 Industry-standard SRT format output
- 🎨 Modern, user-friendly GUI
- ⚡ 4x faster than standard Whisper (uses faster-whisper)

## System Requirements

- **OS**: Windows 10/11 (64-bit), macOS, Linux
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: Dual-core minimum, quad-core recommended
- **Disk Space**: 2-4GB (app + models)
- **Internet**: Only for initial model download

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/subgen.git
cd subgen

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### CLI Usage (Phase 1 - Current)

```bash
# Basic usage
python src/cli.py path/to/video.mp4

# Specify model size
python src/cli.py video.mp4 --model small

# Specify language
python src/cli.py video.mp4 --language en

# Custom output path
python src/cli.py video.mp4 -o subtitles/output.srt

# Verbose mode
python src/cli.py video.mp4 --verbose
```

### GUI Usage (Phase 2 - Coming Soon)

```bash
# Launch GUI application
python src/main.py
```

## Model Selection

| Model  | Size    | Speed    | Accuracy | Use Case                |
|--------|---------|----------|----------|-------------------------|
| tiny   | 75 MB   | Fastest  | Lowest   | Quick drafts, testing   |
| base   | 145 MB  | Fast     | Good     | **Recommended** balance |
| small  | 466 MB  | Medium   | Better   | Higher accuracy needed  |
| medium | 1.5 GB  | Slow     | Best     | Best quality            |

**Recommendation**: Start with `base` model for the best balance of speed and accuracy.

## Performance Expectations

Processing speed (CPU-only):
- **tiny model**: 3-5x slower than realtime
- **base model**: 5-10x slower than realtime (e.g., 10-minute video = 50-100 minutes)
- **small model**: 10-15x slower than realtime
- **medium model**: 15-25x slower than realtime

These are approximate times on a quad-core CPU. Actual performance varies based on:
- CPU speed and core count
- Audio quality and complexity
- Language (English models are faster)

## Supported Video Formats

MP4, AVI, MKV, MOV, WMV, FLV, WebM, M4V, MPG, MPEG, 3GP, TS

## Project Structure

```
subgen/
├── src/
│   ├── main.py              # GUI entry point (Phase 2)
│   ├── cli.py               # CLI for testing (Phase 1)
│   ├── gui/                 # GUI components (Phase 2)
│   ├── core/                # Core functionality
│   │   ├── audio_extractor.py
│   │   ├── transcriber.py
│   │   ├── srt_generator.py
│   │   ├── model_downloader.py
│   │   └── config.py
│   └── utils/               # Utilities
├── resources/               # Icons, styles, languages
├── models/                  # Downloaded Whisper models
└── requirements.txt
```

## Development Roadmap

- [x] **Phase 1**: Core Functionality (CLI)
  - [x] Audio extraction
  - [x] Whisper transcription
  - [x] SRT generation
  - [x] Model management
  - [x] CLI interface

- [ ] **Phase 2**: GUI Development
  - [ ] Main window layout
  - [ ] File selection
  - [ ] Progress tracking
  - [ ] Model management UI

- [ ] **Phase 3**: Model Management
  - [ ] Model downloader with progress
  - [ ] Model selection UI
  - [ ] Offline mode handling

- [ ] **Phase 4**: Polish & Optimization
  - [ ] CPU optimization
  - [ ] Progress estimation
  - [ ] Error handling
  - [ ] UI styling

- [ ] **Phase 5**: Packaging
  - [ ] Windows executable
  - [ ] Installer (optional)
  - [ ] Documentation

## Technology Stack

- **GUI**: PyQt6
- **Transcription**: faster-whisper (CPU-optimized)
- **Audio Processing**: ffmpeg
- **Packaging**: PyInstaller

## Troubleshooting

### "ffmpeg not found"
Install ffmpeg and add it to your system PATH:
- **Windows**: Download from https://ffmpeg.org/download.html
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

### Out of Memory
Try a smaller model (tiny or base) or close other applications.

### Slow Processing
This is normal on CPU. Use the "tiny" model for faster results, or consider:
- Closing other applications
- Using a computer with more CPU cores
- Being patient - quality takes time!

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## License

MIT License - See LICENSE file for details

## Credits

- Uses [faster-whisper](https://github.com/guillaumekln/faster-whisper) for transcription
- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Powered by [OpenAI Whisper](https://github.com/openai/whisper) models

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
