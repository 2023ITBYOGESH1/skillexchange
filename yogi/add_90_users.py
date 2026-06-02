import sqlite3
import random

conn = sqlite3.connect('instance/skillswap.db')
c = conn.cursor()

# 90 new users - boys and girls names
new_users = [
    # Boys names (45)
    ('akhil', 'akhil@demo.com'),
    ('balaji', 'balaji@demo.com'),
    ('charan', 'charan@demo.com'),
    ('dinesh', 'dinesh@demo.com'),
    ('elango', 'elango@demo.com'),
    ('farook', 'farook@demo.com'),
    ('gopal', 'gopal@demo.com'),
    ('harish', 'harish@demo.com'),
    ('irfan', 'irfan@demo.com'),
    ('joseph', 'joseph@demo.com'),
    ('karthik', 'karthik@demo.com'),
    ('lokesh', 'lokesh@demo.com'),
    ('mani', 'mani@demo.com'),
    ('naveen', 'naveen@demo.com'),
    ('ovidhu', 'ovidhu@demo.com'),
    ('prakash', 'prakash@demo.com'),
    ('ramesh', 'ramesh@demo.com'),
    ('sathish', 'sathish@demo.com'),
    ('thiru', 'thiru@demo.com'),
    ('uma Shankar', 'uma@demo.com'),
    ('vignesh', 'vignesh@demo.com'),
    ('wasiq', 'wasiq@demo.com'),
    ('xavier', 'xavier@demo.com'),
    ('yuvan', 'yuvan@demo.com'),
    ('zuber', 'zuber@demo.com'),
    ('ajesh', 'ajesh@demo.com'),
    ('bharath', 'bharath@demo.com'),
    ('chandru', 'chandru@demo.com'),
    ('dhanush', 'dhanush@demo.com'),
    ('gowtham', 'gowtham@demo.com'),
    ('hari', 'hari@demo.com'),
    ('jagan', 'jagan@demo.com'),
    ('kavin', 'kavin@demo.com'),
    ('logesh', 'logesh@demo.com'),
    ('madhan', 'madhan@demo.com'),
    ('nithish', 'nithish@demo.com'),
    ('ponraj', 'ponraj@demo.com'),
    ('rajesh', 'rajesh@demo.com'),
    ('suriya', 'suriya@demo.com'),
    ('tamil', 'tamil@demo.com'),
    ('udhay', 'udhay@demo.com'),
    ('vasan', 'vasan@demo.com'),
    ('wilden', 'wilden@demo.com'),
    ('yasar', 'yasar@demo.com'),
    ('zivan', 'zivan@demo.com'),
    
    # Girls names (45)
    ('aishwarya', 'aishwarya@demo.com'),
    ('banu', 'banu@demo.com'),
    ('chitra', 'chitra@demo.com'),
    ('devi', 'devi@demo.com'),
    ('geetha', 'geetha@demo.com'),
    ('hema', 'hema@demo.com'),
    ('iniya', 'iniya@demo.com'),
    ('jothi', 'jothi@demo.com'),
    ('kamala', 'kamala@demo.com'),
    ('lavanya', 'lavanya@demo.com'),
    ('malini', 'malini@demo.com'),
    ('nandhini', 'nandhini@demo.com'),
    ('osma', 'osma@demo.com'),
    ('pooja', 'pooja@demo.com'),
    ('quincy', 'quincy@demo.com'),
    ('ramya', 'ramya@demo.com'),
    ('saranya', 'saranya@demo.com'),
    ('tharani', 'tharani@demo.com'),
    ('umaa', 'umaa@demo.com'),
    ('vaishnavi', 'vaishnavi@demo.com'),
    ('warda', 'warda@demo.com'),
    ('xena', 'xena@demo.com'),
    ('yogalakshmi', 'yogalakshmi@demo.com'),
    ('zara', 'zara@demo.com'),
    ('archana', 'archana@demo.com'),
    ('bavani', 'bavani@demo.com'),
    ('clarissa', 'clarissa@demo.com'),
    ('divyabranch', 'divyabranch@demo.com'),
    ('eshwari', 'eshwari@demo.com'),
    ('fathima', 'fathima@demo.com'),
    ('ganga', 'ganga@demo.com'),
    ('harshini', 'harshini@demo.com'),
    ('indhu', 'indhu@demo.com'),
    ('jansi', 'jansi@demo.com'),
    ('kavitha', 'kavitha@demo.com'),
    ('lisa', 'lisa@demo.com'),
    ('mahalakshmi', 'mahalakshmi@demo.com'),
    ('nisha', 'nisha@demo.com'),
    ('othila', 'othila@demo.com'),
    ('parvathi', 'parvathi@demo.com'),
    ('qirat', 'qirat@demo.com'),
    ('rita', 'rita@demo.com'),
    ('suganya', 'suganya@demo.com'),
    ('thulasi', 'thulasi@demo.com'),
    ('ushabranch', 'ushabranch@demo.com'),
    ('vijaya', 'vijaya@demo.com'),
]

from werkzeug.security import generate_password_hash
pwd_hash = generate_password_hash('password123')

added = 0
for username, email in new_users:
    c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
              (username, email, pwd_hash))
    added += 1

print(f"Added {added} new users")

conn.commit()

# Get all user IDs
c.execute("SELECT id, username FROM users")
all_users = c.fetchall()
print(f"\nTotal users now: {len(all_users)}")

# Reassign ALL skills to random users
c.execute("SELECT id, title FROM skills")
all_skills = c.fetchall()

for skill_id, title in all_users:
    random_user = random.choice(all_users)
    c.execute("UPDATE skills SET user_id = ? WHERE id = ?", (random_user[0], skill_id))

conn.commit()

# Show skill count per user
c.execute('''SELECT u.username, COUNT(s.id) as cnt 
             FROM users u LEFT JOIN skills s ON u.id = s.user_id 
             GROUP BY u.id ORDER BY cnt DESC LIMIT 20''')
print("\nTop 20 users with skills:")
for r in c.fetchall():
    print(f"  {r[0]}: {r[1]} skills")

print("\nDone! All skills now have different usernames.")
conn.close()
