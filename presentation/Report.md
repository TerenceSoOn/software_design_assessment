# FlirtNet: We Meet. We Flirt. We Love.

**Group 2 Project Report**
**Date:** December 21, 2025
**Group Members**:
1. Jiachen Pan 20233802046
2. Junrui Liang 20233802068
3. Hongjia Huang 20223802016
4. Junlin Li 20233802058
5. Yueshen Wang 20233802018

---

## 1. Project Overview
**FlirtNet** is a web-based social platform built to help everyone finds their love one.

While there are many apps for "matching," we realized there was no unified experience for the entire journey of a relationship—from the awkward first "Hello," to the spark of falling in love, and even to the healing process after a breakup(optional).


### The "Meet → Flirt → Love → Heal" Cycle
Our software covers four distinct stages of the user's emotional journey:
1.  **Meet**: Discovering people through **Random Matching** or our **Community Square**.
2.  **Flirt**: Using our **Wingman** to analyze the "vibe" and learn how to communicate.
3.  **Love**: Forming **Datemate** connections and moving to private, secure chats.
4.  **Heal**: Using the **Miss Ex** feature to find closure if things go wrong.

---

## 2. The Need for Software (Why FlirtNet?)

Today's dating landscape has serious problems that we aim to solve:

### A. Too Shy to Start & Lack of dating experience
Many people struggle to meet new people. They match on dating apps but freeze when it's time to start a conversation—afraid of saying the wrong thing or being rejected. They might also not good at expressing themselves, or have no idea how to flirt, the conversation then turns boring.

### B. Fragmented Experience
Users jump between Instagram to browse profiles, Tinder to swipe, and ask unprofessional friends for texting advice. This is exhausting and makes dating feel like a chore instead of fun.

### C. No Protection or Care
When users are harassed, reporting is slow. When relationships end, apps cruelly show the ex's profile again. Lack of emotional support, and checking those abusing words manually is mentally asbuse to stuffs.

---

## 3. How We Came Up With This Idea
Our idea started with a simple question: **"Why is dating so scary?"**

**The truth is: Many of our groupmates are single, and our friends don't even dare to start dating.** We saw this problem everywhere around us:

1. **Hard to meet new people:** Lots of us just stay inside at their spare time, there is almost no chance to meet new people. Even if they meet someone, they do not dare and do not know how to start a talk.

2.  **Seek help from the wrong person**: We watched friends copy-paste their chat logs to their friends, and ask them for suggestions, while they are not professional on dating at all! This is ridiculous!

3.  **The Post-Breakup Void**: We noticed that after breakups, people are at their most vulnerable—staring at old messages with no closure. We thought: *What if we could use those chat histories to simulate a final, safe goodbye?*

This led to **FlirtNet**: not just a tool, but a companion that helps you meet people AND fall in love with the right one, without fear.

---

## 4. Innovations & Key Features

### Random Matching
- With random matching, you will always have a way meeting new people, and you don't have to be shy since if you mess up, just end the chat and find someone else! No one will remember you.

### Your Wingman
This is our flagship innovation. The Wingman will by your side to help you on chatting.
*   **Vibe Analysis**: It reads the conversation history and tells you the current "vibe" (e.g., "Flirty," "Awkward," "Deep").
*   **Smart Replies**: It suggests 3 flirty different responses based on that vibe, helping shy users keep the conversation flowing naturally. Flirt freely with the help of your @ingman.

### Miss Ex (Emotional Closure)
A first-of-its-kind feature. If a user "breaks up" (unfriends a Datemate), they can unlock "Miss Ex."
*   **Function**: It simulates the ex-partner's tone and personality based on past chat history.
*   **Purpose**: It allows users to say the things they never got to say—to get closure, vent, or apologize—in a safe environment that doesn't affect real life.

### Practice Mode
Before meeting real humans, users can enter Practice Mode.
*   **Function**: Chat with a robot (e.g., "The Romantic," "The Cold One") to train on your flirting and social skills.
*   **Benefit**: A "sandbox" for dating where rejection doesn't hurt.

### Flirty and Warm UI Design
We chose a design style that matches the purpose of the app—romantic and welcoming:
*   **Aesthetic**: Inspired by modern "Liquid Glass" trends with translucent cards, soft pink/purple gradients, and floating animations.
*   **Goal**: Create a warm, flirty atmosphere that makes users feel comfortable and excited.

---

## 5. Architecture & Technical Design

We followed strictly professional software engineering practices to build FlirtNet.

### Design Pattern: MVC (Model-View-Controller)
*   **Model (Database)**: We use **SQLite** to store User data, Profiles, and Chat logs.
*   **View (Frontend)**: Built with **React**. It handles the beautiful Liquid Glass UI and user interactions.
*   **Controller (Backend)**: Built with **FastAPI**. It processes the logic, handles AI requests, and manages the database.

### Tech Stack
*   **Frontend**: React, Vite, CSS Modules (for Glassmorphism).
*   **Backend**: Python FastAPI (Eazy to implement).
*   **Real-Time**: **Socket.IO** (Crucial for instant messaging).
*   **AI**: DeepSeek API (Powering the Wingman, Practice Mode, Miss Ex and Report system).

---

## 6. Future Roadmap

We have a clear plan to make FlirtNet a professional, long-term product.

### Phase 1: Essential Feature Updates
*   **Multimedia Support**: Allow sending images and voice messages in Random and Private chats.
*   **Safety Tools**: Add "Blacklist" functionality and Datemate deletion.
*   **Voice/Video Chat**: Moving beyond text to real face-to-face connection.
*   **Password Security**: Email-based password reset and change password functionality.

### Phase 2: Monetization (Pro Plan)
*   **Business Model**: Separate Free vs. Pro users to ensure sustainable growth.
*   **Pro Benefits**: 
    - Unlimited Random Chats
    - Unlimited Wingman assistance
    - Unlimited Profile Optimizer
    - Exclusive access to "Miss Ex" feature

### Phase 3: Professionalism & Scale
*   **Database**: Migrate from SQLite to **PostgreSQL** for better performance and scalability.
*   **Platform Expansion**: Native mobile apps (iOS/Android) and improved Windows compatibility.
*   **Public Access**: Enable public IP access for broader deployment and real-world testing.

---

### Conclusion
FlirtNet is more than code; it's a solution to a human problem. By combining **Random Matching**, **Community**, and **Humanity Caring Features**, we have created a platform that doesn't just match profiles, it connects hearts.

**"No need to be afraid. We are here to help."**
