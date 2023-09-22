@echo off
IF "%~1"=="" (
    echo No arguments provided!
    echo Try 'search-txt -h' or 'search-txt --help' for more information.
    pause
    exit /b
)

IF "%~1"=="-h" (
    echo Usage: search-txt inputFile search-terms
    echo This script converts the encoding of inputFile to encoding and writes the output to outputFile.
    echo Example: search-txt file1.txt file2.txt UTF8
    pause
    exit /b
)

IF "%~1"=="--help" (
    echo Usage: search-txt inputFile outputFile encoding
    echo This script converts the encoding of inputFile to encoding and writes the output to outputFile.
    echo Example: search-txt file1.txt file2.txt UTF8
    pause
    exit /b
)

PowerShell -Command "Get-Content -Path %1 | Select-String -Pattern %2 -SimpleMatch"