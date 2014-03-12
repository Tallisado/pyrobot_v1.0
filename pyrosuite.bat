@echo off

set thisDir=%~dp0
set oldDir=%CD%
set python=%thisDir%..\Python\python.exe
set PYTHONPATH_BAK=%PYTHONPATH%
set PYTHONPATH=%PYTHONPATH%;%thisDir%..\Tests\CommonLibs
set PATH_BAK=%PATH%
set PATH=%PATH%;%thisDir%..\Python

cd %thisDir%
%python% Parabot.py -b %oldDir%\ %*
cd %oldDir%

set PYTHONPATH=%PYTHONPATH_BAK%
set PYTHONPATH_BAK=
set python=
set oldDir=
set PATH=%PATH_BAK%
set PATH_BAK=