"""
Populate test data for FlirtNet application.

Creates 3 test users with profiles, datemate connections, messages, and forum posts.
"""
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models.user import User
from app.models.profile import Profile
from app.models.connection import DatemateConnection
from app.models.message import PrivateMessage
from app.models.post import Post, PostComment, PostLike
from app.utils.security import hash_password


def populate_data():
    """Populate database with test data."""
    print("🔄 Initializing database...")
    init_db()
    
    db = SessionLocal()
    
    try:
        print("👥 Creating users...")
        
        # User 1: Alice
        alice = User(
            username="alice",
            email="alice@flirtnet.com",
            password_hash=hash_password("alice123")
        )
        db.add(alice)
        db.flush()
        
        alice_profile = Profile(
            user_id=alice.id,
            display_name="Alice Wonder",
            bio="Love hiking and photography 📸 Looking for someone to explore the world with!",
            age=25,
            gender="female",
            preferred_gender="male",
            location="San Francisco, CA",
            interests=["hiking", "photography", "travel", "coffee"]
        )
        db.add(alice_profile)
        
        # User 2: Bob
        bob = User(
            username="bob",
            email="bob@flirtnet.com",
            password_hash=hash_password("bob123")
        )
        db.add(bob)
        db.flush()
        
        bob_profile = Profile(
            user_id=bob.id,
            display_name="Bob Smith",
            bio="Software engineer by day, chef by night 👨‍💻🍳 Let's grab dinner!",
            age=28,
            gender="male",
            preferred_gender="female",
            location="San Francisco, CA",
            interests=["cooking", "tech", "gaming", "movies"]
        )
        db.add(bob_profile)
        
        # User 3: Charlie
        charlie = User(
            username="charlie",
            email="charlie@flirtnet.com",
            password_hash=hash_password("charlie123")
        )
        db.add(charlie)
        db.flush()
        
        charlie_profile = Profile(
            user_id=charlie.id,
            display_name="Charlie Brown",
            bio="Musician and artist 🎸🎨 Open to meeting new people!",
            age=26,
            gender="male",
            preferred_gender="any",
            location="Oakland, CA",
            interests=["music", "art", "concerts", "painting"]
        )
        db.add(charlie_profile)
        
        db.commit()
        print(f"✅ Created users: alice (ID: {alice.id}), bob (ID: {bob.id}), charlie (ID: {charlie.id})")
        
        # Create datemate connections
        print("💑 Creating datemate connections...")
        
        # Alice <-> Bob (accepted)
        alice_bob_connection = DatemateConnection(
            requester_id=alice.id,
            receiver_id=bob.id,
            status="accepted",
            requested_at=datetime.utcnow() - timedelta(days=5),
            responded_at=datetime.utcnow() - timedelta(days=4)
        )
        db.add(alice_bob_connection)
        
        # Charlie -> Alice (pending)
        charlie_alice_connection = DatemateConnection(
            requester_id=charlie.id,
            receiver_id=alice.id,
            status="pending",
            requested_at=datetime.utcnow() - timedelta(days=1)
        )
        db.add(charlie_alice_connection)
        
        db.commit()
        print("✅ Created connections: Alice↔Bob (accepted), Charlie→Alice (pending)")
        
        # Create private messages between Alice and Bob
        print("💬 Creating private messages...")
        
        messages = [
            (bob.id, alice.id, "Hey Alice! How's it going?", 5),
            (alice.id, bob.id, "Hi Bob! Doing great, thanks! How about you?", 5),
            (bob.id, alice.id, "Pretty good! Want to grab coffee this weekend?", 4),
            (alice.id, bob.id, "That sounds lovely! I know a great place in the Mission.", 4),
            (bob.id, alice.id, "Perfect! Saturday at 2pm?", 3),
            (alice.id, bob.id, "See you then! 😊", 3),
            (bob.id, alice.id, "Looking forward to it!", 2),
            (alice.id, bob.id, "Me too! Have a great day!", 2),
        ]
        
        for sender_id, receiver_id, text, days_ago in messages:
            msg = PrivateMessage(
                connection_id=alice_bob_connection.id,
                sender_id=sender_id,
                receiver_id=receiver_id,
                message_text=text,
                sent_at=datetime.utcnow() - timedelta(days=days_ago, hours=2)
            )
            db.add(msg)
        
        db.commit()
        print(f"✅ Created {len(messages)} messages between Alice and Bob")
        
        # Create forum posts
        print("📝 Creating forum posts...")
        
        posts_data = [
            (alice.id, "Best hiking spots in Bay Area? Looking for recommendations for weekend hikes! 🥾", 3),
            (bob.id, "Anyone tried the new ramen place downtown? Just discovered this amazing spot, highly recommend! 🍜", 2),
            (charlie.id, "Live music this weekend! Playing at The Fillmore on Saturday, come say hi! 🎸", 1),
        ]
        
        for user_id, content, days_ago in posts_data:
            post = Post(
                user_id=user_id,
                content_text=content,
                created_at=datetime.utcnow() - timedelta(days=days_ago)
            )
            db.add(post)
            db.flush()
            
            # Add some likes
            if user_id != alice.id:
                like = PostLike(post_id=post.id, user_id=alice.id)
                db.add(like)
            if user_id != bob.id:
                like = PostLike(post_id=post.id, user_id=bob.id)
                db.add(like)
            
            # Add a comment
            if user_id == alice.id:
                comment = PostComment(
                    post_id=post.id,
                    user_id=bob.id,
                    comment_text="I love Muir Woods! Great suggestion."
                )
                db.add(comment)
            elif user_id == bob.id:
                comment = PostComment(
                    post_id=post.id,
                    user_id=alice.id,
                    comment_text="Thanks for the tip! I'll check it out!"
                )
                db.add(comment)
        
        db.commit()
        print(f"✅ Created {len(posts_data)} forum posts with likes and comments")
        
        print("\n" + "="*60)
        print("✨ Test data populated successfully!")
        print("="*60)
        print("\n📋 Test Credentials:")
        print("-" * 60)
        print("Username: alice    | Password: alice123")
        print("Username: bob      | Password: bob123")
        print("Username: charlie  | Password: charlie123")
        print("-" * 60)
        print("\n💡 Relationships:")
        print("  • Alice and Bob are datemates (can message)")
        print("  • Charlie has sent a pending request to Alice")
        print("\n🎯 Ready to test!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    populate_data()
