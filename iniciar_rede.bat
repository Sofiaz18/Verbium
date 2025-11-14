@echo off
echo ========================================
echo    VERBIUM - Servidor na Rede Local
echo ========================================
echo.

REM Obter IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        set LOCAL_IP=%%b
        goto :found
    )
)
:found

echo IP Local: %LOCAL_IP%
echo Porta: 8000
echo.
echo URLs de Acesso:
echo   Local: http://127.0.0.1:8000
echo   Rede:  http://%LOCAL_IP%:8000
echo.
echo Usuarios de teste:
echo   Professor: admin / admin123
echo   Aluno: aluno1 / senha123
echo.
echo ========================================
echo Pressione CTRL+C para parar o servidor
echo ========================================
echo.

python manage.py runserver %LOCAL_IP%:8000