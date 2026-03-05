"""Setup script for SubGen."""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme = Path('README.md')
long_description = readme.read_text(encoding='utf-8') if readme.exists() else ''

setup(
    name='subgen',
    version='1.0.0',
    description='Offline subtitle generator using Whisper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='SubGen Team',
    author_email='',
    url='https://github.com/yourusername/subgen',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        'resources': ['languages.json', 'styles/*.qss'],
    },
    install_requires=[
        'faster-whisper>=1.0.0',
        'PyQt6>=6.6.1',
        'ffmpeg-python>=0.2.0',
        'huggingface-hub>=0.19.4',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.3',
            'pytest-qt>=4.2.0',
            'black>=23.12.1',
            'pyinstaller>=6.3.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'subgen-cli=cli:main',
        ],
        'gui_scripts': [
            'subgen=main:main',
        ],
    },
    python_requires='>=3.9,<3.12',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Multimedia :: Video',
        'Topic :: Text Processing',
    ],
)
