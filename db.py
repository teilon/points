import postgresql


def db_connet():
    con = postgresql.open('pq://torn:torn@185.143.173.37:5432/dbmarket')
    # test(con)
    # fill_dics(con)

def fill_dics(con):
    # formdict
    con.execute("INSERT INTO FormDict (name) VALUES ('market point')")
    con.execute("INSERT INTO FormDict (name) VALUES ('chain point')")
    con.execute("INSERT INTO FormDict (name) VALUES ('sale point')")

    #paymentdict
    con.execute("INSERT INTO PaymentDict (name) VALUES ('cash')")
    con.execute("INSERT INTO PaymentDict(name) VALUES ('real')")
    con.execute("INSERT INTO PaymentDict(name) VALUES ('cons')")
    con.execute("INSERT INTO PaymentDict(name) VALUES ('unknown')")


def test(con):
    con.execute(
        'CREATE TABLE FormDict(' +
        'id SERIAL PRIMARY KEY,' +
        'name char(16)' +
        ')'
    )
    con.execute(
        'CREATE TABLE PaymentDict(' +
        'id SERIAL PRIMARY KEY,' +
        'name char(16)' +
        ')'
    )
    con.execute(
        'CREATE TABLE PointContact(' +
        'id SERIAL PRIMARY KEY,' +
        'point_id integer REFERENCES Point(id),' +
        'name char(64),' +
        'contact char(64)' +
        ')'
    )
    con.execute(
        'CREATE TABLE Point(' +
        'id SERIAL PRIMARY KEY,' +
        'name char(64),' +
        'form_id integer references FormDict(id),' +
        'payment_id integer references PaymentDict(id),' +
        'adress char(64)' +
        ')'
    )
    con.execute(
        'CREATE TABLE Trader(' +
        'id SERIAL PRIMARY KEY,' +
        'name char(16)' +
        ')'
    )
    con.execute(
        'CREATE TABLE Trade(' +
        'id SERIAL PRIMARY KEY,' +
        'trader_id integer references trader(id),' +
        'point_id integer references point(id),' +
        'count integer,' +
        'sale money,' +
        'date DATE NOT NULL DEFAULT CURRENT_DATE' +
        ')'
    )