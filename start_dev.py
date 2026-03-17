import os
import socket
import subprocess
import time
import signal
import sys
from pathlib import Path

def get_lan_ip():
    """Get the local LAN IP address, prioritizing Wi-Fi (en0) on macOS."""
    try:
        # First try getting the Wi-Fi IP explicitly (macOS specific)
        result = subprocess.run(['ipconfig', 'getifaddr', 'en0'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
            
        # Fallback: Get all IPs and pick the first "real" LAN one (192.168.x.x, 10.x.x.x)
        # Avoid 127.0.0.1 and 198.x.x.x (internal benchmarking)
        hostname = socket.gethostname()
        ips = socket.gethostbyname_ex(hostname)[2]
        
        for ip in ips:
            if ip.startswith("192.168.") or ip.startswith("10.") or (ip.startswith("172.") and int(ip.split('.')[1]) in range(16, 32)):
                return ip
                
        return "127.0.0.1"
    except Exception:
        return "127.0.0.1"

def setup_backend():
    """Setup backend: create venv if needed, install dependencies."""
    root_dir = Path(__file__).resolve().parent
    backend_dir = root_dir / "codespace" / "backend"
    venv_dir = backend_dir / "venv"
    venv_python = venv_dir / "bin" / "python"
    venv_python3 = venv_dir / "bin" / "python3"
    requirements_file = backend_dir / "requirements.txt"

    # Prefer python (always present), fallback to python3
    if venv_python3.exists():
        venv_python = venv_python3
    
    # Check if venv exists
    if not venv_python.exists():
        print("📦 Creating virtual environment...")
        result = subprocess.run(
            [sys.executable, "-m", "venv", str(venv_dir)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ Failed to create venv: {result.stderr}")
            return False
        print("✅ Virtual environment created")

    # Re-resolve python path after venv creation
    if venv_python3.exists():
        venv_python = venv_python3
    
    # Check if dependencies need to be installed
    result = subprocess.run(
        [str(venv_python), "-c", "import bcrypt; import fastapi; import uvicorn"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("📦 Installing backend dependencies...")
        result = subprocess.run(
            [str(venv_python), "-m", "pip", "install", "-r", str(requirements_file)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
        print("✅ Dependencies installed")
    else:
        print("✅ Backend dependencies OK")
    
    # Check frontend node_modules
    frontend_dir = root_dir / "codespace" / "frontend"
    node_modules = frontend_dir / "node_modules"
    
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        result = subprocess.run(
            ["npm", "install"],
            cwd=str(frontend_dir),
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ Failed to install npm packages: {result.stderr}")
            return False
        print("✅ Frontend dependencies installed")
    else:
        print("✅ Frontend dependencies OK")
    
    return True

def update_frontend_env(ip):
    """Update the frontend .env file with the new IP."""
    root_dir = Path(__file__).resolve().parent
    env_path = root_dir / "codespace" / "frontend" / ".env"
    new_url = f"http://{ip}:8000"
    
    print(f"📝 Updating frontend config to use IP: {ip}")
    
    with open(env_path, "w") as f:
        f.write(f"VITE_API_URL={new_url}\n")

def run_services(ip):
    """Start backend and frontend services."""
    root_dir = Path(__file__).resolve().parent
    backend_dir = root_dir / "codespace" / "backend"
    frontend_dir = root_dir / "codespace" / "frontend"
    venv_python = backend_dir / "venv" / "bin" / "python"
    venv_python3 = backend_dir / "venv" / "bin" / "python3"
    if venv_python3.exists():
        venv_python = venv_python3
    
    print("🚀 Starting Backend...")
    backend_process = subprocess.Popen(
        [
            str(venv_python),
            "-m",
            "uvicorn",
            "app.main:socket_app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
            "--reload",
        ],
        cwd=str(backend_dir),
        preexec_fn=os.setsid,
    )
    
    print("🚀 Starting Frontend...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev", "--", "--host"],
        cwd=str(frontend_dir),
        preexec_fn=os.setsid,
    )
    
    print(f"\n✅ Services started!")
    print(f"📱 Access the app at: http://{ip}:5173")
    print(f"🔌 API running at: http://{ip}:8000")
    print("\nPress Ctrl+C to stop all services...")
    
    try:
        while True:
            time.sleep(1)
            backend_code = backend_process.poll()
            frontend_code = frontend_process.poll()

            if backend_code is not None:
                print(f"\n❌ Backend exited (code {backend_code}). Stopping frontend...")
                break
            if frontend_code is not None:
                print(f"\n❌ Frontend exited (code {frontend_code}). Stopping backend...")
                break
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")

    # Shared shutdown path (either Ctrl+C or one process exited)
    try:
        os.killpg(os.getpgid(backend_process.pid), signal.SIGTERM)
    except (ProcessLookupError, OSError):
        pass
    try:
        os.killpg(os.getpgid(frontend_process.pid), signal.SIGTERM)
    except (ProcessLookupError, OSError):
        pass
    sys.exit(0)

if __name__ == "__main__":
    # Setup backend (create venv + install deps if needed)
    if not setup_backend():
        sys.exit(1)
    
    # Use LAN IP for network access (uncomment hostname for stable sessions)
    current_ip = get_lan_ip() 
    # current_ip = "HUAWEI-Mate-Book-Pro.local"
    # current_ip = socket.gethostname() + ".local" # Alternative auto-detection
    
    print(f"🔍 Using LAN IP: {current_ip}")
    
    # Update config
    update_frontend_env(current_ip)
    
    # Run services
    run_services(current_ip)
