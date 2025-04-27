@echo off
cd /d %~dp0

git add .
git commit -m "Auto %date% %time%"
git push origin master
pause