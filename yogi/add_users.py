import sqlite3

conn = sqlite3.connect('instance/skillswap.db')
c = conn.cursor()

# Get existing usernames
c.execute("SELECT username FROM users")
existing = [row[0].lower() for row in c.fetchall()]
print(f"Existing: {existing}")

# New users (boys and girls names)
new_users = [
    ('rahul', 'rahul@demo.com'),
    ('priya', 'priya@demo.com'),
    ('arun', 'arun@demo.com'),
    ('divya', 'divya@demo.com'),
    ('kumar', 'kumar@demo.com'),
    ('sneha', 'sneha@demo.com'),
    ('vijay', 'vijay@demo.com'),
    ('anita', 'anita@demo.com'),
    ('suresh', 'suresh@demo.com'),
    ('meera', 'meera@demo.com'),
]

added = 0
for username, email in new_users:
    if username.lower() not in existing:
        # Default password is "password123"
        from werkzeug.security import generate_password_hash
        pwd_hash = generate_password_hash('password123')
        c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                  (username, email, pwd_hash))
        print(f"Added: {username}")
        added += 1

print(f"\nTotal added: {added}")

conn.commit()

# Show all users
c.execute("SELECT id, username FROM users")
print("\nAll users:")
for r in c.fetchall():
    print(f"  ID {r[0]}: {r[1]}")

conn.close()

