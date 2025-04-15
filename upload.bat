@echo off
cd /d %~dp0

git add .
git commit -m "Автокоммит %date% %time%"
git push origin master
pause