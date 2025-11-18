# Requirements for FlirtNet

The function overview of FlirtNet can be simply understood as a high‑level summary of these requirements:

- Randomly matched chat, users can choose OK/Not OK, and enter private chat after users both agreeing.
- Users are allowed to post (text and images), and other users can like, comment, or try to start a private chats with poster.
- Personal profile pages and photo walls.
- Private chat and group chat.
- AI assistant: 
  - AI companion when no one matches
  - AI "lost partner"
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
- **FR‑4**: The system should provide a text-only random matching function, the user can choose **OK** or **Not OK**.
- **FR‑5**: Before starting a chat, the system should show some basic information of the other user.
- **FR‑6**: If both users choose **OK**, the system should connect them and start a one‑to‑one chat.

### 1.3 Connection System
- **FR‑7**: After a good random chat, user is allowed to send a connection (friend) request to the other user.
- **FR‑8**: The system should allow the other user to accept or reject the connection request.
- **FR‑9**: If a connection request is accepted, both users should appear in each other’s **Connections List**.

### 1.4 Public Square (Posts and Discussions)
- **FR‑10**: The system should allow users to post, which includes text and images.
- **FR‑11**: The system should allow other users to like and comment on posts.
- **FR‑12**: The system should allow users to look through posts and follow topics or tags.


### 1.5 Private Messaging and Group Chat
- **FR‑13**: The system should allow two connected users to send one‑to‑one private messages.
- **FR‑14**: The system should notify users when they receive new messages.
- **FR‑15**: The system should support group chats, users can choose to create group chats.

### 1.6 AI‑Supported Features
- **FR‑16**: If a user cannot match others for a long time, the system will give a option that user whether need to chat with an **AI Companion** or not.
- **FR‑17**: The system should provide an **Miss ex** option, where AI can imitate tone and style of user’s ex based on their chat history (only if the user agrees and data use is allowed).
- **FR‑18**: The system should provide an **Intelligent Matching Assistant** that suggest better matches according to user's porfile.
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