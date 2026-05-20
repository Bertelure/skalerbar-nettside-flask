@echo off
REM Automatisk Git setup og push til GitHub
REM 
REM Denne batch-filen:
REM 1. Initialiserer Git repo lokalt
REM 2. Legger til alle filer
REM 3. Lager første commit
REM 4. Legger til GitHub remote
REM 5. Pusher til GitHub

cd /d "%~dp0"

echo.
echo ========================================
echo Git Setup for skalerbar-nettside-flask
echo ========================================
echo.

REM Sjekk om git er installert
git --version >nul 2>&1
if errorlevel 1 (
    echo [FEIL] Git er ikke installert!
    echo Installer Git fra: https://git-scm.com/
    pause
    exit /b 1
)

REM Initialiserer Git repo hvis ikke allerede gjort
if not exist .git (
    echo [1/5] Initialiserer Git repository...
    git init
    git config user.email "vetlesteinstad@gmail.com"
    git config user.name "Bertelure"
    echo [✓] Git repo initialisert
) else (
    echo [1/5] Git repo finnes allerede - hopper over
)

echo.
echo [2/5] Legger til alle filer...
git add .
echo [✓] Filer lagt til

echo.
echo [3/5] Lager første commit...
git commit -m "Initial commit: Skalerbar Flask-nettside med autentisering og datalagrting

- Flask backend med SQLite database
- Brukerautentisering (login/registrering)
- Datalagrting API med JSON-lagring
- Responsive HTML/CSS frontend
- Dynamisk menysystem
- Skalerbar arkitektur (blueprints)
- Komplett dokumentasjon
- Klart for PythonAnywhere deployment"

if errorlevel 0 (
    echo [✓] Commit opprettet
) else (
    echo [!] Muligens ingenting å committe - fortsetter
)

echo.
echo [4/5] Legger til GitHub remote...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/Bertelure/skalerbar-nettside-flask.git
echo [✓] GitHub remote lagt til

echo.
echo [5/5] Pusher til GitHub...
git branch -M main
git push -u origin main

if errorlevel 0 (
    echo.
    echo ========================================
    echo [✓] SUKSESS! Kode pushet til GitHub
    echo ========================================
    echo.
    echo Repository: https://github.com/Bertelure/skalerbar-nettside-flask
    echo.
) else (
    echo.
    echo [!] Push feilet - sjekk GitHub-autentisering
    echo Se: https://docs.github.com/en/get-started/quickstart/set-up-git
    echo.
)

pause
