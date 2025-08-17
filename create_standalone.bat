@echo off
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Uninstalling pathlib (required for PyInstaller to work)...
"C:\Users\user1\Desktop\streamlit_updated\env\Scripts\python.exe" -m pip uninstall -y pathlib

echo.
echo Creating standalone executable...
python package_app.py

echo.
echo Done! Press any key to exit.
pause > nul
