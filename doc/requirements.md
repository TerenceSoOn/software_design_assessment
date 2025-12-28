# Requirements for FlirtNet

The function overview of FlirtNet can be simply understood as a high‑level summary of these requirements:

- Randomly matched chat, and enter private chat. Can send datemate request after chat.
- Users are allowed to post (text and images), and other users can like, comment, or try to start a private chats with poster.
- Personal profile pages and photo walls.
- Private chat between datemates.
- AI assistant: 
  - AI companion when no one matches
  - Missed EX
  - AI matching help
  - AI wingman
  - Atmosphere analyzer
  - Profile optimizer
  - AI practice mode

## 1. Functional Requirements

### 1.1 User Accounts and Profiles
- **FR‑1**: The system should allow users to register an account and log in.
- **FR‑2**: The system should allow users to edit their personal profile (basic info, interests, etc.).
- **FR‑3**: The system should allow users to manage a photo wall or avatar.

### 1.2 Discovery (Random Matching)
- **FR‑4**: The system should provide a text-only random matching function where users are automatically paired with an available partner.
- **FR‑5**: Once matched, the system should immediately start a one‑to‑one chat session.
- **FR‑6**: During the chat, users can view basic information about the other user.

### 1.3 Connection System
- **FR‑7**: After a good random chat, a user can send a **datemate request** to the other user to establish a long-term connection.
- **FR‑8**: The system must require the other user to explicitly **accept** or **reject** the datemate request.
- **FR‑9**: If a datemate request is accepted, both users should appear in each other’s **Datemate List**.

### 1.4 Public Square (Posts and Discussions)
- **FR‑10**: The system should allow users to post, which includes text and images.
- **FR‑11**: The system should allow other users to like and comment on posts.
- **FR‑12**: The system should allow users to look through posts and follow topics or tags.


### 1.5 Private Messaging
- **FR‑13**: The system should allow two connected users (datemates) to send one‑to‑one private messages.
- **FR‑14**: The system should notify users when they receive new messages.

### 1.6 AI‑Supported Features
- **FR‑16**: If a user cannot find any datemate for long time, the system will give a option that user whether need to chat with an **AI Companion** or not.
- **FR‑17**: The system should provide an **Miss ex** option, where AI can imitate tone and style of user’s ex based on their chat history (only if the user agrees and data use is allowed).
- **FR‑19**: The system should provide an **AI Wingman** that suggests opening lines or topics based on the other user’s profile.
- **FR‑20**: The system should provide an **Atmosphere Analyzer** that gives feedback during the conversation.
- **FR‑21**: The system should provide an **AI Profile Optimizer** that gives tips on how to improve the user’s profile.
- **FR‑22**: The system should provide an **AI Practice Mode** for users to practice chatting with AI before talking to real people.
- **FR‑23**: The system should provide an **AI Abuse & Harassment Detector** that analyzes messages and public posts in near real time to flag abusive / harassing / aggressive content and suggest actions (auto warning, temporary hiding, or prompt user to report). It should focus on context (tone, repeated patterns) not only keywords.

## 2. Non‑Functional Requirements

These requirements describe qualities of the system instead of specific features.

### 2.1 Usability
- **NFR‑1**: The user interface should be simple enough so that a new user can understand the basic functions without reading a long manual.
- **NFR‑2**: The system should support common screen sizes (for example, desktop and mobile).

### 2.2 Performance
- **NFR‑3**: Normally, opening a chat or sending a message should feel fast (for example, respond within a few seconds).

### 2.3 Security and Privacy
- **NFR‑4**: Users should log in with a password or other basic authentication.
- **NFR‑5**: User data such as messages and profiles should not be visible to people who are not allowed to see.
- **NFR‑6**: The system should allow users to report and block other users who behave badly.

### 2.4 Reliability
- **NFR‑7**: The system should try to avoid losing important data such as connection lists and message history.

### 2.5 Future Scalability and Maintainability
- **NFR‑8**: The design should allow us to add more new features in thr future without rebuliding everything.