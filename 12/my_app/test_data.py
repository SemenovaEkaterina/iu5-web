import MySQLdb


class Connection:
    def __init__(self, user, password, db, host='localhost'):
        self.user = user
        self.host = host
        self.password = password
        self.db = db
        self._connection = None

    @property
    def connection(self):
        return self._connection

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        if not self._connection:
            self._connection = MySQLdb.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                db=self.db,
                charset = "utf8"
            )

    def disconnect(self):
        if self._connection:
            self._connection.close()


class User:

    def __init__(self, db_connection, first_name, last_name, middle_name, document_number, birthday):
        self.db_connection = db_connection.connection
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.document_number = document_number
        self.birthday = birthday

    def save(self):
        c = self.db_connection.cursor()
        c.execute("INSERT INTO my_app_user (first_name, last_name, middle_name, document_number, birthday) VALUES (%s, %s, %s, %s, %s);",
                  (self.first_name, self.last_name, self.middle_name, self.document_number, self.birthday))
        self.db_connection.commit()
        c.close()

    def get(self):
        c = self.db_connection.cursor()
        c.execute("SELECT * FROM my_app_user;")
        users = []
        for row in c.fetchall():
            u = User
            u.first_name = row[1]
            u.last_name = row[2]
            u.middle_name = row[3]
            u.document_number = row[4]
            u.birthday = row[5]
            users.append(u)
        return users


class Bank:
    def __init__(self, db_connection, name, address):
        self.db_connection = db_connection.connection
        self.name = name
        self.address = address

    def save(self):
        c = self.db_connection.cursor()
        c.execute("INSERT INTO my_app_bank (name, address) VALUES (%s, %s);",
                  (self.name, self.address))
        self.db_connection.commit()
        c.close()


class Transaction:
    def __init__(self, db_connection, type, count, usr_id, bank_id):
        self.db_connection = db_connection.connection
        self.type = type
        self.count = count
        self.usr_id = usr_id
        self.bank_id = bank_id

    def save(self):
        c = self.db_connection.cursor()
        c.execute("INSERT INTO my_app_transaction (type, count, user_id, bank_id) VALUES (%s, %s, %s, %s);",
                  (self.type, self.count, self.usr_id, self.bank_id))
        self.db_connection.commit()
        c.close()


con = Connection("kate", "123", "db_rip")

with con:
    user = User(con, 'Екатерина'.encode('utf-8'), 'Семенова'.encode('utf-8'), 'Владимировна'.encode('utf-8'), '4510'.encode('utf-8'), '1996-12-02')
    user.save()
    bank = Bank(con, 'Стандарт', 'Адрес!')
    bank.save()
    bank = Bank(con, 'Стандарт2', 'Адрес2')
    bank.save()

    for i in range(2, 10):
        tr = Transaction(con, 'perevod', '1000', i/2, i)
        tr.save()

