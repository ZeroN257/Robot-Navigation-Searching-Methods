@echo off

REM Check if the correct number of arguments is provided
if "%~2"=="" (
    echo Usage: search ^<filename^> ^<method^>
    exit /b
)

REM Get the arguments
set filename=%~1
set method=%~2

REM Check if the file exists
if not exist "%filename%" (
    echo The specified file does not exist.
    exit /b
)

REM Call the appropriate Python script based on the method
if /i "%method%"=="BFS" (
    python BFS.py "%filename%"
) else if /i "%method%"=="AS" (
    python AS.py "%filename%"
) else if /i "%method%"=="DFS" (
    python DFS.py "%filename%"
) else if /i "%method%"=="GBFS" (
    python GBFS.py "%filename%"
) else if /i "%method%"=="CUS1" (
    python CUS1.py "%filename%"
) else if /i "%method%"=="CUS2" (
    python CUS2.py "%filename%"
) else if /i "%method%"=="RS" (
    python RS.py "%filename%"
) else (
    echo Invalid method. Supported methods: BFS, AS, DFS, GBFS
)
