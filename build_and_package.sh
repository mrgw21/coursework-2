#!/bin/bash

# Detect the operating system
OS=$(uname -s)
echo "Detected OS: $OS"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist InsideImmune.zip

# Build the project
echo "Building the project..."
if [[ "$OS" == "Darwin" ]]; then
    # macOS build
    pyinstaller --onefile --name InsideImmune --distpath . --add-data "assets:assets" --add-data "data:data" main.py
    echo "Setting executable permissions for macOS..."
    chmod +x InsideImmune
elif [[ "$OS" == "Linux" ]]; then
    # Linux build
    pyinstaller --onefile --name InsideImmune --distpath . --add-data "assets:assets" --add-data "data:data" main.py
    echo "Setting executable permissions for Linux..."
    chmod +x InsideImmune
else
    # Assume Windows (Git Bash or WSL environment)
    pyinstaller --onefile --name InsideImmune --distpath . --add-data "assets;assets" --add-data "data;data" main.py
fi

# Check if the build succeeded
if [[ ! -f "InsideImmune" && ! -f "InsideImmune.exe" ]]; then
    echo "Build failed. Exiting..."
    exit 1
fi

# Zip the executable and required files
echo "Packaging the game into InsideImmune-MacOS-Linux.zip..."
if [[ "$OS" == "Darwin" || "$OS" == "Linux" ]]; then
    zip -r InsideImmune-MacOS-Linux.zip InsideImmune assets/ data/ README.md
else
    zip -r InsideImmune-MacOS-Linux.zip InsideImmune.exe assets/ data/ README.md
fi

echo "Packaging complete. InsideImmune-MacOS-Linux.zip is ready for distribution!"