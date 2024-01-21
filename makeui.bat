@echo off
cd /d  %~dp0
%~dp0.libs\scripts\activate && pyuic5 -o UI\MainWin.py UI\main.ui