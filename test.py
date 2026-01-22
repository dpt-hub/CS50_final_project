import sqlite3

db = sqlite3.connect('instance/main.db')
cur = db.cursor()
test = cur.execute (
    'SELECT * FROM users WHERE user_id = 700'
)
print(len(test))
print(test)
print(test.keys())
print(test[0])




if not test:
    print('if not test:')
else:
    print('error')