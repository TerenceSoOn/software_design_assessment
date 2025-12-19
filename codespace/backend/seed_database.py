"""
Database Seed Script - Populate DB with demo data for presentation.

Run this script to insert realistic users, posts, connections, and messages
for a professional presentation demo.
"""
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.profile import Profile
from app.models.post import Post, PostLike, PostComment
from app.models.connection import DatemateConnection
from app.models.message import PrivateMessage
from app.utils.security import hash_password


def clear_database(db: Session):
    """Clear all existing data."""
    print("🧹 Clearing existing data...")
    db.query(PrivateMessage).delete()
    db.query(PostComment).delete()
    db.query(PostLike).delete()
    db.query(Post).delete()
    db.query(DatemateConnection).delete()
    db.query(Profile).delete()
    db.query(User).delete()
    db.commit()
    print("✅ Database cleared")


def create_users(db: Session):
    """Create demo users with profiles."""
    print("👥 Creating users...")
    
    users_data = [
        {
            "username": "alice_chen",
            "email": "alice@demo.com",
            "profile": {
                "display_name": "Alice",
                "age": 23,
                "gender": "Female",
                "preferred_gender": "Male",
                "bio": "Adventure seeker 🌍 | Coffee addict ☕ | Love hiking and photography",
                "interests": ["Hiking", "Photography", "Travel", "Coffee"],
                "location": "San Francisco"
            }
        },
        {
            "username": "bob_martin",
            "email": "bob@demo.com",
            "profile": {
                "display_name": "Bob",
                "age": 25,
                "gender": "Male",
                "preferred_gender": "Female",
                "bio": "Software engineer by day, musician by night 🎸 Always up for good conversations",
                "interests": ["Music", "Gaming", "Coding", "Coffee"],
                "location": "New York"
            }
        },
        {
            "username": "cathy_wong",
            "email": "cathy@demo.com",
            "profile": {
                "display_name": "Cathy",
                "age": 22,
                "gender": "Female",
                "preferred_gender": "Any",
                "bio": "Art student 🎨 | Foodie | Looking for genuine connections",
                "interests": ["Art", "Cooking", "Museums", "Travel"],
                "location": "Los Angeles"
            }
        },
        {
            "username": "david_lee",
            "email": "david@demo.com",
            "profile": {
                "display_name": "David",
                "age": 27,
                "gender": "Male",
                "preferred_gender": "Female",
                "bio": "Fitness enthusiast 💪 | Movie buff 🎬 | Let's grab a smoothie!",
                "interests": ["Fitness", "Movies", "Cooking", "Hiking"],
                "location": "San Francisco"
            }
        },
        {
            "username": "emma_liu",
            "email": "emma@demo.com",
            "profile": {
                "display_name": "Emma",
                "age": 24,
                "gender": "Female",
                "preferred_gender": "Male",
                "bio": "Book lover 📚 | Yoga instructor 🧘‍♀️ | Plant mom 🌱",
                "interests": ["Reading", "Yoga", "Gardening", "Tea"],
                "location": "Seattle"
            }
        },
        {
            "username": "frank_tan",
            "email": "frank@demo.com",
            "profile": {
                "display_name": "Frank",
                "age": 26,
                "gender": "Male",
                "preferred_gender": "Female",
                "bio": "Entrepreneur | Basketball player 🏀 | Love trying new restaurants",
                "interests": ["Basketball", "Business", "Food", "Travel"],
                "location": "Austin"
            }
        }
    ]
    
    password = hash_password("demo123")  # All users have password: demo123
    users = []
    
    for user_data in users_data:
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password_hash=password
        )
        db.add(user)
        db.flush()  # Get user ID
        
        profile_data = user_data["profile"]
        profile = Profile(
            user_id=user.id,
            display_name=profile_data["display_name"],
            age=profile_data["age"],
            gender=profile_data["gender"],
            preferred_gender=profile_data.get("preferred_gender"),
            bio=profile_data["bio"],
            interests=profile_data["interests"],
            location=profile_data.get("location")
        )
        db.add(profile)
        users.append(user)
    
    db.commit()
    print(f"✅ Created {len(users)} users")
    return users


def create_posts(db: Session, users):
    """Create engaging community posts."""
    print("📝 Creating posts...")
    
    posts_data = [
        {
            "user_idx": 0,  # Alice
            "content": "Just got back from an amazing hike in Yosemite! 🏔️ The views were absolutely breathtaking. Anyone else love exploring nature?",
            "tags": ["Hiking", "Nature", "Travel"]
        },
        {
            "user_idx": 1,  # Bob
            "content": "Finished my first jazz composition today! 🎸 Been working on it for weeks. Music is such a beautiful way to express emotions.",
            "tags": ["Music", "Jazz", "Creative"]
        },
        {
            "user_idx": 2,  # Cathy
            "content": "Discovered this cute little cafe downtown ☕ Their matcha latte is to die for! Perfect spot for weekend brunch.",
            "tags": ["Food", "Coffee", "Weekend"]
        },
        {
            "user_idx": 3,  # David
            "content": "New PR at the gym today! 💪 Consistency is key. Who else is on their fitness journey?",
            "tags": ["Fitness", "Gym", "Motivation"]
        },
        {
            "user_idx": 4,  # Emma
            "content": "Just finished reading 'The Midnight Library' 📚 Such a beautiful story about choices and second chances. Highly recommend!",
            "tags": ["Books", "Reading", "Recommended"]
        },
        {
            "user_idx": 0,  # Alice
            "content": "Golden hour photography walk around the city 📸 The lighting was perfect today!",
            "tags": ["Photography", "Art", "City"]
        }
    ]
    
    posts = []
    for post_data in posts_data:
        user = users[post_data["user_idx"]]
        post = Post(
            user_id=user.id,
            content_text=post_data["content"],
            tags=post_data.get("tags", []),
            created_at=datetime.utcnow() - timedelta(hours=len(posts) * 2)
        )
        db.add(post)
        posts.append(post)
    
    db.commit()
    print(f"✅ Created {len(posts)} posts")
    return posts


def create_likes_and_comments(db: Session, users, posts):
    """Add likes and comments to posts."""
    print("💬 Creating likes and comments...")
    
    # Like relationships
    likes_data = [
        (1, 0),  # Bob likes Alice's hiking post
        (2, 0),  # Cathy likes Alice's hiking post
        (3, 0),  # David likes Alice's hiking post
        (0, 1),  # Alice likes Bob's music post
        (4, 1),  # Emma likes Bob's music post
        (0, 2),  # Alice likes Cathy's cafe post
        (1, 2),  # Bob likes Cathy's cafe post
        (4, 3),  # Emma likes David's fitness post
        (3, 4),  # David likes Emma's book post
        (0, 5),  # Alice's photography post liked by Bob
        (1, 5),
    ]
    
    for user_idx, post_idx in likes_data:
        if post_idx < len(posts):
            like = PostLike(
                post_id=posts[post_idx].id,
                user_id=users[user_idx].id
            )
            db.add(like)
    
    # Comments
    comments_data = [
        {
            "post_idx": 0,  # Alice's hiking post
            "user_idx": 1,  # Bob comments
            "text": "Wow! I've been wanting to visit Yosemite. Any trail recommendations?"
        },
        {
            "post_idx": 0,
            "user_idx": 3,  # David comments
            "text": "Stunning! Nature is the best therapy 🌲"
        },
        {
            "post_idx": 1,  # Bob's music post
            "user_idx": 0,  # Alice comments
            "text": "This is so cool! Would love to hear it sometime!"
        },
        {
            "post_idx": 2,  # Cathy's cafe post
            "user_idx": 0,  # Alice comments
            "text": "I know that place! Their pastries are amazing too 🥐"
        },
        {
            "post_idx": 4,  # Emma's book post
            "user_idx": 3,  # David comments
            "text": "Adding this to my reading list! Thanks for the rec 📖"
        },
        {
            "post_idx": 5,  # Alice's photography post
            "user_idx": 2,  # Cathy comments
            "text": "Beautiful shots! What camera do you use?"
        }
    ]
    
    for comment_data in comments_data:
        comment = PostComment(
            post_id=posts[comment_data["post_idx"]].id,
            user_id=users[comment_data["user_idx"]].id,
            comment_text=comment_data["text"]
        )
        db.add(comment)
    
    db.commit()
    print(f"✅ Created {len(likes_data)} likes and {len(comments_data)} comments")


def create_connections(db: Session, users):
    """Create datemate connections."""
    print("💑 Creating datemate connections...")
    
    connections_data = [
        {
            "requester_idx": 0,  # Alice -> Bob (accepted)
            "receiver_idx": 1,
            "status": "accepted",
            "days_ago": 5
        },
        {
            "requester_idx": 3,  # David -> Emma (accepted)
            "receiver_idx": 4,
            "status": "accepted",
            "days_ago": 3
        },
        {
            "requester_idx": 1,  # Bob -> Cathy (pending)
            "receiver_idx": 2,
            "status": "pending",
            "days_ago": 1
        }
    ]
    
    connections = []
    for conn_data in connections_data:
        connection = DatemateConnection(
            requester_id=users[conn_data["requester_idx"]].id,
            receiver_id=users[conn_data["receiver_idx"]].id,
            status=conn_data["status"],
            requested_at=datetime.utcnow() - timedelta(days=conn_data["days_ago"]),
            responded_at=datetime.utcnow() - timedelta(days=conn_data["days_ago"] - 1) if conn_data["status"] == "accepted" else None
        )
        db.add(connection)
        connections.append(connection)
    
    db.commit()
    print(f"✅ Created {len(connections)} connections")
    return connections


def create_messages(db: Session, users, connections):
    """Create private messages between datemates."""
    print("💌 Creating private messages...")
    
    # Messages between Alice and Bob
    alice_bob_messages = [
        {
            "sender_idx": 0,  # Alice
            "receiver_idx": 1,  # Bob
            "text": "Hey! Thanks for connecting! I saw you're into music 🎸",
            "hours_ago": 48
        },
        {
            "sender_idx": 1,  # Bob
            "receiver_idx": 0,  # Alice
            "text": "Hi Alice! Yes! I saw your hiking photos, they're amazing! 📸",
            "hours_ago": 47
        },
        {
            "sender_idx": 0,
            "receiver_idx": 1,
            "text": "Thank you! I'd love to hear your jazz composition sometime",
            "hours_ago": 46
        },
        {
            "sender_idx": 1,
            "receiver_idx": 0,
            "text": "I'd be happy to share it! Maybe we could grab coffee and I can tell you about my music?",
            "hours_ago": 45
        },
        {
            "sender_idx": 0,
            "receiver_idx": 1,
            "text": "That sounds wonderful! I know a great coffee place downtown ☕",
            "hours_ago": 44
        }
    ]
    
    # Messages between David and Emma
    david_emma_messages = [
        {
            "sender_idx": 3,  # David
            "receiver_idx": 4,  # Emma
            "text": "Hi Emma! I loved your post about The Midnight Library 📚",
            "hours_ago": 24
        },
        {
            "sender_idx": 4,  # Emma
            "receiver_idx": 3,  # David
            "text": "Hi David! Thanks! Are you a reader too?",
            "hours_ago": 23
        },
        {
            "sender_idx": 3,
            "receiver_idx": 4,
            "text": "I'm trying to read more! Also noticed you do yoga - I've been wanting to start",
            "hours_ago": 22
        },
        {
            "sender_idx": 4,
            "receiver_idx": 3,
            "text": "That's great! Yoga has changed my life. I teach beginner classes if you're interested!",
            "hours_ago": 21
        }
    ]
    
    all_messages = []
    
    # Add Alice-Bob messages
    for msg_data in alice_bob_messages:
        message = PrivateMessage(
            connection_id=connections[0].id,
            sender_id=users[msg_data["sender_idx"]].id,
            receiver_id=users[msg_data["receiver_idx"]].id,
            message_text=msg_data["text"],
            sent_at=datetime.utcnow() - timedelta(hours=msg_data["hours_ago"])
        )
        db.add(message)
        all_messages.append(message)
    
    # Add David-Emma messages
    for msg_data in david_emma_messages:
        message = PrivateMessage(
            connection_id=connections[1].id,
            sender_id=users[msg_data["sender_idx"]].id,
            receiver_id=users[msg_data["receiver_idx"]].id,
            message_text=msg_data["text"],
            sent_at=datetime.utcnow() - timedelta(hours=msg_data["hours_ago"])
        )
        db.add(message)
        all_messages.append(message)
    
    db.commit()
    print(f"✅ Created {len(all_messages)} messages")


def main():
    """Main seed function."""
    print("\n🌱 Starting database seeding...\n")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Clear existing data
        clear_database(db)
        
        # Create demo data
        users = create_users(db)
        posts = create_posts(db, users)
        create_likes_and_comments(db, users, posts)
        connections = create_connections(db, users)
        create_messages(db, users, connections)
        
        print("\n✨ Database seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"  • {len(users)} users created")
        print(f"  • {len(posts)} posts created")
        print(f"  • {len(connections)} connections established")
        print("\n🔑 Login credentials:")
        print("  Username: alice_chen, bob_martin, cathy_wong, david_lee, emma_liu, or frank_tan")
        print("  Password: demo123")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
