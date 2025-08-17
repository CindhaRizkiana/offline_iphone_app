import os
import subprocess
import sys
import time

def create_executable():
    """Create a standalone executable for the budget app."""
    print("Starting packaging process...")
    
    # Install PyInstaller if not already installed
    try:
        import PyInstaller
        print("PyInstaller is already installed.")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Create a wrapper script that will start the Streamlit app
    wrapper_path = "app_launcher.py"
    with open(wrapper_path, "w") as f:
        f.write("""
import os
import subprocess
import sys
import time
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    # Start Streamlit in a separate process
    streamlit_cmd = [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true"]
    
    # Open browser after a short delay
    Timer(2, open_browser).start()
    
    # Run Streamlit
    process = subprocess.Popen(streamlit_cmd)
    
    try:
        # Keep the app running until user closes it
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        process.wait()
""")
    
    # Create the spec file for PyInstaller
    spec_path = "budget_app.spec"
    with open(spec_path, "w") as f:
        f.write("""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app.py', '.'),
        ('.streamlit', '.streamlit'),
    ],
    hiddenimports=[
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'openpyxl',
        'uuid',
        'datetime',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BudgetApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BudgetApp',
)
""")
    
    # Check for and uninstall pathlib if it exists (it's incompatible with PyInstaller)
    try:
        print("Checking for pathlib package...")
        import pathlib
        print("Uninstalling pathlib package (it's incompatible with PyInstaller)...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "pathlib"])
        print("Pathlib uninstalled successfully.")
    except ImportError:
        print("Pathlib package not found, continuing with packaging...")
    
    # Run PyInstaller
    print("Building executable with PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "PyInstaller", "budget_app.spec", "--noconfirm"])
    
    print("\nPackaging complete!")
    print("Your standalone app is available in the 'dist/BudgetApp' folder.")
    print("To run the app, double-click on 'BudgetApp.exe' in that folder.")

if __name__ == "__main__":
    create_executable()
