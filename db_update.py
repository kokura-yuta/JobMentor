import sqlite3

conn = sqlite3.connect("jobmentor.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE chat_logs
ADD COLUMN category TEXT
""")

cursor.execute("""
ALTER TABLE chat_logs
ADD COLUMN root_cause TEXT
""")

conn.commit()
conn.close()

print("更新完了！")