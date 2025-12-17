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

def check_dependencies():
    """Check if backend dependencies are installed."""
    print("🔍 Checking dependencies...")
    venv_python = os.path.join("codespace", "backend", "venv", "bin", "python3")
    
    if not os.path.exists(venv_python):
        print("❌ Virtual environment not found. Run: cd codespace/backend && python3 -m venv venv")
        return False
    
    # Check if bcrypt is installed with correct version
    result = subprocess.run(
        [venv_python, "-c", "import bcrypt; print(bcrypt.__version__)"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ Dependencies not installed. Run: cd codespace/backend && source venv/bin/activate && pip install -r requirements.txt")
        return False
    
    print("✅ Dependencies OK")
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
    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)
    
    # Get current IP
    current_ip = get_lan_ip()
    print(f"🔍 Detected LAN IP: {current_ip}")
    
    # Update config
    update_frontend_env(current_ip)
    
    # Run services
    run_services(current_ip)
