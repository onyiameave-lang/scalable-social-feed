from models import db, User, Post, Follow
from faker import Faker
import random

def clear_data():
    """wipe the db to start fresh"""
    Post.query.delete()
    Follow.query.delete()
    User.query.delete()
    db.session.commit()


def create_users(count=50):
    """Generate fake user accounts"""
    fake = Faker()
    for _ in range(count):
        # Generate fake data
        user = User(
            username=fake.user_name(),
            email=fake.email()
        )
        db.session.add(user)
    db.session.commit()


def create_posts(count_per_user=5):
    """Generate fake posts for every user"""
    users = User.query.all()

    for user in users:
        for _ in range(count_per_user):
            post_content = f"Random post text for {user.username} - {random.randint(1, 1000)}"
            # Save the post to the database
            new_post = Post(content=post_content, user_id=user.id)
            db.session.add(new_post)
    db.session.commit()
    print(f"Generated {count_per_user} posts for {len(users)} users.")


def create_followers(users):
    """Create random many-to-many relationships"""
    # Check if there are enough users to form a relationship
    if len(users) < 2:
        return
    all_users = User.query.all()

    for follower in all_users:
        num_to_follow = random.randint(3, min(7, len(all_users) - 1))
        # use random sample to avoid picking the same user twice
        potential_targets = random.sample(
            [u for u in all_users if u.id != follower.id], num_to_follow
        )

        for followed in potential_targets:
            # Ensure a user does not follow themselves
            if follower.id != followed.id:
                new_relationship = Follow(follower_id=follower.id, followed_id=followed.id)
                db.session.add(new_relationship)

    db.session.commit()
    print("Network simulation complete")