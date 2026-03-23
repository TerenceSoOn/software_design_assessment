# FlirtNet - We Meet, We Flirt, We Love
Project Proposal on a Supportive Online Dating Platform  
By CS Group 10  


## 1. Introduction and Project Idea

FlirtNet is a supportive social discovery platform designed to help users through the full interaction journey, not only helping them get a match. Many existing dating or social discovery platforms focus too much on first impressions, quick matching, and short-term engagement. However, users often need more support after a match is made. They may not know how to start a conversation, how to keep it going, how to decide whether they want a more meaningful relationship, or how to deal with negative experiences such as harassment or breakup.

Our project aims to build a more complete and caring platform for online social interaction. FlirtNet combines user discovery, real-time chat, datemate relationship development, community interaction, safety support, and emotional support in one system. Instead of treating social interaction as a short and isolated event, the platform is designed to support the whole process, from meeting someone for the first time to developing a datemate relationship, and even to finding closure when that relationship ends.

This project is suitable for a software design and implementation course because it involves several connected software modules, a clear need for system architecture, real-time communication, data management, user interaction design, and practical design decisions. It is also large enough for team-based work, because the system includes account management, profile handling, matching, messaging, safety-related functions, community features, and copilot-based support features.

## 2. Problem Statement and Relevance

Modern dating and social discovery applications make it easier for people to meet online, but they also create several social and emotional problems. Many of these platforms are built around swiping, appearance-based filtering, and quick decisions. As a result, they often encourage shallow interaction and make users focus too much on first impressions. This design may help users find many possible matches, but it does not help them build more meaningful communication.

One major problem is that many users struggle with conversation itself. For shy users, inexperienced users, or users with low confidence, getting matched with someone is only the beginning. They may not know how to start the chat, how to respond naturally, or how to keep the interaction respectful and interesting. Because of this, many conversations quickly become awkward, boring, or inactive. This problem is highly relevant to students and young adults, because many people in this group are active online but still feel pressure and uncertainty in social and dating situations.

Another important issue is fragmentation. In real life, users often move between different tools and platforms to complete what should be one simple social process. They may use one app to discover people, another app to view more personal content, and other online tools to ask for conversation advice. This makes the experience tiring and inconvenient. A better system should provide a more unified environment where users can discover people, communicate, and get support without always switching between platforms.

Safety is also a serious concern. Harmful behaviour in online conversations can affect users immediately, but many current reporting systems are slow, unclear, or only reactive. Users may wait a long time before receiving any feedback after making a report. At the same time, staff may need to manually review harmful chat content, which can create unnecessary emotional burden. A more thoughtful system should provide quicker response, stronger monitoring, and clearer support for users who experience abuse or harassment.

The final issue is that current platforms provide very little support when a relationship ends. In most cases, the system simply removes the datemate relationship and leaves the user to deal with the emotional result alone. However, breakup and failed relationships can have a strong effect on users, especially younger users who may not have much dating experience. A more human-centered platform should recognize that emotional support after a relationship is also part of the user journey.

For these reasons, FlirtNet is relevant as a software project. It responds to real problems in current platforms by proposing a more supportive system that covers discovery, conversation support, datemate relationship development, safety, and emotional closure.

## 3. Target Users and Primary Needs

The main target users of FlirtNet are university students and young adults who use online platforms to meet new people. This group is highly familiar with digital communication, but many users still face difficulties in real social interaction. Some are shy, some have limited dating experience, and some want a safer and more respectful environment than what many existing platforms currently provide.

The project also targets users who need help with communication. These users may be able to create a profile and enter a chat, but they still struggle to find the right words, maintain a good conversation, or express themselves clearly. In addition, the platform is suitable for users who want a stronger sense of safety, especially users who are worried about harassment, abuse, or unclear reporting outcomes.

The primary needs of these users can be summarized as follows:

- They need practical ways to meet suitable people online.
- They need support for starting and maintaining conversations.
- They need tools to present themselves clearly through profiles.
- They need a smoother path from first interaction to longer-term datemate communication.
- They need quick protection and feedback when harmful behaviour happens.
- They need emotional support when a datemate relationship ends badly.

FlirtNet is designed around these needs. Each major module of the system addresses a specific part of the user journey, while still connecting naturally to the others.

## 4. Project Scope

The proposed project will focus on a realistic proof of concept that shows the main design idea of FlirtNet. The project scope is divided into core features for the proof of concept, secondary features that may be added if time allows, and explicit exclusions that will not be part of the initial proof of concept.

### 4.1 Core PoC Features

The core proof of concept will include the following features to make sure our software works:

- **Account registration and login** so that users can create accounts and access personalized functions.
- **User profiles and preferences** so that users can set personal information, interests, preferences, and profile presentation details.
- **Real-time matching** so that users can be paired with suitable partners for first interaction.
- **Random chat** so that matched users can talk immediately in a live one-to-one conversation.
- **Datemate request workflow** so that a successful random chat can develop into a more stable datemate relationship.
- **Datemate list and private chat** so that accepted datemates can continue communication with persistent message history.
- **Community Square** so that users can post content, interact publicly, and discover other users beyond direct matching.
- **Conversation copilot** so that users can receive support when they do not know how to continue a conversation.
- **Practice mode** so that users can practice communication with virtual personas before talking to real people.
- **Quick report and safety monitoring** so that harmful behaviour can be identified and reported more effectively.
- **Miss Ex** so that users have a reflective support space after a datemate relationship ends.

### 4.2 Secondary Features

The following features are planned as secondary features. They are important to the long-term development of the platform, but they are not required for the initial proof of concept:

- **Atmosphere feedback** for giving users simple feedback on the tone of a conversation.
- **Profile optimizer** so that users can improve self-description and profile quality.
- **Relationship control tools** such as datemate removal, blocklist functions, and mute controls.
- **Cross-platform accessibility and notifications** so that the platform can later extend beyond the initial web environment and keep users aware of important activity.
- **Multimedia communication** such as image sharing, voice messages, or richer chat interaction.
- **Membership and payment features** to separate free users and pro users.

### 4.3 Explicit Exclusions

To keep the proposal realistic and achievable, the initial proof of concept will not include:

- full voice and video calling
- a fully developed moderation and admin management system

These areas are valuable for future improvement, but including them in the first proof of concept would increase risk and make the project scope less realistic for the course timeline.

## 5. High-Level Technical Specification

FlirtNet will be developed as a web application with distinct page-level views for the main user workflows. The frontend will be built using **React**, together with CSS and JavaScript for interactive behaviour. This means the system will provide clearly separated views for registration, profile management, random chat, datemates, private chat, and Community Square. This approach fits the project well because it keeps the application structure clear, supports page-based navigation, and still allows the team to use a modern frontend library for reusable interface components.

The backend will be developed in **Go**, using **Gin** as the web framework. Database access will be handled through **GORM**, while the main database will be **PostgreSQL**. In simple terms, React will handle the user interface, Gin will handle HTTP requests and backend routing, GORM will manage data access in the Go application, and PostgreSQL will store the persistent system data. The overall architectural style will be a **modular monolith**. This means the system will run as one main application, but the codebase will be separated into clear functional modules. This approach is suitable because it provides better structure than a simple monolithic implementation, while still being more realistic than splitting the system into many separate services too early.

At a high level, the system will contain the following backend modules:

- an authentication module for account registration, login, and access control
- a profile module for user information and preferences
- a matching and chat module for real-time matching and conversation
- a datemate module for datemate requests, datemate lists, and private chat
- a community module for public posts and interaction
- a safety module for reporting and harmful-content handling
- a copilot-related module for conversation support, practice mode, profile optimization, and Miss Ex

The main persistent data store will be PostgreSQL. This is suitable because the platform depends on structured relational data, including users, profiles, datemate relationships, chat records, posts, comments, and reports. Compared with a lightweight local database, PostgreSQL gives a more professional foundation for data consistency, future growth, and more reliable development practice.

The system will also include WebSocket-based real-time communication for matching and chat. This is necessary because random matching and live messaging depend on fast and continuous interaction between users. In addition to normal HTTP request and response flow, the system therefore needs a persistent real-time layer for live communication events.

The system will also include a message queue layer for asynchronous tasks. This is useful for features that do not need to block the main user request, such as notification delivery, report processing, safety-related background checks, and some copilot-related jobs. For this project, Redis can be used as the supporting technology for caching, temporary state, and queue-related functions. This keeps the architecture more practical for the project while still giving the system a more professional asynchronous processing design.

FlirtNet will also interact with an external copilot-related service for features such as conversation suggestions, safety checking, profile optimization, practice mode, and Miss Ex style support. In the proposal, this external service is treated as a separate system boundary. The main FlirtNet application will be responsible for managing user flow, context, and results, while the copilot-related service will provide support functions for specific features.

### 5.1 Key Interfaces and System Boundaries

The proposal will treat the following interfaces and boundaries as important parts of the system:

- browser pages for registration, profile, random chat, datemates, private chat, and Community Square
- HTTP request and response flow for normal features
- a WebSocket-based real-time communication layer for matching and live chat
- PostgreSQL as the main persistent storage boundary
- a Redis-backed message queue and temporary-state layer for asynchronous processing
- an external copilot service boundary for suggestions, safety checks, and emotional-support functions

These boundaries help define the overall structure of the system clearly without going too deeply into implementation detail at the proposal stage.

## 6. Development Methodology

The project will follow an Agile iterative development approach. This methodology is suitable because FlirtNet is a team-based software project with several connected modules and both technical and user-facing features. An iterative process makes it easier to divide the work into manageable stages, integrate modules gradually, and adjust priorities when needed.

The development process will begin with planning and confirmation of requirements. After that, the team will move into system architecture and data design, so that major structural decisions can be made early. Once the technical foundation is stable, implementation will be carried out in short cycles, with core features prioritized first. This will allow the team to make visible progress while reducing the risk of late integration problems.

Testing and integration will happen throughout development, but a dedicated refinement period will also be included before the proof of concept is finalized. This is important because the project contains several connected parts, including real-time communication, profile-based features, and copilot-related functions. By using iterative development, the team can continuously check whether the system remains coherent and whether the proof of concept still matches the approved proposal scope.

This methodology also fits the course objectives well. It demonstrates software planning, teamwork, incremental implementation, and practical decision-making, instead of relying on one large development phase near the deadline.

## 7. Timeline and Milestones

The project timeline will follow the main course deadlines while leaving enough time for implementation, integration, and documentation.

### 7.1 Proposal Stage

- **By March 30, 2026:** finalize and submit the project proposal

### 7.2 Design and Setup Stage

- **April 1 to April 7, 2026:** confirm detailed requirements, freeze the main scope, and finalize the architecture
- **April 8 to April 21, 2026:** set up backend structure, PostgreSQL foundation, frontend page structure, and core authentication and profile management

### 7.3 Core Implementation Stage

- **April 22 to May 5, 2026:** implement the main social interaction flow, including matching, random chat, datemate workflow, private chat, and Community Square
- **May 6 to May 19, 2026:** implement the main supportive and safety features, including Conversation Copilot, Practice Mode, Miss Ex, and Quick Report

### 7.4 Integration and Refinement Stage

- **May 20 to May 31, 2026:** carry out integration, testing, bug fixing, message-queue integration, and final refinement of the proof of concept; desired features are only considered if the core system is already stable

### 7.5 Submission Preparation Stage

- **By June 1, 2026:** complete and submit the final report
- **June 2 to June 8, 2026:** stabilize the proof of concept, complete the user manual, and submit the software package by the PoC deadline
- **June 9 to June 15, 2026:** prepare the presentation materials, recorded presentation, and final demonstration flow
- **By June 16, 2026:** finalize and submit the group workload profile

This timeline is realistic because it puts the strongest focus on the core proof of concept features first, while keeping secondary features available only if the main implementation is already stable.

## 8. Required Resources

The project requires a combination of development tools, software platforms, infrastructure components, and teamwork.

### 8.1 Development Tools and Platforms

The main tools and platforms required for development are:

- **VS Code** as the main development environment
- **Codex** as a development support tool
- **Git and GitHub** for version control and team collaboration
- **Docker** for environment setup and deployment-related testing
- **Postman** for API testing
- **Go**, **Gin**, and **GORM** for backend development
- **PostgreSQL** for data storage
- **React, CSS, and JavaScript** for the frontend interface

### 8.2 External Services and Optional Components

The project may also rely on:

- external model providers (e.g. OpenAI or DeepSeek) for conversation and support features
- **Redis** for caching, queueing, and temporary state management
- Google Cloud for deploying the project

### 8.3 Team Roles

- Product Manager: Junlin Li, Jiachen Pan
- Backend Developer: Jiachen Pan, Junrui Liang
- Frontend Developer: Junlin Li
- UI Design: Qijia Liu, Mingyuan Li
- Database Design: Yueshen Wang, Hongjia Huang
- Software Testing: Rui Ye, Xinhao Cai
- DevOps: Guangsheng Cai, Rui Ye
- Documentation: Junlin Li, Jiachen Pan

## 9. Conclusion

FlirtNet is proposed as a supportive social discovery platform that responds to several real problems in current online dating and social interaction systems. Instead of focusing only on matching, it aims to support users throughout the larger interaction process, including discovery, communication, datemate relationship development, safety, and emotional closure.

From a software engineering perspective, the project is suitable for the course because it requires clear system design, structured implementation, real-time interaction, database-backed features, asynchronous task processing, and teamwork across several connected modules. The selected technical direction, which uses a React frontend, a Go backend with Gin and GORM, PostgreSQL, Redis, and a modular monolith architecture, provides a practical and coherent foundation for development.

The proposed proof of concept is ambitious but still realistic. It focuses on the core features that define the identity of FlirtNet, while leaving more advanced or broader extensions as secondary work. For these reasons, the project is feasible, coherent, and well aligned with the learning goals of Software Design and Implementation.
