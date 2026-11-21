@echo off
REM One-time setup of the free AI song engine ACE-Step 1.5 (MIT license, github.com/ACE-Step/ACE-Step-1.5)
REM It runs on this PC's NVIDIA GPU and makes full sung songs from our lyrics. Takes ~10-20 min the first time.
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title ZooBlender - install song engine
echo === 1/4 Git ===
set GIT=
for /f "delims=" %%P in ('where git 2^>nul') do if "!GIT!"=="" set "GIT=%%P"
if "%GIT%"=="" if exist "C:\Program Files\Git\cmd\git.exe" set "GIT=C:\Program Files\Git\cmd\git.exe"
if "%GIT%"=="" (
  winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements
  if exist "C:\Program Files\Git\cmd\git.exe" set "GIT=C:\Program Files\Git\cmd\git.exe"
)
if "%GIT%"=="" ( echo Git could not be installed. & pause & exit /b 1 )
echo Using git: %GIT%
echo === 2/4 uv (Python manager) ===
set UV=
for /f "delims=" %%P in ('where uv 2^>nul') do if "!UV!"=="" set "UV=%%P"
if "%UV%"=="" if exist "%LOCALAPPDATA%\Microsoft\WinGet\Links\uv.exe" set "UV=%LOCALAPPDATA%\Microsoft\WinGet\Links\uv.exe"
if "%UV%"=="" if exist "%USERPROFILE%\.local\bin\uv.exe" set "UV=%USERPROFILE%\.local\bin\uv.exe"
if "%UV%"=="" (
  winget install --id astral-sh.uv -e --accept-source-agreements --accept-package-agreements
  if exist "%LOCALAPPDATA%\Microsoft\WinGet\Links\uv.exe" set "UV=%LOCALAPPDATA%\Microsoft\WinGet\Links\uv.exe"
  if exist "%USERPROFILE%\.local\bin\uv.exe" set "UV=%USERPROFILE%\.local\bin\uv.exe"
)
if "%UV%"=="" ( echo uv could not be installed. & pause & exit /b 1 )
>uv_path.txt echo %UV%
echo Using uv: %UV%
echo === 3/4 Download ACE-Step 1.5 ===
if not exist acestep\pyproject.toml "%GIT%" clone --depth 1 https://github.com/ACE-Step/ACE-Step-1.5 acestep
if not exist acestep\pyproject.toml ( echo Download failed. & pause & exit /b 1 )
cd acestep
echo === 4/4 Install (Python 3.11 + GPU libraries, several GB - please wait) ===
"%UV%" sync
if errorlevel 1 ( echo Install failed - send Claude the text above. & pause & exit /b 1 )
"%UV%" run --with stable-ts python -c "import stable_whisper; print('alignment tool ready')"
cd ..
echo installed %date% %time% > acestep_installed.txt
echo.
echo ===========================================================
echo  Song engine installed. Restart START_RENDER_WORKER.bat so
echo  the worker can use it. The first song also downloads the
echo  AI model (a few GB), after that songs take under a minute.
echo ===========================================================
pause
