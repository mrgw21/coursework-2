#!/bin/bash

# Detect the operating system
OS=$(uname -s)
echo "Detected OS: $OS"

# Temporary directory for the build
TEMP_BUILD_DIR="temp_build"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist InsideImmune.zip $TEMP_BUILD_DIR

# Create a temporary directory for the build
mkdir -p $TEMP_BUILD_DIR

# Build the project
echo "Building the project..."
if [[ "$OS" == "Darwin" ]]; then
    # macOS build
    pyinstaller --onefile --name InsideImmune --distpath $TEMP_BUILD_DIR --add-data "assets:assets" --add-data "data:data" main.py
    echo "Setting executable permissions for macOS..."
    chmod +x $TEMP_BUILD_DIR/InsideImmune
elif [[ "$OS" == "Linux" ]]; then
    # Linux build
    pyinstaller --onefile --name InsideImmune --distpath $TEMP_BUILD_DIR --add-data "assets:assets" --add-data "data:data" main.py
    echo "Setting executable permissions for Linux..."
    chmod +x $TEMP_BUILD_DIR/InsideImmune
else
    # Assume Windows (Git Bash or WSL environment)
    pyinstaller --onefile --name InsideImmune --distpath $TEMP_BUILD_DIR --add-data "assets;assets" --add-data "data;data" main.py
fi

# Check if the build succeeded
if [[ ! -f "$TEMP_BUILD_DIR/InsideImmune" && ! -f "$TEMP_BUILD_DIR/InsideImmune.exe" ]]; then
    echo "Build failed. Exiting..."
    rm -rf $TEMP_BUILD_DIR
    exit 1
fi

# Zip the executable and required files
echo "Packaging the game into InsideImmune-MacOS-Linux.zip..."
if [[ "$OS" == "Darwin" || "$OS" == "Linux" ]]; then
    zip -r InsideImmune-MacOS-Linux.zip $TEMP_BUILD_DIR/InsideImmune assets/ data/ README.md
else
    zip -r InsideImmune-MacOS-Linux.zip $TEMP_BUILD_DIR/InsideImmune.exe assets/ data/ README.md
fi

# Clean up the temporary directory
echo "Cleaning up temporary files..."
rm -rf $TEMP_BUILD_DIR

echo "Packaging complete. InsideImmune-MacOS-Linux.zip is ready for distribution!"