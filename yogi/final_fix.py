import sqlite3
import random

conn = sqlite3.connect('instance/skillswap.db')
c = conn.cursor()

# 1. Change admin username to "master"
c.execute("UPDATE users SET username = 'master' WHERE username = 'admin'")
print("Changed 'admin' -> 'master'")

# Get user IDs
c.execute("SELECT id FROM users")
user_ids = [row[0] for row in c.fetchall()]
print(f"Users: {user_ids}")

# 2. Add Learning skills
learning_skills = [
    ('Learn Python', 'Want to learn Python programming', 'Technology'),
    ('Guitar Lessons', 'Looking for guitar lessons', 'Music'),
    ('Spanish', 'Want to learn Spanish language', 'Languages'),
    ('Healthy Cooking', 'Want to learn healthy cooking', 'Cooking'),
    ('Yoga', 'Interested in learning yoga', 'Health'),
    ('Photography', 'Want to learn photography basics', 'Art & Design'),
    ('Swimming', 'Looking for swimming lessons', 'Sports'),
    ('Mathematics', 'Need help with mathematics', 'Academic'),
    ('Business Skills', 'Want to learn business basics', 'Business'),
    ('Crafts', 'Interested in learning crafts', 'Crafts'),
]

for title, desc, cat in learning_skills:
    random_user = random.choice(user_ids)
    c.execute('''INSERT INTO skills (user_id, title, description, category, skill_type, is_approved) 
                 VALUES (?, ?, ?, ?, 'wanted', 1)''',
              (random_user, title, desc, cat))
    print(f"Added: {title} -> user {random_user}")

conn.commit()

# Verify
print("\n=== Learning Skills ===")
c.execute("SELECT s.title, s.skill_type, u.username FROM skills s JOIN users u ON s.user_id = u.id WHERE s.skill_type = 'wanted'")
for r in c.fetchall():
    print(f"  {r[0]} - {r[2]}")

print("\n=== Admin Username ===")
c.execute("SELECT username FROM users WHERE id = 1")
print(f"  User ID 1 is now: {c.fetchone()[0]}")

conn.close()
print("\nDone!")

