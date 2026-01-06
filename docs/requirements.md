# Requirements for FlirtNet

The function overview of FlirtNet can be simply understood as a high‑level summary of these requirements:

- Randomly matched chat, and enter private chat. Can send datemate request after chat.
- Users are allowed to post (text and images), and other users can like, comment, or try to start a private chats with poster.
- Personal profile pages with bio, interests, and preferences.
- Private chat between datemates.
- Humanity Caring Features: 
  - Practice Mode for shy users
  - Miss Ex for emotional closure
  - Wingman for conversation coaching
  - Profile Optimizer
  - Quick Report with instant judgment

## 1. Functional Requirements

### 1.1 User Accounts and Profiles
- **FR‑1**: The system shall allow users to register an account and log in securely.
- **FR‑2**: The system shall allow users to create and edit their personal profile (display name, bio, interests, age, gender, preferred gender, location).
- **FR‑3**: The system shall allow users to set their avatar.

### 1.2 Discovery (Random Matching)
- **FR‑4**: The system shall provide a text-only random matching function where users are automatically paired with a compatible partner based on gender preferences.
- **FR‑5**: Once matched, the system shall immediately start a one‑to‑one chat session via WebSocket.
- **FR‑6**: During the chat, users shall be able to view basic profile information of the other user.

### 1.3 Datemate Connection System
- **FR‑7**: After a random chat, a user can send a **Datemate Request** to the other user to establish a long-term connection.
- **FR‑8**: The system shall require the receiver to explicitly **accept** or **reject** the datemate request.
- **FR‑9**: If a datemate request is accepted, both users shall appear in each other's **Datemate List**.

### 1.4 Community Square (Posts and Discussions)
- **FR‑10**: The system shall allow users to publish posts, which include text and optional images.
- **FR‑11**: The system shall allow other users to like and comment on posts.
- **FR‑12**: Users shall be able to send Datemate Requests to post authors from the Community Square.

### 1.5 Private Messaging
- **FR‑13**: The system shall allow two connected users (datemates) to send one‑to‑one private messages.
- **FR‑14**: Private chat history shall be persisted and retrievable.

### 1.6 Humanity Caring Features

#### 1.6.1 Practice Mode
- **FR‑15**: The system shall provide a **Practice Mode** where users can practice chatting with a persona before talking to real people.

#### 1.6.2 Wingman (Conversation Coach)
- **FR‑16**: The system shall provide a **Wingman** feature that analyzes the chat conversation and suggests context-aware flirty responses.
- **FR‑17**: The Wingman shall be available in both Random Chat and Private Chat.

#### 1.6.3 Miss Ex (Emotional Closure)
- **FR‑18**: The system shall provide a **Miss Ex** feature that simulates a past partner's tone and style based on chat history.
- **FR‑19**: Miss Ex shall only be available for users who have removed a datemate connection.

#### 1.6.4 Profile Optimizer
- **FR‑20**: The system shall provide a **Profile Optimizer** that gives suggestions on how to improve the user's bio.

#### 1.6.5 Report System
- **FR‑21**: The system shall allow users to report other users for abusive or harassing behavior.
- **FR‑22**: Upon receiving a report, the system shall analyze the chat history and determine if the reported user is guilty.
- **FR‑23**: If guilty, the reported user's account shall be banned immediately.

## 2. Non‑Functional Requirements

### 2.1 Usability
- **NFR‑1**: The user interface shall follow a "Liquid Glass" (Glassmorphism) design aesthetic with pink/purple gradients to create a warm, romantic atmosphere.
- **NFR‑2**: The system shall be responsive and support desktop browsers. Mobile optimization is planned for future releases.

### 2.2 Performance
- **NFR‑3**: Chat messages shall be delivered in near real-time via Socket.IO (target latency < 100ms on local network).
- **NFR‑4**: Wingman suggestions shall be generated within 2 seconds.

### 2.3 Security and Privacy
- **NFR‑5**: User passwords shall be hashed using bcrypt before storage.
- **NFR‑6**: API authentication shall use JWT tokens.
- **NFR‑7**: User data such as messages and profiles shall only be accessible to authorized users.

### 2.4 Reliability
- **NFR‑8**: The system shall persist all private chat history to the database.
- **NFR‑9**: Random chat history shall be preserved and transferred to private messages upon becoming datemates.

### 2.5 Maintainability and Scalability
- **NFR‑10**: The system shall follow MVC architecture pattern for separation of concerns.
- **NFR‑11**: The database layer shall use SQLAlchemy ORM to enable easy migration from SQLite to PostgreSQL.