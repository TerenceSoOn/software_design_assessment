# Problem Statement

## 1. Ideal

In an ideal online world, social interaction would be easy and flexible, like in real life. There should be a perfect platform for online social interaction. The platform would combine different ways of communication, and by using the platform, users could easily enjoy the excitement of meeting new people randomly, having deep public discussions, and building private, long-lasting connections. Besides, this platform would put user’s control and safety first. It would have a strong login system to make sure every user is real. It should also have a system that checks content by using a mix of AI checks and human’s report to find and stop bad behavior such as spam and harassment.

Functionally, the user experience would be smooth. A user could start a quick chat with a random person. After the chat, they could send a "connection request”. If accepted, this new contact would become a “My Connection”, and later, they could have one-on-one chats with each other. At the same time, there is a lively public forum. People are sharing thoughts and joining discussions on different topics. The platform would work perfectly on desktops, tablets, and mobile devices, and be built to grow easily, supporting many users without slowing down.

## 2. Reality

The current market for online social apps is broken into many different pieces and does not offer a complete experience. Users have to switch between separate apps that each do only one thing. One platform might offer temporary random chat (like OmeTV), but these chats disappear permanently after the "next" button is clicked. There is no way to stay in touch even though they had a pleasant conversation. Separately, platforms for public discussion (like TieBa or Reddit) are good for community chats but are often not personal and not good for sparking one-on-one connections. Their focus is content, not connection. Finally, private messaging apps (like Wechat or WhatsApp) are built only for people who already know each other; they don't have a feature to find new people.

More importantly, these separate platforms have serious, unsolved problems. Random chat services are known for having for serious problems such as inappropriate content and scams. And due to the anonymity, they have almost no rules or security checks. Public forums are struggled by false information and mass harassment. Because of the lack of a unified login system, a user who has been banned on one platform for bad behavior can easily appear on another platform, and even register a new account on the same platform.

## 3. Consequences

The results of these problems are serious. First, the mental effort of managing accounts and apps for different social needs makes users tired of these platforms. Users are unsatisfied, as no single platform gives them the complete social experience they want. Second, they result in a trend of shallow chats. Being unable to link a chance encounter with a long-lasting relationship means that many potential connections will be missed. Third, and most dangerously, they create an unsafe and unfriendly online space. Bad behavior easily happens if the platform fails to use platform-wide safety checks and user verification. Not only does it put users in danger, but it also damages public trust in online social apps, making people unwilling to join in.

## 4. Proposal

We propose the development of a complete social platform -- "FlirtNet", which is designed to fix the problems above. It will be composed of four parts:

1.  The Discovery: A text-only random matching service. This part acts as the "discovery" path, letting users have playful and engaging one-on-one chats. Importantly, it will be supported by our login system to stop bad behavior.

2.  The Connection System: This part serves as the bridge from temporary to permanent. Users who have a good chat in the Discovery can send a “Connection” request. Once accepted, they are added to a “Connections List” that both users agree to.

3.  The Public Square: A public forum where users can create profiles, publish posts (text, images), follow topics, and join in discussions.

4.  Private Messaging: A one-on-one messaging system available only between users who are "Connections". This provides a safe and private space for developing the connections discovered on the platform.

To achieve this, we will adopt the Model-View-Controller (MVC) architectural pattern, which is ideal for our team size. This pattern separates our application into three parts: The Model (our backend data and logic, Firebase), The View (the frontend UI our users see, built with HTML/CSS/JS), and The Controller (takes user input and updates both the Model and View).

This single system addresses the problems directly. It will remove the need for many applications by providing connected features. It will build a path from random meetings to lasting connections for its users. Finally, it addresses concerns by basing the entire platform on the necessary user registration and check content.
