@echo off

REM Temporary build directory
set TEMP_BUILD_DIR=temp_build

REM Clean previous builds
echo Cleaning previous builds...
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q %TEMP_BUILD_DIR%
del InsideImmune.zip 2>nul

REM Create a temporary directory for the build
mkdir %TEMP_BUILD_DIR%

REM Build the project
echo Building the project...
pyinstaller --onefile --name InsideImmune --distpath %TEMP_BUILD_DIR% --add-data "assets;assets" --add-data "data;data" main.py

REM Check if the build was successful
if exist "%TEMP_BUILD_DIR%\InsideImmune.exe" (
    echo Build completed successfully.
    move /y "%TEMP_BUILD_DIR%\InsideImmune.exe" InsideImmune.exe
) else (
    echo Build failed. Exiting...
    rmdir /s /q %TEMP_BUILD_DIR%
    exit /b 1
)

REM Package the executable and required files into a zip
echo Packaging the game into InsideImmune-Windows.zip...
powershell -Command "Compress-Archive -Path InsideImmune.exe, assets, data, README.md -DestinationPath InsideImmune-Windows.zip"

REM Clean up the temporary directory
echo Cleaning up temporary files...
rmdir /s /q %TEMP_BUILD_DIR%

echo Packaging complete. InsideImmune.zip is ready for distribution!
pause