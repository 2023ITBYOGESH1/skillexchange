import sqlite3
conn = sqlite3.connect('instance/skillswap.db')
c = conn.cursor()
c.execute("UPDATE users SET profile_picture = 'default.png' WHERE profile_picture IS NULL")
conn.commit()
print("Fixed! Users with NULL profile_picture updated to default.png")
conn.close()

