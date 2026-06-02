import sqlite3
conn = sqlite3.connect('instance/skillswap.db')
c = conn.cursor()

# Check Learning skills
c.execute("SELECT title, skill_type, username FROM skills s JOIN users u ON s.user_id = u.id WHERE s.skill_type = 'wanted' LIMIT 8")
print('Learning (wanted) skills:')
for r in c.fetchall():
    print(f'  {r[0]} - {r[2]}')

# Check admin username
c.execute('SELECT username FROM users WHERE id = 1')
print(f'\nAdmin user is now: {c.fetchone()[0]}')

conn.close()

