@echo off
pushd "C:\_PATH\custom-tools"
call .\src\convert-img\\venv\Scripts\activate
python src\convert-img\convert-img.py %*
popd