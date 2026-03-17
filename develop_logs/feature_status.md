# FlirtNet Feature Status Audit

This document is for internal development use. It records the status of the existing `codespace` implementation from the older FlirtNet version and maps it to the current project-description feature list.

Status labels:
- `Implemented`: working in the old version with visible frontend and backend support.
- `Partial`: present in some form, but limited, inconsistent, or missing important parts.
- `Not Implemented`: not present in the old version, or only mentioned in old planning documents.

## Feature Status

| Feature | Status in Old Version | Notes |
|---|---|---|
| Account Registration and Login | Implemented | Registration and JWT login exist in backend and frontend. |
| User Profiles and Preferences | Implemented | Users can edit profile details, interests, preferences, location, and avatar. |
| Real-Time Matching | Partial | Real-time matching exists, but actual matching logic is mainly based on gender and preferred gender rather than richer discovery filters or shared-interest discovery. |
| Random Chat | Implemented | Random one-to-one chat works through Socket.IO, including leave and disconnect flow. |
| Datemate Request Workflow | Partial | Sending and accepting datemate requests work, but the reject flow appears inconsistent between frontend and backend routes. |
| Datemate List and Private Chat | Implemented | Accepted datemates are listed, and private chat with persisted history is available. |
| Community Square | Implemented | Users can create posts with images, like posts, comment, view profiles, and send datemate requests through the community flow. |
| Wingman Conversation Copilot | Implemented | Wingman suggestions are available in both random chat and private chat. |
| Atmosphere Feedback | Partial | Atmosphere analysis exists and is used in random chat; it is not consistently exposed as a standalone feature across all chat flows. |
| Profile Optimizer | Implemented | Users can request profile improvement suggestions from the profile page. |
| Quick Report and Safety Monitoring | Partial | Safety warning checks and report analysis exist, and reports return immediate feedback, but the system does not provide a full moderation workflow and safety handling is still limited. |
| Practice Mode | Implemented | Users can practice with virtual personas before real conversations. |
| Miss Ex Emotional Support | Partial | Miss Ex exists in private chat and can imitate a partner's tone, but it is not restricted to post-breakup use and there is no finished datemate-removal flow to unlock it properly. |
| Relationship Control Tools | Not Implemented | Datemate removal, blocklist, and mute controls are mentioned in old planning documents but are not present in the old codebase. |
| Cross-Platform Accessibility and Notifications | Partial | The app is web-based and responsive enough for browser use, but there is no mobile app and no real notification system. |
| Multimedia Communication | Not Implemented | Image sharing in chat, voice messages, audio calls, and video calls are only future ideas in the old docs. |

## Evidence Summary

### Clearly Implemented in `codespace`
- Auth: `codespace/backend/app/routers/auth.py`, `codespace/frontend/src/services/authService.js`
- Profiles: `codespace/backend/app/routers/profiles.py`, `codespace/frontend/src/pages/ProfilePage.jsx`
- Matching and random chat: `codespace/backend/app/utils/socketio_server.py`, `codespace/frontend/src/pages/RandomChatPage.jsx`
- Datemates: `codespace/backend/app/routers/datemates.py`, `codespace/frontend/src/pages/DatematesPage.jsx`
- Private messages: `codespace/backend/app/routers/messages.py`, `codespace/frontend/src/pages/MessagesPage.jsx`
- Community square: `codespace/backend/app/routers/posts.py`, `codespace/frontend/src/pages/SquarePage.jsx`
- Wingman, Practice Mode, Profile Optimizer, Miss Ex, Atmosphere, Safety Check: `codespace/backend/app/routers/ai.py`, `codespace/frontend/src/services/aiService.js`
- Reporting: `codespace/backend/app/routers/report.py`, `codespace/frontend/src/services/reportService.js`

### Mentioned in old docs but not finished in code
- Datemate removal
- Blocklist / blacklist
- Mute controls
- Notifications
- Image sharing in private/random chat
- Voice messages
- Audio calls
- Video calls
- Mobile app support

## Developer Notes

- The old FlirtNet version is strongest in its core loop:
  register -> profile -> real-time matching -> random chat -> datemate request -> private chat
- The old version also already includes its distinctive humanity-caring layer:
  Wingman, Practice Mode, Profile Optimizer, Miss Ex, and Quick Report
- The biggest gaps between the old vision and the old implementation are:
  richer matching logic, relationship control tools, proper Miss Ex unlocking after breakup, stronger moderation flow, notifications, and multimedia communication
