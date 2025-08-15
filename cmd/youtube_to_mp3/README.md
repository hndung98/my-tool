# Introduction
This tool can transform a youtube video url to mp3 file

# Installation

- Install Chocolatey using Powershell (admin)

```
Set-ExecutionPolicy Bypass -Scope Process -Force; `
[System.Net.ServicePointManager]::SecurityProtocol = `
[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

To check version: `choco -v`

- Install ffmpeg

```
choco install ffmpeg
```

To check version: `ffmpeg -v`

- Install py package

```
pip install yt-dlp
```

- Run bat file
