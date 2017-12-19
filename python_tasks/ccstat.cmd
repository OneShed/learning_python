@echo off
set ScriptDir=%~dp0

if not "%1"=="" goto Begin
echo Usage: %0 WorkDir
echo.
echo Inside WorkDir, a .\RawData and .\Data directories will be removed and 
echo repopulated using collect.py and parse.py located in script directory
echo %ScriptDir%
echo.
exit /b 1

:Begin
:: collect from live ClearCase via DataDir into DestDir
set DataDir=%1\RawData
set DestDir=%1\Data
set CCServer=clearcase
set Jobs=4

:: cleanup previous snapshot
echo Removing %DataDir% ...
rd /s /q %DataDir% > NUL
echo Removing %DestDir% ...
rd /s /q %DestDir% > NUL

:: fetch live data
python %ScriptDir%collect.py --verbose --server %CCServer% --properties --full --timeout 3 --processes %Jobs% %DataDir%

:: parse to JSON and CSV
python %ScriptDir%parse.py --verbose %DataDir% %DestDir%
