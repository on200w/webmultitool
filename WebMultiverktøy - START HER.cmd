@echo off
setlocal
set "ROOT=%~dp0"
set "TARGET=%ROOT%source\app\index.html"

if not exist "%TARGET%" (
  echo Fant ikke filen:
  echo %TARGET%
  echo.
  echo Sjekk at mappestrukturen er intakt.
  pause
  exit /b 1
)

start "" "%TARGET%"
exit /b 0
