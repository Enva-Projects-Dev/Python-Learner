@echo off
rem startet Python Learner (desktop-fenster über pywebview)
setlocal
cd /d "%~dp0"

rem --- python-interpreter suchen: py launcher -> PATH -> bekannter install-pfad ---
set "PY="
where py >nul 2>&1 && (py -3 -c "import sys" >nul 2>&1 && set "PY=py -3")
if not defined PY (
    where python >nul 2>&1 && (python -c "import sys" >nul 2>&1 && set "PY=python")
)
if not defined PY (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    )
)
if not defined PY (
    echo.
    echo  Python 3.12 was not found on this system.
    echo  Install it with:
    echo      winget install -e --id Python.Python.3.12 --scope user
    echo  then run this file again.
    echo.
    pause
    exit /b 1
)

rem --- pywebview installieren falls nötig (einmalig, sichtbare konsole) ---
%PY% -c "import webview" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    %PY% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo  Package installation failed. Check your internet connection
        echo  and run this file again.
        pause
        exit /b 1
    )
)

rem --- ohne konsolenfenster starten wenn pythonw.exe da is ---
set "PYW="
if /i "%PY%"=="py -3" (
    py -3 -c "import sys" >nul 2>&1 && for /f "delims=" %%i in ('py -3 -c "import sys,os;print(os.path.join(os.path.dirname(sys.executable),'pythonw.exe'))"') do set "PYW=%%i"
) else (
    for /f "delims=" %%i in ('%PY% -c "import sys,os;print(os.path.join(os.path.dirname(sys.executable),'pythonw.exe'))"') do set "PYW=%%i"
)
if defined PYW if exist "%PYW%" (
    start "" "%PYW%" -m app.main
    exit /b 0
)
%PY% -m app.main
endlocal
