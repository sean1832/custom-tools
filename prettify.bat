@echo off
pushd "C:\_PATH\custom-tools"
python src\prettify.py %1 %2
popd