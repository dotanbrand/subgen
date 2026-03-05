# Testing Guide for SubGen

This guide explains how to test SubGen to ensure it's working correctly.

## Prerequisites

Before testing:

1. Install all dependencies: `pip install -r requirements.txt`
2. Install FFmpeg and add to PATH
3. Have test video files ready (MP4, AVI, MKV, etc.)
4. Ensure you have internet for model downloads

## Quick Verification

### Test 1: Installation Check

```bash
# Verify Python packages
python -c "import PyQt6; print('PyQt6:', PyQt6.__version__)"
python -c "import faster_whisper; print('faster-whisper: OK')"
python -c "import ffmpeg; print('ffmpeg-python: OK')"

# Verify FFmpeg
ffmpeg -version
ffprobe -version
```

Expected: All commands succeed without errors.

### Test 2: CLI Basic Test

```bash
cd src
python cli.py --help
```

Expected: Help message displays with all options.

### Test 3: Configuration Test

```bash
cd src
python -c "from core import Config; c = Config(); print('Config dir:', c.config_dir)"
```

Expected: Config directory path displayed (e.g., `~/.subgen` or `%APPDATA%\SubGen`).

## Core Functionality Tests

### Test 4: Audio Extraction

Create a test script `test_audio.py`:

```python
from pathlib import Path
from src.core import AudioExtractor

# Use your test video path
video_path = Path("path/to/test_video.mp4")

extractor = AudioExtractor()

# Test extraction
audio_path = extractor.extract_audio(video_path)
print(f"Audio extracted: {audio_path}")

# Test duration
duration = extractor.get_duration(video_path)
print(f"Duration: {duration:.2f} seconds")

# Check audio file exists
assert audio_path.exists(), "Audio file not created"
print("✓ Audio extraction works!")
```

Expected: Audio WAV file created, duration reported correctly.

### Test 5: SRT Generation

Create a test script `test_srt.py`:

```python
from pathlib import Path
from src.core import SRTGenerator

# Test segments
segments = [
    {"start": 0.0, "end": 2.5, "text": "Hello, this is a test."},
    {"start": 2.5, "end": 5.0, "text": "This is the second subtitle."},
    {"start": 5.0, "end": 8.0, "text": "And this is the third."},
]

generator = SRTGenerator()
output_path = Path("test_output.srt")

# Generate SRT
generator.generate_srt(segments, output_path)

# Validate
assert generator.validate_srt(output_path), "SRT validation failed"

# Display content
print(output_path.read_text())
print("\n✓ SRT generation works!")
```

Expected: Valid SRT file created with correct format.

### Test 6: Model Download (requires internet)

```bash
cd src
python -c "
from core import Config, ModelDownloader
config = Config()
downloader = ModelDownloader(config.models_directory)

# Check what's downloaded
downloaded = downloader.get_downloaded_models()
print('Downloaded models:', downloaded)

# Download tiny model (small, for testing)
if 'tiny' not in downloaded:
    print('Downloading tiny model...')
    downloader.download_model('tiny')
    print('✓ Download complete!')
else:
    print('✓ Tiny model already downloaded')
"
```

Expected: Tiny model downloaded to models directory.

### Test 7: End-to-End CLI Test

```bash
cd src

# Use a SHORT test video (1-2 minutes max for quick test)
python cli.py path/to/short_test_video.mp4 --model tiny --verbose
```

Expected:
- Audio extraction completes
- Model loads
- Transcription progresses with updates
- SRT file created
- No errors

Verify SRT file:
```bash
cat path/to/short_test_video.srt
```

Should show properly formatted subtitles.

## GUI Tests

### Test 8: Launch GUI

```bash
cd src
python main.py
```

Expected: GUI window opens without errors.

### Test 9: Model Manager

1. Launch GUI
2. Click "Manage Models"
3. Verify model list shows available models
4. Try downloading a model
5. Verify download progress shows
6. Verify model shows as downloaded after completion

### Test 10: Full Subtitle Generation

1. Launch GUI
2. Select a test video file
3. Choose language (or auto-detect)
4. Choose model (use "tiny" for quick test)
5. Click "Generate Subtitles"
6. Verify:
   - Progress bar updates
   - Status messages change
   - ETA is displayed
   - UI is disabled during processing
   - Cancel button is enabled
7. Wait for completion
8. Verify success message with output path
9. Check that SRT file exists and is valid

### Test 11: Error Handling

Test various error conditions:

**Invalid video file:**
1. Enter invalid file path
2. Click "Generate Subtitles"
3. Verify error message displayed

**Model not downloaded:**
1. Select a model that's not downloaded
2. Click "Generate Subtitles"
3. Verify prompt to download model

**Cancel during processing:**
1. Start generation
2. Click "Cancel"
3. Confirm cancellation
4. Verify process stops and UI re-enables

### Test 12: Different Video Formats

Test with various formats:
- MP4
- AVI
- MKV
- MOV

Verify all formats work correctly.

### Test 13: Different Languages

Test language auto-detection and selection:
1. Video with English audio → auto-detect
2. Video with Spanish audio → select Spanish
3. Verify subtitles are in correct language

### Test 14: Model Comparison

Generate subtitles with different models for the same video:
- tiny: fastest, lower quality
- base: balanced
- small: slower, better quality

Compare:
- Processing time
- Subtitle accuracy
- Memory usage

## Performance Tests

### Test 15: Resource Usage

Monitor during transcription:
```bash
# On Linux/macOS
top -p $(pgrep -f "python.*main.py")

# On Windows
# Use Task Manager
```

Verify:
- CPU usage is high (expected, CPU-intensive)
- Memory usage is reasonable (<4GB for base model)
- No memory leaks during long processing

### Test 16: Processing Speed

Time different models on same video:
```bash
time python src/cli.py test.mp4 --model tiny
time python src/cli.py test.mp4 --model base
time python src/cli.py test.mp4 --model small
```

Expected ratios:
- tiny: ~3-5x slower than realtime
- base: ~5-10x slower than realtime
- small: ~10-15x slower than realtime

## Edge Cases

### Test 17: Edge Cases

- **Very short video** (<30 seconds)
- **Long video** (>1 hour)
- **Video with no audio**
- **Video with poor audio quality**
- **Very large video file** (>1GB)
- **Already existing output file** (test overwrite prompt)

## Packaging Tests

### Test 18: PyInstaller Build

```bash
pyinstaller subgen.spec
```

Expected: Build completes without errors.

### Test 19: Standalone Executable

1. Copy `dist/SubGen` to another location
2. Run executable
3. Verify full functionality without Python installed

## Regression Tests

After any code changes, run:

1. All Core Functionality Tests (Tests 4-7)
2. End-to-end GUI test (Test 10)
3. Error handling (Test 11)

## Automated Testing

Create `tests/test_core.py`:

```python
import pytest
from pathlib import Path
from src.core import SRTGenerator, Config

def test_srt_format():
    """Test SRT timestamp formatting."""
    gen = SRTGenerator()

    # Test various timestamps
    assert gen.format_timestamp(0) == "00:00:00,000"
    assert gen.format_timestamp(61.5) == "00:01:01,500"
    assert gen.format_timestamp(3661) == "01:01:01,000"

def test_srt_entry():
    """Test SRT entry creation."""
    gen = SRTGenerator()
    entry = gen.create_srt_entry(1, 0, 2.5, "Test subtitle")

    assert "1\n" in entry
    assert "00:00:00,000 --> 00:00:02,500" in entry
    assert "Test subtitle" in entry

def test_config_creation():
    """Test configuration creation."""
    config = Config()

    assert config.config_path.exists()
    assert config.models_directory.exists()
    assert config.default_model in ['tiny', 'base', 'small', 'medium']

# Run with: pytest tests/
```

## Success Criteria

All tests pass if:

✓ Audio extracts correctly from all video formats
✓ SRT files are properly formatted
✓ Model download and management works
✓ Full end-to-end processing completes successfully
✓ GUI is responsive and intuitive
✓ Error messages are clear and helpful
✓ Cancel functionality works
✓ Offline mode works after model download
✓ Packaged executable runs on clean system
✓ No crashes or data loss

## Reporting Issues

When reporting issues, include:

1. SubGen version
2. Operating system and version
3. Python version
4. Video file format and size
5. Model used
6. Error message or unexpected behavior
7. Log file (if available)
8. Steps to reproduce

Log location:
- Windows: `%APPDATA%\SubGen\subgen.log`
- macOS/Linux: `~/.subgen/subgen.log`
