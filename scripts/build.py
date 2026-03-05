#!/usr/bin/env python3
"""
Build helper script for SubGen.
Handles platform detection, FFmpeg location, and build verification.
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def get_platform_info():
    """Get current platform information."""
    system = platform.system()
    machine = platform.machine()
    return {
        'system': system,
        'machine': machine,
        'is_windows': system == 'Windows',
        'is_macos': system == 'Darwin',
        'is_linux': system == 'Linux',
    }


def find_ffmpeg():
    """Locate FFmpeg and FFprobe binaries."""
    ffmpeg = shutil.which('ffmpeg')
    ffprobe = shutil.which('ffprobe')

    if not ffmpeg or not ffprobe:
        print("ERROR: FFmpeg not found in PATH!")
        print("Please install FFmpeg before building.")
        sys.exit(1)

    print(f"✓ Found ffmpeg: {ffmpeg}")
    print(f"✓ Found ffprobe: {ffprobe}")

    return ffmpeg, ffprobe


def update_spec_file(ffmpeg_path, ffprobe_path):
    """Update the spec file with FFmpeg paths (if needed)."""
    print("\nFFmpeg binaries will be detected automatically by subgen.spec")
    print("No manual spec file update required.")
    return True


def verify_build():
    """Verify that the build completed successfully."""
    pinfo = get_platform_info()
    dist_dir = Path('dist/SubGen')

    if not dist_dir.exists():
        print("ERROR: Build directory not found!")
        return False

    # Check for executable
    if pinfo['is_windows']:
        exe_path = dist_dir / 'SubGen.exe'
    else:
        exe_path = dist_dir / 'SubGen'

    if not exe_path.exists():
        print(f"ERROR: Executable not found: {exe_path}")
        return False

    print(f"✓ Found executable: {exe_path}")

    # Check for FFmpeg binaries in dist
    ffmpeg_dir = dist_dir / 'ffmpeg'
    if ffmpeg_dir.exists():
        ffmpeg_files = list(ffmpeg_dir.glob('*'))
        print(f"✓ FFmpeg directory exists with {len(ffmpeg_files)} files")
        for f in ffmpeg_files:
            print(f"  - {f.name}")
    else:
        print("WARNING: FFmpeg directory not found in dist!")
        print("The application may not work correctly.")

    # Check for resources
    resources_dir = dist_dir / 'resources'
    if resources_dir.exists():
        print(f"✓ Resources directory exists")
    else:
        print("WARNING: Resources directory not found!")

    # Check size
    size_mb = sum(f.stat().st_size for f in dist_dir.rglob('*') if f.is_file()) / (1024 * 1024)
    print(f"✓ Build size: {size_mb:.1f} MB")

    return True


def run_build():
    """Run PyInstaller build."""
    print("\n=== Building with PyInstaller ===\n")

    spec_file = Path('subgen.spec')
    if not spec_file.exists():
        print("ERROR: subgen.spec not found!")
        return False

    try:
        subprocess.run(['pyinstaller', 'subgen.spec'], check=True)
        print("\n✓ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Build failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print("ERROR: PyInstaller not found!")
        print("Install with: pip install pyinstaller")
        return False


def package_build():
    """Create a distributable package."""
    pinfo = get_platform_info()
    dist_dir = Path('dist')

    print("\n=== Creating package ===\n")

    if pinfo['is_windows']:
        # Create ZIP for Windows
        output_file = dist_dir / 'SubGen-Windows-x64.zip'
        try:
            shutil.make_archive(
                str(output_file.with_suffix('')),
                'zip',
                dist_dir,
                'SubGen'
            )
            print(f"✓ Created: {output_file}")
        except Exception as e:
            print(f"ERROR: Failed to create ZIP: {e}")
            return False

    elif pinfo['is_macos']:
        # Create tarball for macOS
        output_file = dist_dir / 'SubGen-macOS.tar.gz'
        try:
            subprocess.run([
                'tar', '-czf',
                str(output_file),
                '-C', str(dist_dir),
                'SubGen'
            ], check=True)
            print(f"✓ Created: {output_file}")
        except Exception as e:
            print(f"ERROR: Failed to create tarball: {e}")
            return False

    elif pinfo['is_linux']:
        # Create tarball for Linux
        output_file = dist_dir / 'SubGen-Linux-x64.tar.gz'
        try:
            subprocess.run([
                'tar', '-czf',
                str(output_file),
                '-C', str(dist_dir),
                'SubGen'
            ], check=True)
            print(f"✓ Created: {output_file}")
        except Exception as e:
            print(f"ERROR: Failed to create tarball: {e}")
            return False

    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='SubGen build helper')
    parser.add_argument('--update-spec', action='store_true',
                        help='Update spec file with FFmpeg paths')
    parser.add_argument('--verify', action='store_true',
                        help='Verify the build')
    parser.add_argument('--build', action='store_true',
                        help='Run the build')
    parser.add_argument('--package', action='store_true',
                        help='Package the build')
    parser.add_argument('--all', action='store_true',
                        help='Run complete build process')

    args = parser.parse_args()

    # Show platform info
    pinfo = get_platform_info()
    print(f"Platform: {pinfo['system']} {pinfo['machine']}")

    # Find FFmpeg
    ffmpeg, ffprobe = find_ffmpeg()

    if args.update_spec or args.all:
        update_spec_file(ffmpeg, ffprobe)

    if args.build or args.all:
        if not run_build():
            sys.exit(1)

    if args.verify or args.all:
        if not verify_build():
            sys.exit(1)

    if args.package or args.all:
        if not package_build():
            sys.exit(1)

    if not any([args.update_spec, args.verify, args.build, args.package, args.all]):
        # Default: just show info
        print("\nUse --all to run complete build process")
        print("Or use --build, --verify, --package individually")


if __name__ == '__main__':
    main()
