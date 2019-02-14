import postgresql


db = postgresql.open('pq://postgres:postgres@localhost:5432/mydb')

db.execute(
    'CREATE TABLE users (' +
    'id SERIAL PRIMARY KEY, ' +
    'login CHAR(64), ' +
    'password CHAR(64)' +
    ')'
)

#INSERT
ins = db.prepare("INSERT INTO users (login, password) VALUES ($1, $2)")

# ins("afiskon", "123")
# ins("eax", "456")

# SELECT
db.query("SELECT id, trim(login), trim(password) FROM users")
# [(1, 'afiskon', '123'), (2, 'eax', '456')]

users = db.query("SELECT * FROM users WHERE id = 1");
users[0][0]
# 1
users[0]["id"]
# 1
users[0]["login"].strip()
# 'afiskon'


# UPDATE
update = db.prepare("UPDATE users SET password = $2 where login = $1")
update("eax", "789")
# ('UPDATE', 1)


# DELETE
delete = db.prepare("DELETE FROM users WHERE id = $1")
delete(3)
# ('DELETE', 0)
db.query("DELETE FROM users WHERE id = 3")
# ('DELETE', 0)


# TRANSACTION
with db.xact() as xact:
    db.query("SELECT id FROM users")
# [(1,), (2,)]

# ROLLBACK
with db.xact() as xact:
    db.query("SELECT id FROM users")
    xact.rollback()


#STORED PROCEDURE
ver = db.proc("version()")
ver()


#CURSOR
db.execute(
    "DECLARE my_cursor CURSOR WITH HOLD FOR " +
    "SELECT id, trim(login) FROM users"
)
c = db.cursor_from_id("my_cursor")
c.read()
# [(1, 'afiskon'), (2, 'eax')]
c.read()
# []
c.close()
