# SubGen - Quick Start Guide

Get up and running with SubGen in 5 minutes!

## Prerequisites

- Python 3.9-3.11
- FFmpeg installed
- Internet connection (for initial model download only)

## Installation (2 minutes)

```bash
# Navigate to project
cd subgen

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Install FFmpeg

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH
4. Verify: Open cmd and run `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
```

## First Run (3 minutes)

### 1. Launch GUI

```bash
cd src
python main.py
```

### 2. Download Model

- Click **"Manage Models"** button
- Select **"base"** (recommended)
- Click **"Download Selected"**
- Wait for download (~145 MB)
- Click **"Close"** when done

### 3. Generate Subtitles

- Click **"Browse"** next to "Video File"
- Select your video (MP4, AVI, MKV, etc.)
- Leave language as **"Auto-detect"**
- Leave model as **"Base"**
- Click **"Generate Subtitles"**
- Wait for completion (be patient - this takes time!)
- Find your `.srt` file next to the video

## Done! 🎉

Your subtitle file is ready to use with any video player that supports SRT files.

---

## Command Line (Alternative)

Prefer command line?

```bash
cd src
python cli.py /path/to/video.mp4
```

Options:
- `--model tiny|base|small|medium` - Choose model
- `--language en|es|fr|...` - Specify language
- `-o output.srt` - Custom output path
- `--verbose` - Detailed output

---

## Model Recommendations

| Model | Size | Speed | Best For |
|-------|------|-------|----------|
| tiny  | 75 MB | ⚡⚡⚡ | Quick tests, very long videos |
| **base** | 145 MB | ⚡⚡ | **Most users** (recommended) |
| small | 466 MB | ⚡ | Better accuracy needed |
| medium | 1.5 GB | 🐌 | Best quality possible |

**Start with `base`** - it's the best balance!

---

## Expected Processing Time

On a typical quad-core CPU:
- 10-minute video with `base` model = **50-100 minutes**

Yes, it's slow! But:
- ✅ No internet needed (after model download)
- ✅ No GPU required
- ✅ Works on modest hardware
- ✅ Great accuracy

---

## Troubleshooting

### "ffmpeg not found"
- Install ffmpeg and add to PATH
- Restart terminal after installation

### "Model not downloaded"
- Click "Manage Models" and download it first

### Very slow
- This is normal! CPU transcription is slow
- Try `tiny` model for faster results
- Or be patient - quality takes time

### Need help?
- Check **README.md** for full documentation
- Check **TESTING.md** for testing guide
- Check **IMPLEMENTATION_SUMMARY.md** for technical details

---

## What's Next?

- Generate subtitles for more videos
- Try different models and compare
- Experiment with different languages
- Read full documentation in README.md

---

**Happy subtitle generating!** 🎬✨
