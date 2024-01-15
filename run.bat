@echo off

set VENV_FOLDER=venv
set REQUIREMENTS_FILE=requirements.txt

rem Check if virtual environment folder exists
if not exist %VENV_FOLDER% (
    echo LOG: Virtual environment not found. Creating...
    python -m venv %VENV_FOLDER%
	echo LOG: Virtual environment created.
)

rem Activate the virtual environment
call %VENV_FOLDER%\Scripts\activate

echo LOG: Virtual environment is activated.
echo LOG: Checking if pip is in VENV.
rem Check if pip is installed in the virtual environment
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo LOG: Installing pip in the virtual environment...
    python -m ensurepip
	echo LOG: pip successfully installed.
)

rem Check if requirements are already installed
set "REQUIREMENTS_MET=true"
for /f "delims=" %%i in (%REQUIREMENTS_FILE%) do (
    set "PACKAGE_FOUND=false"
)

for /d %%p in (%VENV_FOLDER%\Lib\site-packages\*) do (
    for /f %%i in ('type %REQUIREMENTS_FILE% ^| findstr /i /c:"%%~nxp"') do (
        set "PACKAGE_FOUND=true"
        goto :PACKAGE_FOUND
    )
)
:PACKAGE_FOUND

if "%PACKAGE_FOUND%"=="false" (
    set "REQUIREMENTS_MET=false"
    echo LOG: Some requirements are missing.
)

if "%REQUIREMENTS_MET%"=="false" (
    echo LOG: Installing requirements...
    pip install -r %REQUIREMENTS_FILE%
) else (
    echo LOG: Requirements are already installed.
)

set "modelfolder=ssd_mobilenetv2_coco"

rem Check if the folder exists
if not exist "%modelfolder%" (
    echo LOG: Model folder does not exist. Creating...
    mkdir "%modelfolder%"
    if errorlevel 1 (
        echo LOG: Failed to create model folder. Aborting.
        exit /b 1
    ) else (
        echo LOG: Model folder created successfully.
    )
)

echo.
echo LOG: Starting the script
rem Run the Python script
python person_autocrop.py
