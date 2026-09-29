@echo off
title Setup Skill Gap Analyzer File Structure
echo Creating project directories...

:: Create directories
if not exist "datasets" mkdir "datasets"
if not exist "modules" mkdir "modules"
if not exist "assets" mkdir "assets"

echo Creating empty files...

:: Root files
if not exist "app.py" type nul > "app.py"
if not exist "requirements.txt" type nul > "requirements.txt"
if not exist ".env" type nul > ".env"

:: Dataset files
if not exist "datasets\skills_database.json" type nul > "datasets\skills_database.json"
if not exist "datasets\roles_database.json" type nul > "datasets\roles_database.json"
if not exist "datasets\job_roles.csv" type nul > "datasets\job_roles.csv"
if not exist "datasets\all_job_post.csv" type nul > "datasets\all_job_post.csv"
if not exist "datasets\coursea_data.csv" type nul > "datasets\coursea_data.csv"

:: Module files
if not exist "modules\__init__.py" type nul > "modules\__init__.py"
if not exist "modules\preprocessing.py" type nul > "modules\preprocessing.py"
if not exist "modules\extractor.py" type nul > "modules\extractor.py"
if not exist "modules\analyzer.py" type nul > "modules\analyzer.py"
if not exist "modules\roadmap.py" type nul > "modules\roadmap.py"
if not exist "modules\pdf_generator.py" type nul > "modules\pdf_generator.py"

:: Asset files
if not exist "assets\style.css" type nul > "assets\style.css"

echo Project structure created successfully!
pause