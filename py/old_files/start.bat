@echo off
echo Are you sure you are supposed to be running this? It may cause issues if you dont know what you are doing.[y/n]
set/p "ans=>"
if ans == 'n' GOTO :END
python.exe test.py

:END