# Project Specification: Aura - The Emotionally Intelligent Social Discovery Platform

### 1. Problem Statement

Modern dating and social discovery applications have gamified human connection, leading to a phenomenon known as "swipe-and-ghost." By treating individuals as commodities in an infinite catalog, existing platforms foster choice overload, interaction anxiety, and emotional burnout. Furthermore, these platforms typically abandon the user immediately after a match is made, providing no support for the subsequent, and arguably more difficult, stages of relationship building: initiating conversation, deepening the connection, and navigating the emotional fallout of a disconnection. 

A startup has hired your development team to build **Aura**, a next-generation social discovery platform built on a philosophy of "Humanity Caring." Aura aims to differentiate itself by acting as a supportive digital companion throughout the entire lifecycle of a connection (Meet, Converse, Commit, and Heal). To support a large user base with real-time demands, the system requires a highly scalable, robust architecture. The new system will leverage a modern tech stack—employing a Golang-based microservices architecture, PostgreSQL for relational data, Redis for high-speed queue management, and advanced Large Language Model (LLM) integrations for real-time emotional and conversational support. Designed by a 10-person engineering team, the platform must be secure, highly concurrent, and capable of real-time bidirectional communication.

The requirements for this system are given in the list below as either minimum viable features or desired features for the overall system. 

### 2. Minimum Viable Features (MVF)

a) **Real-Time Asynchronous Matching Engine:** The core of the product must include an efficient matching queue where users are paired based on bidirectional preferences (e.g., gender, age, interests). The backend must use an in-memory datastore (e.g., Redis) to achieve sub-second matching latency for thousands of concurrent users.

b) **Secure, Room-Based Private Chat:** Upon a successful match, users must be transitioned seamlessly into a private, ephemeral communication room. This requires a robust WebSocket implementation capable of handling high-frequency message broadcasting, connection drops, and automatic reconnections. All message payloads should be encrypted.

c) **User Identity and Profile Management:** The system must allow users to create and manage their profiles, including uploading avatars, setting matching preferences, and defining "interests" using dynamically filterable metadata tags. This data must be securely stored in a relational database (e.g., PostgreSQL).

d) **AI Conversation Coach (The "Wingman"):** To solve the "cold start" conversation problem, the system must integrate with an LLM via an AI Service Layer. During a live chat, users can request the AI Coach to analyze the recent context of the conversation and provide three personalized, respectful, and engaging conversation starters or responses.

### 3. Desired Features

a) **Proactive Safety Monitor:** A background AI service that analyzes the sentiment and content of all real-time messages. It should detect harassment, bullying, or toxic behavior before the message is fully processed by the recipient, automatically masking the content and flagging the offender’s account for moderation.

b) **Closure Space (Breakup Simulator):** An innovative therapeutic feature designed to help users process grief after disconnecting from a match. Using style-transfer LLM capabilities, this module safely simulates a conversation in the communication style of the former partner, allowing users to express unspoken thoughts and find emotional closure without real-world contact.

c) **Social Sandbox (Practice Mode):** A training environment for users with high social anxiety. The Sandbox allows users to chat with diverse AI personas (e.g., "The Introvert", "The Adventurer") in a low-stakes environment to build conversational confidence before entering the live matching queue.

d) **Public Community Feed:** A shared, global feed where users can participate in public dialogue, share text or image posts, and engage with community content before entering one-on-one Discovery mode. This requires an optimized feed generation algorithm.

e) **Multimedia Integration (Audio/Video):** Utilizing WebRTC to allow users who have established a baseline of trust in text chat to upgrade their connection to secure audio or video calls directly within the application, reducing the need to share personal phone numbers.

f) **Scalable Microservices Architecture:** The backend should be decomposed into distinct Go microservices (e.g., Auth Service, Match Service, Chat Service, AI Service), communicating via gRPC or message brokers (like Kafka/RabbitMQ) to ensure high availability, fault tolerance, and ease of deployment via containerization.
