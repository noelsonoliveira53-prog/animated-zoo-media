@echo off
REM The Animated Zoo - render the film-quality 3D Milo clip on this PC's NVIDIA GPU.
setlocal
cd /d "%~dp0"
set BLENDER=
for /d %%D in ("C:\Program Files\Blender Foundation\Blender*") do if exist "%%D\blender.exe" set BLENDER=%%D\blender.exe
if "%BLENDER%"=="" (
  echo Blender is not installed yet.
  echo Installing it with winget ^(free, from blender.org^)...
  winget install --id BlenderFoundation.Blender -e --accept-source-agreements --accept-package-agreements
  for /d %%D in ("C:\Program Files\Blender Foundation\Blender*") do if exist "%%D\blender.exe" set BLENDER=%%D\blender.exe
)
if "%BLENDER%"=="" (
  echo Could not find Blender. Install it from https://www.blender.org/download/ and run this again.
  pause
  exit /b 1
)
echo Using %BLENDER%
echo Rendering 3D Milo on the GPU. A progress line prints for every frame. You can close this window and run it again later: it continues where it stopped.
"%BLENDER%" -b -P milo_blender.py -- --out "%~dp0out" --mouth "%~dp0mouth.json" --audio "%~dp0voice.wav" --samples 128
echo.
echo Finished. Your video: %~dp0out\final.mp4
start "" "%~dp0out"
pause
