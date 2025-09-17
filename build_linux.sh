#!/bin/bash
# Build script for Linux

# Install PyInstaller if not already installed
pip install pyinstaller

# Build the executable, adding the python directory to the path
# Using --paths to add the python directory to the module search path
pyinstaller --onefile \
            --noconsole \
            --name tagfinder \
            --paths=python \
            python/tagfinder.py

echo "Build complete. The executable is in dist/tagfinder"
