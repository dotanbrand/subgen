# GitHub Setup Guide for Cross-Platform Builds

This guide walks you through setting up SubGen on GitHub to enable automated cross-platform builds.

## Prerequisites

- Git installed on your machine
- GitHub account
- SubGen project on your local machine

## Step-by-Step Setup

### 1. Initialize Git Repository (if not already done)

```bash
cd /Users/dotan.brand/subgen

# Initialize git repository
git init

# Check what will be committed
git status
```

### 2. Review and Commit Files

```bash
# Add all project files
git add .

# Create initial commit
git commit -m "Initial commit: SubGen v1.0.0 with GitHub Actions"
```

### 3. Create GitHub Repository

**Option A: Using GitHub Web UI**

1. Go to https://github.com/new
2. Repository name: `subgen` (or your preferred name)
3. Description: "Automatic subtitle generator using Whisper AI"
4. Choose Public or Private (GitHub Actions free for public repos)
5. **Do NOT** initialize with README, .gitignore, or license (you already have these)
6. Click "Create repository"

**Option B: Using GitHub CLI** (if installed)

```bash
# Install GitHub CLI if needed
brew install gh

# Login to GitHub
gh auth login

# Create repository
gh repo create subgen --public --source=. --remote=origin --push
```

### 4. Add Remote and Push (if using Web UI)

```bash
# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/subgen.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### 5. Verify GitHub Actions Setup

1. Go to your repository on GitHub
2. Click on "Actions" tab
3. You should see two workflows:
   - "Build SubGen" - for manual/PR builds
   - "Release" - for automated releases

If you see a message about enabling Actions, click "I understand my workflows, go ahead and enable them"

### 6. Test the Build Workflow

**Manual Test Run:**

1. Go to "Actions" tab
2. Click "Build SubGen" in the left sidebar
3. Click "Run workflow" button (top right)
4. Select branch: `main`
5. Click green "Run workflow" button
6. Wait for the build to complete (~10-15 minutes for all three platforms)

**Check Build Progress:**

- You'll see three jobs running in parallel:
  - Build on windows-latest
  - Build on macos-latest
  - Build on ubuntu-latest

**Download Artifacts:**

1. Once complete, scroll down to "Artifacts" section
2. Download the platforms you need:
   - `SubGen-Windows-x64` (ZIP file)
   - `SubGen-macOS` (tar.gz file)
   - `SubGen-Linux-x64` (tar.gz file)

### 7. Test the Windows Build

1. Download `SubGen-Windows-x64.zip` from artifacts
2. Transfer to a Windows machine (or VM)
3. Extract the ZIP file
4. Run `SubGen.exe`
5. Test basic functionality:
   - Open a video file
   - Select a model
   - Generate subtitles

## Creating a Release

When you're ready to create an official release:

```bash
# Tag the current commit
git tag v1.0.0

# Push the tag to GitHub
git push origin v1.0.0
```

The Release workflow will automatically:
1. Create a GitHub Release
2. Build for all platforms
3. Upload binaries as release assets
4. Generate release notes

## Troubleshooting

### "Permission denied" when pushing

```bash
# Use SSH instead of HTTPS
git remote set-url origin git@github.com:YOUR_USERNAME/subgen.git

# Or configure credentials
gh auth login
```

### GitHub Actions workflow not appearing

1. Ensure the `.github/workflows/` directory exists
2. Check that workflow files are valid YAML
3. Refresh the Actions tab
4. Check repository settings → Actions → "Allow all actions"

### Build fails on FFmpeg

- Check the workflow logs
- FFmpeg installation uses platform package managers
- If persistent, open an issue with the log output

### Build fails on PyInstaller

- Check for missing dependencies
- Review `hiddenimports` in `subgen.spec`
- Check Python version compatibility (using 3.10)

### Can't download artifacts

- Artifacts expire after 30 days
- Must be logged into GitHub to download
- Check that the workflow completed successfully

## Repository Settings (Optional)

### Branch Protection

1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - Require pull request reviews
   - Require status checks (build) to pass

### Secrets (for future code signing)

If you add code signing in the future:

1. Go to Settings → Secrets and variables → Actions
2. Add secrets:
   - `WINDOWS_CERT_PASSWORD` (for Windows code signing)
   - `MACOS_CERT_PASSWORD` (for macOS code signing)

## File Structure

After setup, your repository should have:

```
subgen/
├── .github/
│   └── workflows/
│       ├── build.yml        # Manual/PR builds
│       └── release.yml      # Automated releases
├── scripts/
│   └── build.py            # Build helper script
├── src/                    # Source code
├── resources/              # Resources
├── subgen.spec            # PyInstaller config
├── requirements.txt       # Python dependencies
├── BUILD.md              # Build documentation
├── GITHUB_SETUP.md       # This file
└── README.md             # Project README
```

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Verify workflows appear in Actions tab
3. ✅ Run manual build to test
4. ✅ Download and test Windows executable
5. ⏭️ Create v1.0.0 release tag
6. ⏭️ Share download links with users

## Benefits of This Setup

- ✅ **No Windows machine needed** - GitHub provides Windows runners
- ✅ **Build all platforms** - Windows, macOS, and Linux simultaneously
- ✅ **Reproducible builds** - Same environment every time
- ✅ **Free for public repos** - Unlimited build minutes
- ✅ **Automated releases** - Just push a tag
- ✅ **Easy distribution** - Download links from GitHub Releases

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller Manual](https://pyinstaller.org/en/stable/)
- [Whisper Models](https://github.com/openai/whisper)

## Support

If you encounter issues:

1. Check the [GitHub Actions logs](https://github.com/YOUR_USERNAME/subgen/actions)
2. Review the [BUILD.md](BUILD.md) documentation
3. Open an issue with the error logs
