@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d "%~dp0"
title ASS-ADE ship loop — gates until green
echo.
echo  ASS-ADE autonomous gate loop (local machine only).
echo  - Re-runs: doctor, lint-imports, pytest, synth-tests, golden assimilate, chat smoke.
echo  - Stops when all green, or press Ctrl+C.
echo  - Does NOT push git. After green: stage under C:\!aaaa-nexus then push from there.
echo.
pause
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\swarm-ship-loop.ps1" -UntilGreen -SleepSec 45
set EC=%ERRORLEVEL%
echo.
echo Exit code: %EC%
echo Latest log: logs\swarm-ship-loop.log
echo Latest JSON: logs\LAST_GREEN.json (only if last round was green)
pause
endlocal & exit /b %EC%
