## Prerequisites

- Node.js installed (for frontend)
- Python 3.9+ installed (for backend)

## 1. Start the Backend Server

The backend runs on port 8000.

1.  Open a terminal.
2.  Navigate to the backend directory:
    ```bash
    cd codespace/backend
    ```
3.  Activate the virtual environment:
    ```bash
    source venv/bin/activate
4.  Install dependencies (if needed):
    ```bash
    pip install -r requirements.txt
    ```
5.  Start the server:
    ```bash
    # Option A: Run directly (production-like)
    python3 -m app.main
    
    # Option B: Run with auto-reload (for development)
    uvicorn app.main:socket_app --reload --port 8000
    ```

## 2. Start the Frontend Server

The frontend runs on port 5173 (by default).

1.  Open a **new** terminal (keep the backend running).
2.  Navigate to the frontend directory:
    ```bash
    cd codespace/frontend
    ```
3.  Install dependencies (first time only):
    ```bash
    npm install
    ```
4.  Start the development server:
    ```bash
    npm run dev
    ```

## 3. Verify

- Open your browser to the URL shown in the frontend terminal (usually `http://localhost:5173`).
- The backend API docs are available at `http://localhost:8000/docs`.
- The backend root health check is at `http://localhost:8000/`.