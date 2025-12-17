# FlirtNet: Fostering Genuine Connections in a Digital World
## Software Design Assessment

**Team Members:**
*   Junlin Li
*   Hongjia Huang
*   Jiachen Pan
*   Junrui Liang
*   Yueshen Wang

---

# Session 1: The Vision & The "Why"
**Speaker:** Junlin Li

## Slide 2: The Problem - "The Lonely Crowd"
*   **The Paradox:** We are more connected than ever, yet loneliness is rising.
*   **Fragmentation:**
    *   Users juggle multiple apps: Tinder for dating, Reddit for forums, WhatsApp for chat.
    *   There is no unified journey from "Stranger" to "Partner."
*   **The "Cold" Start:**
    *   Traditional apps offer little guidance.
    *   Shy or anxious users struggle to break the ice.

## Slide 3: Our Philosophy
*   **Human-Centric Design:**
    *   **Social First:** Technology is the bridge, not the destination.
    *   **Supportive:** We believe a platform should actively help users connect, not just match them.
*   **The Goal:**
    *   To create a safe, unified ecosystem where users can express themselves, meet spontaneously, and build deep, lasting relationships.

## Slide 4: Technology Snapshot
*   **Built for Performance & Scale:**
    *   **Frontend:** **React** with **Vite** for a responsive, high-performance user interface.
    *   **Backend:** **FastAPI** provides high-speed, asynchronous processing.
    *   **Real-Time:** **Socket.IO** enables event-driven, instant messaging.
    *   **Intelligence:** **DeepSeek LLM** integration for context-aware AI features.

---

# Session 2: Basic Social Features & Reliability
**Speaker:** Jiachen Pan

## Slide 5: The Public Square
*   **Community Feed:**
    *   A dynamic space for users to share thoughts, images, and interests via **Tags**.
    *   Designed to foster discovery based on shared hobbies rather than just appearance.
*   **User Experience:**
    *   **Multimedia Support:** Seamlessly handles text and image content.
    *   **Interaction:** Built-in Like and Comment systems to encourage community engagement.

## Slide 6: Identity & Connections
*   **Datemate System:**
    *   **Mutual Connection:** A formal "Datemate" status that requires mutual acceptance, ensuring consent.
    *   **Profile Customization:** Rich user profiles with bios and avatars to showcase personality.
*   **Lifecycle Management:**
    *   **Request Flow:** Send -> Pending -> Accept/Reject.
    *   **Termination:** "Delete Datemate" feature allows users to cleanly dissolve connections and remove associated private messages.

## Slide 7: System Reliability & Security
*   **Trust & Safety:**
    *   **Secure Authentication:** Verifies identity on every action to prevent unauthorized access.
    *   **Data Protection:** Industry-standard encryption protects user credentials and personal data.
*   **Performance:**
    *   Built on a robust infrastructure that ensures the app runs consistently and reliably.

---

# Session 3: Real-Time Interaction
**Speaker:** Junrui Liang

## Slide 8: Instant Communication
*   **Real-Time Connection:**
    *   **Random Chat:** Spontaneous 1-on-1 conversations with new people.
    *   **Private Messaging:** Secure, private channels for "Datemates."
*   **The Experience:**
    *   Messages are delivered instantly, creating a natural, conversational flow like a phone call rather than email.
    *   Designed to handle multiple active conversations simultaneously without lag.

## Slide 9: Trust & Safety Workflow
*   **AI Content Safety:**
    *   **Automated Detection:** Real-time analysis of messages to detect abuse, harassment, or aggressive behavior using **DeepSeek**.
*   **User Reporting:**
    *   **Manual Action:** One-click reporting mechanism for users to flag harmful content that slips through.
    *   **Review System:** Flags incidents for administrative review (Ban/Suspend).

---

# Session 4: Smart Connection Support
**Speaker:** Yueshen Wang

## Slide 10: Overcoming Social Barriers
*   **AI Companion:**
    *   **Empathetic Chatbot:** A "warm-up" partner for users who haven't found a match, providing emotional support and conversation practice.
*   **Smart Wingman:**
    *   **Context-Aware Suggestions:** Analyzes the chat history to suggest relevant topics or replies.
    *   **User Agency:** Suggestions are optional; the user remains in control of the conversation.

## Slide 11: Intelligent Context Awareness
*   **Understanding the Conversation:**
    *   To give relevant social advice, the system analyzes the **entire conversation flow**, not just keywords.
    *   It understands tone, topics (e.g., movies, hobbies), and emotional context.
*   **Seamless Experience:**
    *   The support is on-demand and unobtrusive.
    *   Designed to be fast and non-blocking, so the user stays in the flow of the chat while receiving help.

## Slide 12: Designing a Social Coach
*   **The Persona:**
    *   We designed the system to be a **polite, encouraging coach**.
*   **Promoting Healthy Interaction:**
    *   **Open-Ended Questions:** The system prioritizes suggestions that invite a reply, turning a dead-end statement into a dialogue.
    *   **Safety & Respect:** Explicitly instructed to avoid aggressive or inappropriate lines, fostering a respectful dating environment.

---

# Session 5: The Full Experience & Future
**Speaker:** Hongjia Huang

## Slide 13: The Demo (Video)
*   **Narrative Arc:**
    1.  **Onboarding:** Registration and Login.
    2.  **Discovery:** Browsing the Public Square.
    3.  **Connection:** Starting a Random Chat.
    4.  **Assistance:** Using the **Smart Wingman** to break the ice.
    5.  **Safety:** **Reporting** a harmful user.
    6.  **Commitment:** Sending a "Datemate" request.
    7.  **Closure:** Deleting a connection.

## Slide 14: Future Roadmap
*   **What's Next?**
    *   **Voice & Video:** Moving beyond text-only chat to deeper interaction.
    *   **Advanced Matching:** Deep learning analysis of personality for better random matches.
    *   **Mobile App:** React Native version for iOS/Android.

## Slide 15: Conclusion
*   **Summary:**
    *   FlirtNet is more than a chat app; it's a supportive social ecosystem.
    *   We combine **safe spaces**, **real-time connection**, and **intelligent support** to solve the problem of digital loneliness.
*   **Q&A**
