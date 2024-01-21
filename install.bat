@echo off
cd /d  %~dp0
%~dp0libs\python -m virtualenv  .libs
rem >"log/python.log"