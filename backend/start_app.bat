@echo off
echo Starting Legal Drafting LLM...

:: Start Backend
start "Legal Drafting Backend" cmd /k "py main.py"

:: Start Frontend
cd frontend
start "Legal Drafting Frontend" cmd /k "npm run dev"

echo.
echo ====================================================
echo App is starting!
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo ====================================================
pause
