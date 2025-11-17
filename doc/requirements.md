# Requirements for FlirtNet

The short function overview of the system (previously in `function_list.md`) can be understood as a high‑level summary of these requirements:

- Random matching to chat with an OK/Not OK choice and private chat after both agree.
- A place for users to publish posts (text and images), and let others like, comment, or start private chats if both users agree.
- Personal profile pages and photo walls.
- Private chat and group chat.
- Several AI features: AI companion when no one matches, AI "lost partner", AI matching help, AI wingman, atmosphere analyzer, profile optimizer, and practice with AI.

## 1. Functional Requirements

### 1.1 User Accounts and Profiles
- **FR‑1**: The system should allow users to register an account and log in.
- **FR‑2**: The system should allow users to edit their personal profile (basic info, interests, etc.).
- **FR‑3**: The system should allow users to manage a photo wall or profile pictures.

### 1.2 Discovery (Random Matching)
- **FR‑4**: The system should provide a text‑only random matching function where two users can be matched to chat.
- **FR‑5**: Before starting a chat, the system should show some basic information of the other user so that the user can choose **OK** or **Not OK**.
- **FR‑6**: If both users choose **OK**, the system should connect them and start a one‑to‑one chat.

### 1.3 Connection System
- **FR‑7**: After a good random chat, a user should be able to send a connection (friend) request to the other user.
- **FR‑8**: The system should allow the other user to accept or reject the connection request.
- **FR‑9**: If a connection request is accepted, both users should appear in each other’s **Connections List**.

### 1.4 Public Square (Posts and Discussions)
- **FR‑10**: The system should allow users to create posts that include text and images.
- **FR‑11**: The system should allow other users to like and comment on posts.
- **FR‑12**: The system should allow users to browse posts and follow topics or tags.

### 1.5 Private Messaging and Group Chat
- **FR‑13**: The system should allow two connected users to send one‑to‑one private messages.
- **FR‑14**: The system should notify users when they receive new messages.
- **FR‑15**: The system should support basic group chats so that a small group of users can chat together.

### 1.6 AI‑Supported Features
- **FR‑16**: If a user cannot find a match for a long time, the system should offer an **AI Companion** that can chat with the user.
- **FR‑17**: The system should provide an **AI Legacy Partner** option, where the AI can imitate a past partner’s tone based on their chat history (only if the user agrees and data use is allowed).
- **FR‑18**: The system should provide an **Intelligent Matching Assistant** that uses user information to suggest better matches.
- **FR‑19**: The system should provide an **AI Wingman** that suggests opening lines or topics based on the other user’s profile.
- **FR‑20**: The system should provide an **Atmosphere Analyzer** that gives feedback on the mood of the conversation.
- **FR‑21**: The system should provide an **AI Profile Optimizer** that gives tips on how to improve the user’s profile.
- **FR‑22**: The system should provide an **AI Practice Mode** for users to practice chatting with AI before talking to real people.

## 2. Non‑Functional Requirements

These requirements describe qualities of the system instead of specific features.

### 2.1 Usability
- **NFR‑1**: The user interface should be simple enough so that a new user can understand the basic functions without reading a long manual.
- **NFR‑2**: The system should support common screen sizes (for example, desktop and mobile).

### 2.2 Performance
- **NFR‑3**: Under normal conditions, opening a chat or sending a message should feel fast (for example, respond within a few seconds).

### 2.3 Security and Privacy
- **NFR‑4**: Users should log in with a password or other basic authentication method.
- **NFR‑5**: User data such as messages and profiles should not be visible to people who are not allowed to see them.
- **NFR‑6**: The system should allow users to report and block other users who behave badly.

### 2.4 Reliability
- **NFR‑7**: The system should try to avoid losing important data such as connection lists and message history.

### 2.5 Future Scalability and Maintainability
- **NFR‑8**: The design should allow us to add more features later without rewriting everything.

