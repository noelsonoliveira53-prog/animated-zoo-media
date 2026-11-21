@echo off
REM Quick check: renders 3 full-quality still frames (about a minute on an RTX 4060 Ti).
cd /d "%~dp0"
set BLENDER=
for /d %%D in ("C:\Program Files\Blender Foundation\Blender*") do if exist "%%D\blender.exe" set BLENDER=%%D\blender.exe
if "%BLENDER%"=="" ( echo Install Blender first: run RENDER_MILO.bat or get it from blender.org & pause & exit /b 1 )
"%BLENDER%" -b -P milo_blender.py -- --test --res 1920x1080 --samples 128 --grass 20000 --out "%~dp0out"
start "" "%~dp0out"
pause
