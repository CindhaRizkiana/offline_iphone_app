
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
