@echo off
setlocal
cd /d "%~dp0"

rem Usage:
rem   start-algoplay.cmd          - run AlgoPlay locally (Vite dev server with built-in Java/Python compiler)
rem   start-algoplay.cmd docker   - run the full Docker stack (MySQL + Spring Boot judge + Nginx frontend)

if /i "%~1"=="docker" goto docker

where node >nul 2>&1
if errorlevel 1 (
  echo Node.js 18+ is required. Install it from https://nodejs.org and run this file again.
  pause
  exit /b 1
)
where javac >nul 2>&1
if errorlevel 1 echo WARNING: javac was not found on PATH - Java submissions will not compile. Install JDK 17+.
where python >nul 2>&1
if errorlevel 1 (
  where py >nul 2>&1
  if errorlevel 1 echo WARNING: Python 3 was not found on PATH - Python submissions will not run.
)

cd frontend
if not exist node_modules (
  echo Installing frontend dependencies...
  call npm install
  if errorlevel 1 (
    echo npm install failed. Check the output above.
    pause
    exit /b 1
  )
)
echo Starting AlgoPlay with the local compiler on http://localhost:3000 ...
start "" http://localhost:3000
call npm run dev
exit /b %errorlevel%

:docker
where docker >nul 2>&1
if errorlevel 1 (
  echo Docker Desktop is required for the docker mode. Run without arguments to use the local compiler instead.
  pause
  exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
  echo Docker Desktop is installed but its engine is not running.
  echo Start Docker Desktop, wait until it says Engine running, then run this file again.
  pause
  exit /b 1
)

echo Starting the database, code judge, and frontend. First startup may take several minutes.
docker compose up -d --build mysql backend frontend
if errorlevel 1 (
  echo The judge backend failed to start. Check Docker Desktop and the output above.
  pause
  exit /b 1
)

echo AlgoPlay is starting. Open http://localhost:3000 in your browser.
start "" http://localhost:3000
