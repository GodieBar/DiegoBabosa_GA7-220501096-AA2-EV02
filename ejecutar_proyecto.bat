@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo [1/4] Creando entorno virtual...
  python -m venv .venv || goto :error
)
echo [2/4] Instalando dependencias...
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt || goto :error
echo [3/4] Aplicando migraciones...
python manage.py migrate || goto :error
echo [4/4] Ejecutando pruebas...
python manage.py test || goto :error
echo.
echo Todo correcto. Iniciando servidor en http://127.0.0.1:8000/ordenes/
python manage.py runserver
exit /b 0
:error
echo.
echo ERROR: revisa el mensaje anterior y la GUIA_INSTALACION_WINDOWS.md
pause
exit /b 1
