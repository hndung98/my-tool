@echo off
setlocal enabledelayedexpansion

:: Create url
if "%~1"=="" (
    set /p ytlink=YouTube Url: 
) else (
    set ytlink=%~1
)

:: Create folder to save
set "outdir=%~dp0downloads"
if not exist "%outdir%" mkdir "%outdir%"

:: Download
yt-dlp -x --audio-format mp3 -o "%outdir%\%%(title)s.%%(ext)s" "%ytlink%"

echo.
echo === Downloaded ===
pause
