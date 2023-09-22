@echo off
IF "%~1"=="" (
    echo No arguments provided!
    echo Try 'convert-txt -h' or 'convert-txt--help' for more information.
    pause
    exit /b
)

IF "%~1"=="-h" (
    echo Usage: convert-txt inputFile outputFile encoding
    echo This script converts the encoding of inputFile to encoding and writes the output to outputFile.
    echo Example: convert-txt file1.txt file2.txt UTF8
    pause
    exit /b
)

IF "%~1"=="--help" (
    echo Usage: convert-txt inputFile outputFile encoding
    echo This script converts the encoding of inputFile to encoding and writes the output to outputFile.
    echo Example: convert-txt file1.txt file2.txt UTF8
    pause
    exit /b
)

PowerShell -Command "get-content %1 | set-content -encoding %3 %2"
IF EXIST %2 (
    echo File converted successfully.
) ELSE (
    echo File conversion failed.
)
