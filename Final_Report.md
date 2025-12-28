# FlirtNet: We Meet. We Flirt. We Love.

**Group 2 Final Project Report**

**Date:** December 28, 2025

**Group Members:**
1.  **Jiachen Pan** (20233802046) - Backend & Frontend Engineer, Product Manager, UI Design
2.  **Junrui Liang** (20233802068) - Backend Engineer, UI Design
3.  **Hongjia Huang** (20223802016) - Database Design
4.  **Junlin Li** (20233802058) - Product Manager, Frontend Engineer
5.  **Yueshen Wang** (20233802018) - Backend Engineer

---

## 1. Introduction

### Project Overview: A Platform for Connection, Not Just Matching
**FlirtNet** is not just another dating app; it is a web-based social platform built with a singular mission: to help everyone find their loved one through a journey of **Humanity Caring**.

In the current digital landscape, "social" apps often feel antisocial. They gamify human connection, reducing people to profile cards to be swiped left or right. We realized that while there are many apps for "matching," there was no unified experience for the entire journey of a relationship. Users are left to navigate the awkwardness of the first "Hello," the anxiety of early dating, and the crushing void of a breakup entirely on their own.

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
*   To integrate **Artificial Intelligence** not as a gimmick, but as a supportive coach (Wingman) and protector (Safety Monitor).
*   To design a UI that feels warm, romantic, and safe—specifically using a **Liquid Glass** aesthetic to differ from the cold, corporate look of other apps.
*   To provide a unique solution for emotional closure (**Miss Ex**) that has never been seen in the market.

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
*   **NFR-1 (Usability - Liquid Glass)**: The UI must use translucent cards, blur effects, and pink/purple gradients to create a warm, romantic atmosphere. It must not look like a spreadsheet or a corporate dashboard.
*   **NFR-2 (Real-Time Performance)**: Chat messages must appear instantly (<100ms latency) to ensure a smooth conversation flow.
*   **NFR-3 (Safety)**: User passwords must be hashed using Bcrypt. Chat data must be protected.

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

### UI/UX Design: The "Liquid Glass" Philosophy
We wanted FlirtNet to feel different. Most apps use "Flat Design" which is clean but cold. For a platform about love and emotion, we needed warmth.
We adopted the **Liquid Glass (Glassmorphism)** style:
*   **Translucency**: Cards are semi-transparent with a background blur (`backdrop-filter: blur(10px)`). This creates a sense of depth and hierarchy.
*   **Gradients**: We used flowing Pink and Purple gradients. Pink represents romance/flirting, and Purple represents mystery/deep connection.
*   **Floating Animations**: Elements float gently, making the interface feel "alive" and organic, mirroring the fluid nature of human connection.

### Database Design / ER Diagram
Our database is designed to support the complex relationships of a social network.
*   **Users & Profiles**: A one-to-one relationship. Partitioning this data allows us to load the lightweight `User` object for authentication without loading the heavy `Profile` data every time.
*   **Datemate Connections**: A self-referential many-to-many relationship on the `Users` table. A custom association table `DatemateConnection` tracks the status (`pending`, `accepted`, `rejected`) and timestamps.
*   **Chat History**: We maintain two separate stores. `RandomChatHistory` is temporary and optimized for write speed. `PrivateMessage` is persistent and indexed for retrieval. When two users become Datemates, their `RandomChatHistory` is migrated to `PrivateMessage` so the memory of their first meeting is preserved—a key part of our "Humanity Caring" philosophy.

---

## 5. Implementation

### Development Approach
We used an efficient, iterative development methodology. We started with the core **Model** (Database), then built the **Controller** (API), and finally the **View** (Frontend). This matched our flow of "Data -> Logic -> Interface."

### Modules Description & Key Techniques

#### 1. Real-Time Chat Engine (`socketio_server.py`)
This module is the heartbeat of FlirtNet. Implementing real-time chat requires more than just sending text; it requires managing statefulness in a stateless web environment.
*   **The Queue System**: We implemented a `waiting_queue` for random matching. When a user creates a socket connection, they join this queue.
*   **Matching Algorithm**: The backend continuously checks the queue. It doesn't just match random people; it checks **Gender Compatibility**.
    *   *Logic*: User A is matched with User B if and only if User A matches User B's preference AND User B matches User A's preference.
*   **Event Broadcasting**: We use specific event channels (`receive_message`, `match_found`, `partner_left`) to trigger precise UI updates on the client.

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
Our testing strategy focused on ensuring both technical stability and "Humanity" alignment.
1.  **Unit Testing**: We tested individual backend functions, such as the matching algorithm, to ensure gender preferences were respected.
2.  **Integration Testing**: We verified that the Frontend correctly communicates with the Backend. For example, ensuring that when a "Datemate Request" is sent, the database updates the status to `pending` and the partner receives a real-time notification.
3.  **"Red Teaming" (AI Safety)**: We actively tried to break our own system. We sent slang/subtle insults to the Safety Monitor to see if it would catch them. We optimized the prompts until the AI could detect manipulation and harassment effectively.

### Results & Discussion
*   **System Stability**: The Socket.IO server successfully handles user disconnections (e.g., closing the tab). It correctly alerts the partner and moves the user out of the active chat list, preventing "zombie" connections.
*   **AI Performance**: The Wingman feature successfully generates distinct suggestions. In testing, it correctly identified an "awkward" silence and suggested a lighthearted joke to break the ice.
*   **Latency**: Messages are delivered instantly. The AI analysis takes about 1-2 seconds, which we handled in the UI with a "Wingman is thinking..." animation, maintaining a smooth user experience.
*   **Humanity Caring**: The "Miss Ex" feature was tested with sample chat logs. The AI successfully adopted the "tone" of the ex-partner (e.g., being short and cold, or warm and sad), effectively creating the simulation we aimed for.

### Comparison with Objectives
We have successfully met our primary objectives.
*   The **Meet → Flirt → Love → Heal** cycle is fully functional.
*   The **Liquid Glass** UI provides the warm, romantic aesthetic we envisioned.
*   The **AI Features** (Wingman, Miss Ex) work as intended, providing the support and care that standard apps lack.

---

## 7. Project Management

### Timeline
We adhered to a strict development schedule over 7 weeks:
*   **Week 1 (Nov 06)**: Project Initialization. Drafting the Problem Statement and Proposal.
*   **Week 2 (Nov 10-17)**: Requirement Analysis. defining the "Humanity Caring" scope.
*   **Week 3 (Nov 18-24)**: Design Phase. Creating UML diagrams (Class, Use Case) and defining the database schema.
*   **Week 4 (Nov 25-Dec 02)**: Core Implementation. Building the FastAPI backend and basic React frontend.
*   **Week 5 (Dec 03-10)**: AI Integration. Integrating DeepSeek API for Wingman and Miss Ex.
*   **Week 6 (Dec 11-17)**: UI Polish. Implementing the "Liquid Glass" design and fixing Socket stability bugs.
*   **Week 7 (Dec 18-21)**: Final Testing, Report Writing, and Presentation Preparation.

### Roles & Responsibilities
*   **Jiachen Pan**: Team Lead. Responsible for the core Backend logic (Socket.IO), Frontend integration, and overall Product Management (UI Design).
*   **Junlin Li**: Product Manager & Frontend Engineer. Focused on user flow definition and React component implementation.
*   **Junrui Liang**: Backend Engineer & UI Design. Worked on API endpoints and visual consistency.
*   **Yueshen Wang**: Backend Engineer. Specifically responsible for AI service integration and prompt tuning.
*   **Hongjia Huang**: Database Design. Managed the schema and data persistence logic.

### Challenges & Limitations
1.  **Socket Stability**: Real-time connections are fragile. We faced issues where users would get disconnected randomly. We solved this by implementing a "Reconnection" logic in our customized `socketio_server`.
2.  **AI Latency**: Large Language Models can be slow. We had to optimize our prompts to be concise to reduce generation time.
3.  **Context Window**: We cannot feed *infinite* chat history to the AI. We implemented a "Sliding Window" algorithm to only send the most relevant recent messages to the Wingman.

---

## 8. Future Enhancements

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

## 9. Conclusion

FlirtNet is more than code; it is a solution to a human problem.
We looked at the dating market and saw cold efficiency, fragmentation, and isolation. We responded with **Humanity Caring**.

By combining the speed of **Random Matching**, the warmth of a **Community**, and the intelligence of an **AI Wingman**, we have created a platform that doesn't just match profiles—it connects hearts. We guide the user from the terrifying first "Hello" to the comfort of a relationship, and even support them if it ends.

As we stated in our presentation:
**"No need to be afraid. We are here to help."**

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
