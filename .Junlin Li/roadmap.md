# FlirtNet Development Roadmap

## Current Status (as of Dec 2, 2025)

- **Frontend:** ✅ Completed (React + Vite). All major pages (Login, Register, Profile, Public Square, Chat, Connections, AI Companion) are implemented with Glassmorphism UI and mock data.
- **Backend:** ⏳ Pending.
- **Database:** ⏳ Pending.

## 1. Technology Stack Proposal

To adhere to the **MVC (Model-View-Controller)** architecture, we propose the following stack:

- **Model (Database & Data Logic):**
  - **Database:** PostgreSQL (Robust, relational database).
  - **ORM:** SQLAlchemy or Tortoise ORM (Python).
- **View (Frontend Interface):**
  - **Framework:** React.js (using Vite for fast setup).
  - **Styling:** Standard CSS or CSS Modules.
- **Controller (Backend Logic):**
  - **Server:** Python with FastAPI (High performance, easy async support).
  - **API Style:** RESTful API & WebSockets.
- **Real-time Communication:** WebSockets (Native support in FastAPI).
- **AI Integration:** OpenAI API (GPT-4o or similar) for all AI features.

## 2. Development Phases

### Phase 1: Setup & Architecture

- [ ] Initialize Git repository.
- [ ] Set up Monorepo structure (client/ and server/ folders).
- [ ] **Backend:** Initialize FastAPI app, set up folder structure (`models/`, `routers/`, `schemas/`, `database/`).
- [x] **Frontend:** Initialize React app with Vite.
- [ ] Connect Backend to Database.

### Phase 2: User Authentication & Core Models (FR-1, FR-2, FR-3)

- [ ] **Model:** Define `User` schema (username, email, password hash, profile details).
- [ ] **Controller:** Implement Auth Controller (Register, Login, JWT generation).
- [x] **View:** Create Login/Register pages and User Profile editing page.
- [ ] **Integration:** Connect Frontend Auth forms to Backend API.

### Phase 3: The Public Square (FR-10, FR-11, FR-12)

- [ ] **Model:** Define `Post` and `Comment` schemas.
- [ ] **Controller:** CRUD operations for posts (Create, Read, Update, Delete).
- [x] **View:** Public Feed component, Create Post modal.
- [ ] **Integration:** Fetch real posts from DB, handle post creation.

### Phase 4: Real-time Chat & Discovery (FR-4, FR-5, FR-6)

- [ ] **Backend:** Set up WebSocket endpoint.
- [ ] **Controller:** Implement "Matching Logic" (Queue system for random chat).
- [x] **View:** Chat Interface UI (Message bubbles, input area).
- [ ] **Feature:** Implement real-time message passing via WebSockets.

### Phase 5: Connection System (FR-7, FR-8, FR-9, FR-13)

- [ ] **Model:** Update User schema to include `connections` or create a `Connection` schema.
- [ ] **Controller:** Logic for sending/accepting "Datemate" requests.
- [x] **View:** Connections List, Private Chat view (reusing Chat Interface).
- [ ] **Integration:** Real-time friend requests and status updates.

### Phase 6: AI Features Integration (FR-16 to FR-23)

- [ ] **Backend:** Create an `AIService` to handle API calls to OpenAI.
- [ ] **Features:**
  - [ ] AI Companion / Lost Partner (Chatbot endpoints).
  - [ ] AI Wingman (Prompt engineering based on user profiles).
  - [ ] Atmosphere Analyzer (Sentiment analysis of chat logs).
  - [ ] Abuse Detector (Content moderation middleware).
- [x] **View:** AI Companion Interface.

### Phase 7: Polish & Deployment

- [x] UI/UX refinements (Glassmorphism, Animations).
- [ ] Error handling and Validation (Backend side).
- [ ] Deployment (e.g., Vercel for Frontend, Render/Heroku for Backend).
