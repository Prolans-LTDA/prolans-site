@echo off
title Prolans: publicar o site novo no GitHub
cd /d "%~dp0"
set "LOG=%~dp0publicacao-log.txt"
echo Publicacao %date% %time% > "%LOG%"
if exist "publicacao-pages.yml" (
  if not exist ".github\workflows" mkdir ".github\workflows"
  move /y "publicacao-pages.yml" ".github\workflows\pages.yml" >nul
)
if not exist ".git" (
  git init -b main >> "%LOG%" 2>&1
  git config user.name "Prolans-LTDA"
  git config user.email "adm@prolans.com.br"
)
git remote get-url origin >nul 2>&1 || git remote add origin https://github.com/Prolans-LTDA/prolans-site.git
echo === status >> "%LOG%"
git status --short >> "%LOG%" 2>&1
git add -A >> "%LOG%" 2>&1
git commit -m "Site novo da Prolans" >> "%LOG%" 2>&1
echo === log >> "%LOG%"
git log --oneline -3 >> "%LOG%" 2>&1
git branch -a >> "%LOG%" 2>&1
git remote -v >> "%LOG%" 2>&1
echo === push >> "%LOG%"
git push -u origin main >> "%LOG%" 2>&1
if errorlevel 1 (
  echo.
  echo  O envio falhou. O Claude vai ler o arquivo publicacao-log.txt.
) else (
  echo.
  echo  Enviado. A publicacao roda sozinha no GitHub, uns 40 segundos.
)
echo === fim >> "%LOG%"
echo.
pause
