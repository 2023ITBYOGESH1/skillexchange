import sqlite3
import random

conn = sqlite3.connect('instance/skillswap.db')
c = conn.cursor()

# Get all user IDs except admin (1)
c.execute('SELECT id FROM users WHERE id != 1')
user_ids = [row[0] for row in c.fetchall()]
print(f'Available users: {user_ids}')

# Get all skills with user_id = 1 (admin skills)
c.execute('SELECT id, title FROM skills WHERE user_id = 1')
skill_rows = c.fetchall()
print(f'Skills to update: {len(skill_rows)}')

# Assign each skill to a random user
for skill_id, title in skill_rows:
    random_user = random.choice(user_ids)
    c.execute('UPDATE skills SET user_id = ? WHERE id = ?', (random_user, skill_id))
    print(f'Updated: {title} -> user_id {random_user}')

conn.commit()
print('\nUpdated successfully!')

# Verify
c.execute('SELECT s.title, u.username FROM skills s JOIN users u ON s.user_id = u.id LIMIT 15')
print('\nFirst 15 skills with usernames:')
for row in c.fetchall():
    print(f'  {row[0]} -> {row[1]}')

conn.close()

