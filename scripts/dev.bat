@echo off
REM Font Analyzer - Development Scripts for Windows (UV)

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="install-dev" goto install-dev
if "%1"=="test" goto test
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="type-check" goto type-check
if "%1"=="clean" goto clean
if "%1"=="run-example" goto run-example
if "%1"=="dev-check" goto dev-check

:help
echo Font Analyzer - Development Commands (Windows - UV)
echo ======================================================
echo Available commands:
echo   install      - Install production dependencies
echo   install-dev  - Install development dependencies
echo   test         - Run tests
echo   lint         - Run linting
echo   format       - Format code with black
echo   type-check   - Run type checking
echo   clean        - Clean up build artifacts
echo   run-example  - Run example analysis
echo   dev-check    - Run all development checks
echo.
echo Usage: scripts\dev.bat ^<command^>
goto end

:install
echo Installing production dependencies...
uv sync --no-dev
goto end

:install-dev
echo Installing development dependencies...
uv sync
uv run pre-commit install
echo Development environment ready!
goto end

:test
echo Running tests...
uv run python -m unittest tests.test_font_analyzer -v
goto end

:lint
echo Running linting...
uv run flake8 src tests --max-line-length=88 --extend-ignore=E203,W503
goto end

:format
echo Formatting code...
uv run black src tests
goto end

:type-check
echo Running type checking...
uv run mypy src
goto end

:clean
echo Cleaning up build artifacts...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /r . %%f in (*.pyc) do @if exist "%%f" del /q "%%f"
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist htmlcov rd /s /q htmlcov
if exist .coverage del .coverage
echo Cleanup complete!
goto end

:run-example
echo Running example font analysis...
uv run python -m font_analyzer.main --font_path "fonts/AkzidenzGrotesk-Regular.woff"
goto end

:dev-check
echo Running all development checks...
call %0 format
call %0 lint
call %0 type-check
call %0 test
echo All checks complete!
goto end

:end
