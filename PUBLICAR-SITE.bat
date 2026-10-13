@echo off
title Prolans: publicar o site novo no GitHub
cd /d "%~dp0"
if exist "publicacao-pages.yml" (
  if not exist ".github\workflows" mkdir ".github\workflows"
  move /y "publicacao-pages.yml" ".github\workflows\pages.yml" >nul
)
if not exist ".git" (
  git init -b main
  git config user.name "Prolans-LTDA"
  git config user.email "adm@prolans.com.br"
  git remote add origin https://github.com/Prolans-LTDA/prolans-site.git
)
git add -A
git commit -m "Site novo da Prolans" || echo  Nada novo para gravar.
git push -u origin main || (echo. & echo  O envio falhou. Mande um print para o Claude. & goto fim)
echo.
echo  Enviado. A publicacao roda sozinha no GitHub (aba Actions, uns 40 segundos).
:fim
echo.
pause
