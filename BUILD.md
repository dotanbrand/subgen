# Building SubGen

This document explains how to package SubGen for distribution.

## Cross-Platform Building with GitHub Actions (Recommended)

The easiest way to build SubGen for multiple platforms is using GitHub Actions, which provides free Windows, macOS, and Linux runners.

### Prerequisites
- GitHub repository with the SubGen code
- GitHub Actions enabled (enabled by default for public repos)

### Triggering a Build

**Option 1: Manual Build**
1. Go to your GitHub repository
2. Click on "Actions" tab
3. Select "Build SubGen" workflow
4. Click "Run workflow" button
5. Select the branch and click "Run workflow"
6. Wait for the build to complete (~10-15 minutes)
7. Download artifacts from the workflow run page

**Option 2: Automatic Build on Tag**
```bash
# Tag a release
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will automatically build all platforms
```

**Option 3: Build on Pull Request**
- Create a pull request to the `main` branch
- GitHub Actions will automatically build to verify the changes

### Downloading Built Artifacts

After the build completes:
1. Go to the workflow run page
2. Scroll down to "Artifacts" section
3. Download the desired platform:
   - `SubGen-Windows-x64.zip` - Windows Intel/AMD executable
   - `SubGen-macOS.tar.gz` - macOS executable
   - `SubGen-Linux-x64.tar.gz` - Linux executable

Artifacts are kept for 30 days.

### What the GitHub Actions Workflow Does

1. Sets up Python 3.10 on the target platform
2. Installs FFmpeg (platform-specific method)
3. Installs Python dependencies from requirements.txt
4. Updates the spec file with FFmpeg paths
5. Builds with PyInstaller
6. Verifies the build
7. Packages the result (ZIP/tar.gz)
8. Uploads as artifact

### Troubleshooting GitHub Actions Builds

**Build fails on FFmpeg installation:**
- Check the GitHub Actions log for FFmpeg installation step
- The workflow uses platform-specific package managers (choco/brew/apt)

**Build fails on PyInstaller step:**
- Check for missing dependencies in requirements.txt
- Review the PyInstaller logs in the GitHub Actions output
- May need to add `hiddenimports` in subgen.spec

**Artifact not found:**
- Ensure the build completed successfully (green checkmark)
- Artifacts expire after 30 days - download them promptly

## Prerequisites for Local Building

### All Platforms

1. Python 3.9-3.11
2. All dependencies installed (`pip install -r requirements.txt`)
3. FFmpeg installed and in system PATH

### Windows Specific

Download FFmpeg static builds from https://ffmpeg.org/download.html

## Building with PyInstaller

### Step 1: Prepare FFmpeg

**Windows:**
```bash
# Download ffmpeg from https://ffmpeg.org/download.html
# Extract and note the path to ffmpeg.exe and ffprobe.exe
```

**macOS/Linux:**
```bash
# FFmpeg should be in PATH
which ffmpeg
which ffprobe
```

### Step 2: Update spec file

Edit `subgen.spec` and update the binaries section:

```python
binaries=[
    # Windows example:
    ('C:/ffmpeg/bin/ffmpeg.exe', 'ffmpeg'),
    ('C:/ffmpeg/bin/ffprobe.exe', 'ffmpeg'),

    # macOS/Linux example:
    ('/usr/local/bin/ffmpeg', 'ffmpeg'),
    ('/usr/local/bin/ffprobe', 'ffmpeg'),
],
```

### Step 3: Build

**Option A: Using the build helper script (recommended)**
```bash
# Navigate to project root
cd subgen

# Run complete build process
python scripts/build.py --all

# Or run steps individually:
python scripts/build.py --build    # Build with PyInstaller
python scripts/build.py --verify   # Verify the build
python scripts/build.py --package  # Create distributable package
```

**Option B: Using PyInstaller directly**
```bash
# Navigate to project root
cd subgen

# Build with PyInstaller
pyinstaller subgen.spec

# Output will be in dist/SubGen/
```

The build helper script automatically:
- Detects your platform
- Locates FFmpeg binaries
- Builds with PyInstaller
- Verifies the build
- Creates a distributable package (ZIP/tar.gz)

### Step 4: Test

```bash
# Windows
cd dist/SubGen
SubGen.exe

# macOS/Linux
cd dist/SubGen
./SubGen
```

## Distribution

### Windows

**Option 1: ZIP Archive**
```bash
cd dist
zip -r SubGen-Windows.zip SubGen/
```

**Option 2: Installer (using Inno Setup)**

1. Download Inno Setup from https://jrsoftware.org/isinfo.php
2. Create installer script (see `installer.iss` template below)
3. Compile installer

**installer.iss template:**
```iss
[Setup]
AppName=SubGen
AppVersion=1.0.0
DefaultDirName={pf}\SubGen
DefaultGroupName=SubGen
OutputDir=dist
OutputBaseFilename=SubGen-Setup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\SubGen\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\SubGen"; Filename: "{app}\SubGen.exe"
Name: "{commondesktop}\SubGen"; Filename: "{app}\SubGen.exe"

[Run]
Filename: "{app}\SubGen.exe"; Description: "Launch SubGen"; Flags: nowait postinstall skipifsilent
```

### macOS

```bash
# Create DMG (requires create-dmg)
brew install create-dmg

create-dmg \
  --volname "SubGen" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --app-drop-link 450 185 \
  "SubGen.dmg" \
  "dist/SubGen/"
```

### Linux

```bash
# Create tarball
cd dist
tar -czf SubGen-Linux.tar.gz SubGen/
```

## Size Optimization

The bundled app will be approximately:
- Executable: ~250-300 MB (includes PyQt6, ffmpeg)
- Models: Downloaded separately by users

To reduce size:
- Use UPX compression (enabled in spec file)
- Exclude unnecessary modules (already done)
- Consider separate ffmpeg download for users

## Troubleshooting

### "No module named..." errors

Add missing modules to `hiddenimports` in `subgen.spec`:
```python
hiddenimports=[
    'faster_whisper',
    'PyQt6',
    'ffmpeg',
    'your_missing_module',
],
```

### FFmpeg not found in bundled app

1. Verify ffmpeg path in spec file
2. Check that binaries are being copied
3. Ensure ffmpeg is executable

### Large file size

This is normal. The app includes:
- Python runtime
- PyQt6 (large GUI framework)
- FFmpeg (video processing)
- Various dependencies

Models are NOT included and are downloaded separately.

## Release Checklist

- [ ] Update version in `src/__init__.py`
- [ ] Update version in `setup.py`
- [ ] Update version in `subgen.spec`
- [ ] Update CHANGELOG.md
- [ ] Test on clean machine without Python installed
- [ ] Test video processing with each model
- [ ] Create release notes
- [ ] Tag release in git
- [ ] Upload to GitHub releases or distribution platform

## Platform-Specific Notes

### Windows
- Defender may flag the executable (false positive)
- Users may need to "allow" on first run
- Consider code signing certificate for production

### macOS
- App may be blocked by Gatekeeper
- Users need to right-click -> Open on first run
- Consider Apple Developer ID signing for production

### Linux
- Users may need to install system dependencies
- Different distros may have different requirements
- Provide separate builds for common distros if needed
