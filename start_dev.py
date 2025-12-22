import os
import socket
import subprocess
import time
import signal
import sys

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
    backend_dir = os.path.join("codespace", "backend")
    venv_dir = os.path.join(backend_dir, "venv")
    venv_python = os.path.join(venv_dir, "bin", "python3")
    requirements_file = os.path.join(backend_dir, "requirements.txt")
    
    # Check if venv exists
    if not os.path.exists(venv_python):
        print("📦 Creating virtual environment...")
        result = subprocess.run(
            ["python3", "-m", "venv", venv_dir],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ Failed to create venv: {result.stderr}")
            return False
        print("✅ Virtual environment created")
    
    # Check if dependencies need to be installed
    result = subprocess.run(
        [venv_python, "-c", "import bcrypt; import fastapi; import uvicorn"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("📦 Installing backend dependencies...")
        pip_path = os.path.join(venv_dir, "bin", "pip")
        result = subprocess.run(
            [pip_path, "install", "-r", requirements_file],
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
    frontend_dir = os.path.join("codespace", "frontend")
    node_modules = os.path.join(frontend_dir, "node_modules")
    
    if not os.path.exists(node_modules):
        print("📦 Installing frontend dependencies...")
        result = subprocess.run(
            ["npm", "install"],
            cwd=frontend_dir,
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
    env_path = os.path.join("codespace", "frontend", ".env")
    new_url = f"http://{ip}:8000"
    
    print(f"📝 Updating frontend config to use IP: {ip}")
    
    with open(env_path, "w") as f:
        f.write(f"VITE_API_URL={new_url}\n")

def run_services(ip):
    """Start backend and frontend services."""
    backend_cmd = f"source codespace/backend/venv/bin/activate && cd codespace/backend && uvicorn app.main:socket_app --host 0.0.0.0 --port 8000 --reload"
    frontend_cmd = f"cd codespace/frontend && npm run dev -- --host"
    
    print("🚀 Starting Backend...")
    backend_process = subprocess.Popen(backend_cmd, shell=True, executable="/bin/zsh", preexec_fn=os.setsid)
    
    print("🚀 Starting Frontend...")
    frontend_process = subprocess.Popen(frontend_cmd, shell=True, executable="/bin/zsh", preexec_fn=os.setsid)
    
    print(f"\n✅ Services started!")
    print(f"📱 Access the app at: http://{ip}:5173")
    print(f"🔌 API running at: http://{ip}:8000")
    print("\nPress Ctrl+C to stop all services...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        try:
            os.killpg(os.getpgid(backend_process.pid), signal.SIGTERM)
        except (ProcessLookupError, OSError):
            pass  # Process already terminated
        try:
            os.killpg(os.getpgid(frontend_process.pid), signal.SIGTERM)
        except (ProcessLookupError, OSError):
            pass  # Process already terminated
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
