# FlirtNet: We Meet. We Flirt. We Love.

**Group 2 Final Project Report**

**Date:** December 29, 2025

**Group Members:**
1.  **Jiachen Pan** (20233802046) - Backend & Frontend Engineer, Product Manager, UI Design
2.  **Junrui Liang** (20233802068) - Backend Engineer, UI Design
3.  **Hongjia Huang** (20223802016) - Database Design
4.  **Junlin Li** (20233802058) - Product Manager, Frontend Engineer
5.  **Yueshen Wang** (20233802018) - Backend Engineer

---

## Abstract

**FlirtNet** is a next-generation social discovery platform designed to address the emotional disconnection prevalent in modern dating applications. While traditional platforms like Tinder and Bumble focus on superficial matching mechanisms ("swiping"), they often fail to support users through the subsequent stages of relationship building—conversation, connection, and even closure. FlirtNet fills this gap by introducing a "Humanity Caring" philosophy, guiding users through a complete lifecycle: **Meet, Flirt, Love, and Heal**.

The system is built as a responsive web application using a modern technology stack: **React** for the frontend, **FastAPI** for the backend, and **Socket.IO** for real-time communication. Key innovations include an AI-powered **Wingman** (powered by DeepSeek LLM) that provides real-time, context-aware conversation coaching; a **Safety Monitor** that proactively detects and blocks harassment; and a unique **Miss Ex** feature that uses style-transfer AI to help users process breakups by simulating a closure conversation.

This report details the complete software development lifecycle of FlirtNet, from problem identification and requirements specification to system architecture, database design, implementation of complex algorithms, and final testing. The result is a robust, scalable, and emotionally intelligent platform that redefines how technology can support human connection.

---

## Table of Contents

1.  [Title Page](#flirtnet-we-meet-we-flirt-we-love)
2.  [Abstract](#abstract)
3.  [List of Figures](#list-of-figures)
4.  [List of Tables](#list-of-tables)
5.  [Introduction](#1-introduction)
6.  [Background / Literature Review](#2-background--literature-review)
7.  [Requirements Specification](#3-requirements-specification)
8.  [System Design](#4-system-design)
9.  [Implementation](#5-implementation)
10. [Testing & Evaluation](#6-testing--evaluation)
11. [Deployment & User Guide](#7-deployment--user-guide)
12. [Project Management](#8-project-management)
13. [Conclusion](#9-conclusion)
14. [Future Enhancements](#10-future-enhancements)
15. [References](#11-references)
16. [Appendices](#12-appendices)

---

## List of Figures
*(Note: In the actual report, these would be images. Placeholders are provided here.)*
*   Figure 1: FlirtNet "Liquid Glass" UI Concept
*   Figure 2: System Architecture Diagram (MVC Pattern)
*   Figure 3: Database Entity-Relationship (ER) Diagram
*   Figure 4: Socket.IO Matching Flowchart
*   Figure 5: AI Wingman Prompt Engineering Workflow

## List of Tables
*   Table 1: Comparison of Existing Dating Platforms
*   Table 2: Functional Requirements Matrix
*   Table 3: Database Schema - Users Table
*   Table 4: Test Case Results

---

## 1. Introduction

### Project Overview
**FlirtNet** is not just another dating app; it is a web-based social platform built with a singular mission: to help everyone find their loved one through a journey of **Humanity Caring**. In the current digital landscape, "social" apps often feel antisocial. They gamify human connection, reducing people to profile cards to be swiped left or right.

FlirtNet was created to solve this specific human problem. It is designed around the complete emotional cycle of a relationship: **Meet → Flirt → Love → Heal**.

*   **Meet**: We provide a safe space to discover new people through **Random Matching** or our vibrant **Community Square**.
*   **Flirt**: We acknowledge that dating is scary. Our AI **Wingman** is always by your side to analyze the "vibe" and help you communicate with confidence.
*   **Love**: We turn fleeting sparks into lasting flames with our **Datemate** system, offering a secure, private space for couples.
*   **Heal**: We are the first platform to care about what happens *after* a relationship. Our **Miss Ex** feature provides a safe environment for emotional closure if things go wrong.

### Problem Statement
Our project was born from a simple but profound question: **"Why is dating so scary?"**

As university students, we saw this problem effectively everywhere around us. Many of our groupmates are single, and our friends don't even dare to start dating. We identified three specific pain points that current software fails to address:

1.  **Too Shy to Start & Lack of Dating Experience**:
    Many young people struggle to meet new people. They might match with someone on a traditional app, but they freeze when it's time to start a conversation. They are afraid of saying the wrong thing, afraid of rejection, or simply don't know how to keep a conversation interesting. "Hey" is often ignored, and without guidance, potential connections die before they even begin.

2.  **Fragmented Experience & Bad Advice**:
    We watched our friends struggle with a fragmented toolset. They jump between Instagram to browse profiles, Tinder to swipe, and WhatsApp to chat. Worst of all, when they don't know what to reply, they copy-paste chat logs to their friends asking for advice. But their friends are not dating experts! This leads to "blind leading the blind," often resulting in awkwardness or misunderstanding. This process is exhausting and makes dating feel like a chore instead of a joy.

3.  **No Protection or Care (The Post-Breakup Void)**:
    Current platforms are cold. If a user is harassed, reporting is slow and manual, leaving them mentally abused by toxic content. Even worse is the lack of care when a relationship ends. When a user breaks up, typical apps just throw them back into the pool or cruelly show their ex's profile again. There is no emotional support, no closure, and no "Humanity Caring."

### Objectives
Our primary objective is to build a platform that acts as a **Companion**, not just a tool.
*   To create a unified platform that handles the entire social lifecycle.
*   To integrate **Artificial Intelligence** as a supportive coach (Wingman) and protector (Safety Monitor).
*   To design a UI that feels warm and safe, using a **Liquid Glass** aesthetic.
*   To provide a unique solution for emotional closure (**Miss Ex**).

### Scope
The project covers the development of a Full-Stack Web Application.
*   **Frontend**: A React-based Single Page Application (SPA).
*   **Backend**: A FastAPI REST API and Socket.IO real-time server.
*   **Database**: A relational database (SQLite/PostgreSQL) for user data.
*   **AI Service**: Integration with Large Language Models (LLM) for text generation and analysis.

### Stakeholders
*   **End Users (Students/Young Adults)**: The primary beneficiaries who seek meaningful connections.
*   **University Administration**: Interested in safe, controlled social environments for students.
*   **Platform Moderators**: AI acts as the first line of defense, reducing the workload for human moderators.

---

## 2. Background / Literature Review

### Existing Systems / Related Work
We analyzed the strengths and weaknesses of existing solutions to better understand where FlirtNet fits in.

*   **Tinder / Bumble (The Swiping Giants)**:
    *   *Strength*: Massive user base and efficient matching.
    *   *Weakness*: Extremely shallow. They focus 100% on the "Meet" phase and offer zero support for the "Flirt" or "Heal" phases. Once you match, you are on your own.
*   **Omegle / OmeTV (The Random Chatters)**:
    *   *Strength*: Instant connection with strangers.
    *   *Weakness*: High toxicity and zero persistence. Connections are ephemeral; if you disconnect, that person is gone forever. There is no "Datemate" concept to turn a random encounter into a relationship.
*   **Character.AI (The AI Chatbots)**:
    *   *Strength*: Great conversational AI.
    *   *Weakness*: You are chatting with fiction. It isolates users from real human connection rather than helping them find it.

**FlirtNet's Unique Position**: We combine the discovery speed of random chat, the persistence of a dating app, and the intelligence of an AI companion. We are the bridge between these isolated islands.

### Technologies and Tools Used
We selected a modern, professional, and scalable tech stack to build FlirtNet.

*   **Frontend**:
    *   **React**: Chosen for its component-based architecture, allowing us to build reusable UI elements like the "Chat Bubble" or "Glass Card."
    *   **Vite**: Used for its lightning-fast build times, significantly speeding up our development cycle.
    *   **CSS Modules**: We wrote custom CSS to implement the **Glassmorphism** heavily used in our "Liquid Glass" design. We avoided generic libraries like Bootstrap to ensure our unique aesthetic.

*   **Backend**:
    *   **FastAPI (Python)**: Selected for its high performance and ease of implementation. Python is the native language of AI, making it seamless to integrate our DeepSeek AI modules. It also provides automatic API documentation (Swagger UI), which was crucial for our frontend-backend coordination.
    *   **Socket.IO**: The backbone of our real-time features. Unlike standard HTTP requests, Socket.IO allows bi-directional communication, which is essential for instant messaging, vibe analysis, and real-time safety warnings.

*   **Database**:
    *   **SQLite**: A lightweight, file-based database used for this phase of development. It stores User data, Profiles, and Chat logs efficiently.
    *   **SQLAlchemy**: An Object-Relational Mapper (ORM) that allows us to interact with the database using Python objects. This abstraction ensures that we can migrate to PostgreSQL in the future without rewriting our backend logic.

*   **Artificial Intelligence**:
    *   **DeepSeek API**: A powerful Large Language Model (LLM) that powers our "Humanity Caring" features (Wingman, Practice Mode, Miss Ex, Report System).

---

## 3. Requirements Specification

### Functional Requirements
We defined specific functional requirements based on our "Meet → Flirt → Love → Heal" cycle.

#### 1. User Accounts & Profiles
*   **FR-1**: Users must be able to register and log in securely.
*   **FR-2**: Users must be able to create a rich profile, including gender, age, bio, and interests.
*   **FR-3 (AI Optimization)**: Users can click a button to have AI optimize their profile bio to make it more attractive.

#### 2. Discovery (The "Meet" Stage)
*   **FR-4 (Random Matching)**: The system must provide a text-only random matching function. It should prioritize compatible gender preferences.
*   **FR-5 (Community Square)**: Users can publish posts (text + images) to a public feed. Others can like and comment.
*   **FR-6**: Users can view the profiles of people they meet in Random Chat or the Community.

#### 3. Connection & Private Chat (The "Love" Stage)
*   **FR-7 (Datemate Request)**: To solve the "ephemeral" problem of random chat, users can send a "Datemate Request" to convert a stranger into a contact.
*   **FR-8**: Once a request is accepted, users become "Datemates" and unlock persistent **Private Chat**.
*   **FR-9**: Private chat history must be saved and retrievable.

#### 4. AI-Supported Features (The "Flirt" & "Heal" Stage)
*   **FR-10 (Wingman)**: In any chat, users can click "Help" to activate the Wingman. The system must analyze the chat history, determine the "Vibe," and suggest 3 context-aware flirty responses.
*   **FR-11 (Safety Check)**: The system must analyze every message sent. If it contains abusive or harassing language, it must warn the user immediately.
*   **FR-12 (Miss Ex)**: If a Datemate connection is removed (breakup), the user can access "Miss Ex". The system must simulate the ex-partner's tone based on their past chat logs.
*   **FR-13 (Practice Mode)**: Users can chat with an AI persona to practice their social skills before talking to real humans.
*   **FR-14 (Quick Report)**: Users can report bad actors. The AI must analyze the evidence and, if the user is guilty, ban them immediately.

### Non-Functional Requirements
*   **NFR-1 (Latency)**: Chat messages must appear in <100ms.
*   **NFR-2 (Scalability)**: The matching queue must handle concurrent users without race conditions.
*   **NFR-3 (Security)**: Passwords hashed with Bcrypt. JWT tokens used for session management.
*   **NFR-4 (UI Aesthetics)**: "Liquid Glass" design (Glassmorphism) to evoke warmth and romance.

### Use Case Diagrams / Scenario

To better illustrate the system functionality, we have defined key user scenarios and modeled them.

#### Scenario 1: The "Meet & Flirt" Journey
**Actor**: New User (Alice)
**Goal**: Find a romantic partner.
1.  **Registration**: Alice creates an account and sets her gender to "Female" and preference to "Male".
2.  **Profile Optimization**: Alice writes a basic bio. She clicks the **AI Magic Wand**. The system calls the DeepSeek API and rewrites her bio to be more engaging.
3.  **Discovery**: Alice enters "Random Chat". The system places her in the `waiting_queue`.
4.  **Matching**: The system finds Bob (Male, seeks Female). Both receive a `match_found` event.
5.  **Conversation**: Alice doesn't know what to say. She clicks **Wingman**. The AI suggests: *"I love your music taste! What's the last concert you went to?"*.
6.  **Connection**: They hit it off. Alice clicks **"Request Datemate"**. Bob accepts. They are now permanently connected.

#### Scenario 2: The "Heal" Journey
**Actor**: Heartbroken User (Bob)
**Goal**: Get emotional closure after a breakup.
1.  **Breakup**: Alice removes Bob from her Datemate list.
2.  **Miss Ex**: Bob feels sad and wants to talk to Alice, but can't. He goes to the **Miss Ex** feature.
3.  **Simulation**: The system loads the chat history between Bob and Alice. It fine-tunes the AI persona to mimic Alice's tone.
4.  **Closure**: Bob says *"I'm sorry it didn't work out."* The AI (simulating Alice) replies: *"It's okay, Bob. We just wanted different things. I wish you the best."* Bob feels heard and can move on.

---

## 4. System Design

### System Architecture
We followed strictly professional software engineering practices, utilizing the **MVC (Model-View-Controller)** design pattern to keep our codebase organized and maintainable.

1.  **Model (Database Layer)**:
    This layer represents our data structures. We defined SQLAlchemy models for `User`, `Profile`, `Post`, `RandomChat`, `DatemateConnection`, and `PrivateMessage`. This separation ensures that our data logic is decoupled from the business logic.

2.  **View (Frontend Layer)**:
    Built with React, this is what the user sees. It handles the rendering of our **Liquid Glass** UI. Components are modular (e.g., `ChatBubble`, `ProfileCard`, `WingmanModal`) and reusable. The View listens for real-time events from the Controller (via Socket.IO) to update the UI instantly without refreshing the page.

3.  **Controller (Backend Layer)**:
    Built with FastAPI. This layer processes business logic. It handles API requests (e.g., "Login", "Get Posts") and manages the WebSocket connections. It acts as the brain, deciding when to call the AI service, when to write to the database, and when to broadcast a message to a user.

### UML Diagrams

#### Class Diagram
插入图片

#### Sequence Diagram: Random Matching Process
插入图片

### Database Design / ER Diagram
The database is normalized to 3NF. Key tables include:

#### 1. Users Table (`users`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Unique User ID |
| `username` | String | Unique login name |
| `email` | String | User email (optional) |
| `password_hash` | String | Bcrypt hash |
| `created_at` | DateTime | Account creation time |

#### 2. Profiles Table (`profiles`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Unique Profile ID |
| `user_id` | Integer (FK) | Link to Users table |
| `display_name` | String | Public name |
| `gender` | String | "male", "female", "non-binary" |
| `preferred_gender`| String | Matching preference |
| `bio` | Text | User biography |
| `interests` | JSON | List of hobbies (e.g. ["Music", "Tech"]) |

#### 3. Datemate Connections (`datemate_connections`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Connection ID |
| `requester_id` | Integer (FK) | Who sent the request |
| `receiver_id` | Integer (FK) | Who received it |
| `status` | String | "pending", "accepted", "rejected" |

#### 4. Private Messages (`private_messages`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Message ID |
| `connection_id` | Integer (FK) | Link to Datemate Connection |
| `sender_id` | Integer (FK) | Who sent it |
| `message_text` | Text | Content |
| `sent_at` | DateTime | Timestamp |

---

### UI/UX Design: The "Liquid Glass" Philosophy
We wanted FlirtNet to feel different. Most apps use "Flat Design" which is clean but cold. For a platform about love and emotion, we needed warmth.
We adopted the **Liquid Glass (Glassmorphism)** style:
*   **Translucency**: Cards are semi-transparent with a background blur (`backdrop-filter: blur(10px)`). This creates a sense of depth and hierarchy.
*   **Gradients**: We used flowing Pink and Purple gradients. Pink represents romance/flirting, and Purple represents mystery/deep connection.
*   **Floating Animations**: Elements float gently, making the interface feel "alive" and organic, mirroring the fluid nature of human connection.

---

## 5. Implementation

### Development Approach
We followed an **Agile** methodology, iterating through "Sprints":
1.  **Sprint 1**: Backend Setup & DB Schema.
2.  **Sprint 2**: Auth & Basic Profile.
3.  **Sprint 3**: Socket.IO & Random Matching.
4.  **Sprint 4**: AI Integration (Wingman).
5.  **Sprint 5**: Frontend Polish (Glassmorphism).

### Modules Description
The system is divided into modular components to ensure maintainability and separation of concerns.

#### Backend Modules
*   **`app.main`**: The entry point of the application. It initializes the FastAPI app, mounts the Socket.IO server, and registers all API routers.
*   **`app.utils.socketio_server`**: The core real-time engine. It manages the `waiting_queue` for random matching and handles all WebSocket events (`join_queue`, `send_message`, `disconnect`).
*   **`app.utils.deepseek`**: A dedicated wrapper for the DeepSeek API. It contains specialized functions for `get_wingman_suggestion`, `check_content_safety`, and `optimize_profile`, each with custom prompt templates.
*   **`app.routers.*`**: Organized endpoints for different resources:
    *   `auth.py`: Handles JWT token generation and user registration.
    *   `datemates.py`: Manages friend requests and connection statuses.
    *   `messages.py`: Retrieves chat history from the database.

#### Frontend Modules
*   **`context/AuthContext`**: A global state provider that manages the user's login session and JWT token.
*   **`services/aiService`**: An abstraction layer that communicates with the backend AI endpoints.
*   **`pages/RandomChatPage`**: A complex component that handles the Socket.IO client connection, listening for `match_found` events and updating the UI state.

### Key Algorithms / Techniques Used

#### 1. The Matching Algorithm (`socketio_server.py`)
The core of the "Meet" phase is the random matching logic. It uses a `waiting_queue` (deque) and a compatibility check.

```python
def check_match_compatibility(user1, user2):
    # User1 wants user2's gender (or any)
    u1_ok = (user1['preferred_gender'] == 'any' or 
             user1['preferred_gender'] == user2['gender'])
    
    # User2 wants user1's gender (or any)
    u2_ok = (user2['preferred_gender'] == 'any' or 
             user2['preferred_gender'] == user1['gender'])
    
    return u1_ok and u2_ok

async def try_match_user(sid):
    # Loop through waiting queue
    for waiting_sid in waiting_queue:
        if check_match_compatibility(current_user, waiting_user):
            # MATCH FOUND!
            # 1. Create session ID
            # 2. Notify both users
            await sio.emit('match_found', { ... })
            return
```

#### 2. The AI Wingman (`deepseek.py`)
The Wingman is our flagship innovation. It is not a generic chatbot; it is prompt-engineered to be a "Dating Coach."
*   **Technique**: We use **Few-Shot Prompting** and **Context Injection**. When a user asks for help, we don't just send the last message. We package the last 10 messages of conversation history, the user's profile, and the partner's profile.
*   **The Prompt**: We instruct the AI: *"You are FlirtNet's AI Wingman - a charming, playful dating coach. Analyze the vibe of the conversation. Suggest 3 flirty responses."*
*   **Result**: The AI understands if the conversation is "Awkward," "Deep," or "Playful," and suggests replies that fit that specific mood.

#### 3. Miss Ex Feature (Emotional Closure)
This feature required complex logic to simulate a specific human.
*   **Technique**: **Style Transfer**. We fetch the historical chat logs between the user and their ex.
*   **The Prompt**: *"You are participating in a Miss Ex simulation. Strictly imitate the communication style found in this chat history. In this scenario, you ARE that person. Do not break character."*
*   **Humanity Caring**: This implementation allows users to say goodbye to a digital ghost, providing the closure that real life often denies them.

#### 4. Safety Monitor (Real-Time Protection)
*   **Technique**: **Chain-of-Thought Reasoning**. We ask the AI to analyze the message for toxicity *before* broadcasting it.
*   **Logic**: `If AI_Safety_Score < Threshold -> Block Message -> Send Warning`. This protects users from harassment proactively, rather than reacting after the damage is done.

---

## 6. Testing & Evaluation

### Test Strategy
We employed a mix of Unit Testing (Backend) and User Acceptance Testing (Frontend).

### Test Cases

| ID | Test Case | Steps | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | User Registration | Enter valid email/pass | Account created, token returned | Pass | ✅ |
| **TC-02** | Random Matching | User A joins queue. User B (compatible) joins. | Both receive `match_found` event | Pass | ✅ |
| **TC-03** | Incompatible Match | Male (seeks Female) joins. Male (seeks Female) joins. | No match. Both stay in queue. | Pass | ✅ |
| **TC-04** | Wingman Suggestion | Click "Help" in chat | 3 relevant suggestions appear | Pass | ✅ |
| **TC-05** | Safety Block | Send "You are stupid" | Message blocked, Warning shown | Pass | ✅ |

### Performance Evaluation
*   **Socket Latency**: Average message delivery time is ~45ms on local network.
*   **AI Response Time**: DeepSeek API takes ~1.5s to generate Wingman suggestions. We added a "Thinking..." animation to mask this delay.

### Results & Discussion
The final implementation of FlirtNet was subjected to rigorous testing and evaluation.

#### System Output / Screenshots
The following screenshots demonstrate the core functionalities of the system.
*(Note: Please refer to the `/frontend/public/screenshots/` directory for the actual image files)*

1.  **Registration & Profile**:
    *   `register.png`: The entry point with gender/preference selection.
    *   `profile.png`: The user dashboard showing bio and interests.
    *   `profile_optimize.png`: Demonstrates the AI rewriting a user's bio.

2.  **Discovery (The "Meet" Stage)**:
    *   `homepage.png`: The main landing page with Liquid Glass aesthetics.
    *   `community.png`: The public square feed.
    *   `randomchat_matching.png`: The queue screen while waiting for a partner.

3.  **Conversation (The "Flirt" Stage)**:
    *   `randomchat.png`: A live chat session with a stranger.
    *   `randomchat_wingman.png`: The **AI Wingman** offering 3 suggestions.
    *   `receive datemate request.png`: The modal to accept a permanent connection.

4.  **Relationship (The "Love" & "Heal" Stage)**:
    *   `datemate_list.png`: The list of connected friends.
    *   `private_chat.png`: Persistent chat history.
    *   `MissEX.png`: The emotional closure simulator.

#### Comparison with Objectives

| Objective | Status | Discussion |
| :--- | :--- | :--- |
| **Unified Platform** | ✅ Achieved | Successfully integrated Random Chat (Meet), Private Chat (Love), and Miss Ex (Heal) into one SPA. |
| **AI Support** | ✅ Achieved | The **Wingman** successfully suggests relevant replies. **Safety Monitor** blocks toxic messages in real-time. |
| **Liquid Glass UI** | ✅ Achieved | The UI uses `backdrop-filter` and gradients consistent with the design proposal. |
| **Emotional Closure** | ✅ Achieved | The **Miss Ex** feature works as intended, providing a unique "Humanity Caring" value proposition. |

---

## 7. Deployment & User Guide

### Installation Steps

**Prerequisites**: Python 3.9+, Node.js 16+, SQLite.

**Backend Setup**:
1.  Navigate to `codespace/backend`.
2.  Create virtual environment: `python -m venv venv`.
3.  Activate: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Win).
4.  Install dependencies: `pip install -r requirements.txt`.
5.  Run server: `uvicorn app.main:socket_app --reload`.
6.  Server starts at `http://localhost:8000`.

**Frontend Setup**:
1.  Navigate to `codespace/frontend`.
2.  Install packages: `npm install`.
3.  Start dev server: `npm run dev`.
4.  App runs at `http://localhost:5173`.

### User Instructions
1.  **Register**: Create an account.
2.  **Profile**: Go to "Profile" and fill in your bio. Click the **Magic Wand** icon to let AI optimize it.
3.  **Square**: Post a selfie to the Community Square.
4.  **Match**: Go to "Random Chat" and click "Start Matching".
5.  **Chat**: When matched, use the **Lightbulb** icon for AI help.
6.  **Connect**: If you like them, click "Request Datemate".

---

## 8. Project Management

### Timeline
We adhered to a strict development schedule over 7 weeks:
*   **Week 1 (Nov 06)**: Project Initialization. Drafting the Problem Statement and Proposal.
*   **Week 2 (Nov 10-17)**: Requirement Analysis. defining the "Humanity Caring" scope.
*   **Week 3 (Nov 18-24)**: Design Phase. Creating UML diagrams (Class, Use Case) and defining the database schema.
*   **Week 4 (Nov 25-Dec 02)**: Core Implementation. Building the FastAPI backend and basic React frontend.
*   **Week 5 (Dec 03-10)**: AI Integration. Integrating DeepSeek API for Wingman and Miss Ex.
*   **Week 6 (Dec 11-17)**: UI Polish. Implementing the "Liquid Glass" design and fixing Socket stability bugs.
*   **Week 7 (Dec 18-21)**: Final Testing, Report Writing, and Presentation Preparation.

### Tools & Methodology

#### Methodology: Agile Scrum
We adopted the **Agile Scrum** methodology to manage our 7-week development lifecycle efficiently.
*   **Sprints**: We divided the project into three 2-week sprints.
    *   *Sprint 1*: Core Infrastructure (DB, Auth, Socket).
    *   *Sprint 2*: Feature Implementation (Chat, Wingman).
    *   *Sprint 3*: Refinement (UI Polish, Bug Fixes).
*   **Daily Standups**: We held 15-minute daily meetings (via WeChat/Discord) to discuss "What I did yesterday," "What I will do today," and "Blockers."
*   **Pair Programming**: Complex logic like the matching algorithm was written using pair programming to ensure code quality.

#### Tools Used
*   **Version Control**: **GitHub** for code hosting and collaborative development. We used Feature Branch workflow (e.g., `feature/wingman`, `fix/socket-bug`).
*   **Design**: **Figma** for UI/UX prototyping.
*   **API Testing**: **Postman** and **Swagger UI** for testing backend endpoints.
*   **Task Management**: **Notion** Kanban board to track task status (To Do, In Progress, Done).

### Roles & Responsibilities
*   **Jiachen Pan**: Responsible for the core Backend logic (Socket.IO), Frontend integration, and overall Product Management (UI Design).
*   **Junlin Li**: Product Manager & Frontend Engineer. Focused on user flow definition and React component implementation.
*   **Junrui Liang**: Backend Engineer & UI Design. Worked on API endpoints and visual consistency.
*   **Yueshen Wang**: Backend Engineer. Specifically responsible for AI service integration and prompt tuning.
*   **Hongjia Huang**: Database Design. Managed the schema and data persistence logic.

### Challenges & Limitations
1.  **Socket Stability**: Real-time connections are fragile. We faced issues where users would get disconnected randomly. We solved this by implementing a "Reconnection" logic in our customized `socketio_server`.
2.  **AI Latency**: Large Language Models can be slow. We had to optimize our prompts to be concise to reduce generation time.
3.  **Context Window**: We cannot feed *infinite* chat history to the AI. We implemented a "Sliding Window" algorithm to only send the most relevant recent messages to the Wingman.

---

## 8. Conclusion

FlirtNet is more than code; it is a solution to a human problem.
We looked at the dating market and saw cold efficiency, fragmentation, and isolation. We responded with **Humanity Caring**.

By combining the speed of **Random Matching**, the warmth of a **Community**, and the intelligence of an **AI Wingman**, we have created a platform that doesn't just match profiles—it connects hearts. We guide the user from the terrifying first "Hello" to the comfort of a relationship, and even support them if it ends.

As we stated in our presentation:
**"No need to be afraid. We are here to help."**

---

## 9. Future Enhancements

We have a clear roadmap to make FlirtNet a professional, sustainable platform.

### Phase 1: Essential Feature Updates
*   **Multimedia Support**: Currently, chats are text-only. We plan to add image and voice message support to make conversations richer.
*   **Safety Tools**: Add a "Blacklist" functionality and allow users to delete Datemates.
*   **Account Security**: Implement email-based password reset.

### Phase 2: Monetization (Pro Plan)
To ensure long-term sustainability, we will introduce a **Pro Subscription**.
*   **Free Users**: Limited daily random matches and Wingman uses.
*   **Pro Users**: Unlimited Random Chats, Unlimited Wingman assistance, Unlimited Profile Optimization, and exclusive access to the sensitive **Miss Ex** feature.

### Phase 3: Professionalism & Scale
*   **Database Migration**: We will migrate from SQLite to **PostgreSQL** to handle higher concurrency and data volume.
*   **Mobile App**: We will build native iOS/Android apps using React Native to better support push notifications.
*   **Public Access**: We will deploy the server to a public cloud IP to allow real-world users to connect.

---

## 10. References
1.  **FastAPI Documentation**: https://fastapi.tiangolo.com/
2.  **React Documentation**: https://react.dev/
3.  **Socket.IO Documentation**: https://socket.io/docs/v4/
4.  **DeepSeek API Documentation**: https://platform.deepseek.com/
5.  **Design Patterns**: Elements of Reusable Object-Oriented Software (Gamma et al.)

---

## 11. Appendices

### User Guide: How to use FlirtNet
1.  **Register**: Create an account and set your gender/preference.
2.  **Optimize**: Go to Profile and let AI polish your bio.
3.  **Meet**: Click "Random Match" to find a partner.
4.  **Flirt**: Stuck? Click the **Wingman** (Lightbulb icon) for advice.
5.  **Love**: Click "Send Datemate Request" to make it official.
6.  **Heal**: If it doesn't work out, use "Miss Ex" to find closure.