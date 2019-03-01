import postgresql


def db_connet():
    con = postgresql.open('pq://postgres:torn@185.143.173.37:5432/dbmarket')
    test(con)

def fill_dics(con):
    # formdict
    con.execute('INSERT INTO formdict (name) VALUES ("market point")')
    con.execute('INSERT INTO formdict (name) VALUES ("chain point")')
    con.execute('INSERT INTO formdict (name) VALUES ("sale point")')

    #paymentdict
    con.execute('INSERT INTO paymentdict (name) VALUES ("cash")')
    con.execute('INSERT INTO paymentdict(name) VALUES ("real")')
    con.execute('INSERT INTO paymentdict(name) VALUES ("cons")')


def test(con):
    con.execute(
        'CREATE TABLE FormDict(' +
        'id SERIAL PRIMARY KEY,' +
        'name char(16) NOT NULL CHECK (name <> ''),' +
        ')'
    )
    con.execute(
        'CREATE TABLE PaymentDict(' +
        'id SERIAL PRIMARY KEY,' +
        'name char(16) NOT NULL CHECK (name <> ''),' +
        ')'
    )
    # con.execute(
    #     'CREATE TABLE countcat(' +
    #     'id SERIAL PRIMARY KEY,' +
    #     'name char(16) NOT NULL CHECK (name <> ''),' +
    #     'description char(64),' +
    #     ')'
    # )
    con.execute(
        'CREATE TABLE Point(' +
        'id SERIAL PRIMARY KEY,' +
        'name char(64) NOT NULL CHECK (name <> ''),' +
        'form_id integer references formcat(id),' +
        'payment_id integer references paymentcat(id)' +
        ')'
    )
    con.execute(
        'CREATE TABLE PointContact(' +
        'id SERIAL PRIMARY KEY,' +
        'point_id integer references Point(id),' +
        'name char(64),' +
        'contact char(64),' +
        ')'
    )
    con.execute(
        'CREATE TABLE Trader(' +
        'id SERIAL PRIMARY KEY,' +
        'name char(16) NOT NULL CHECK (name <> ''),' +
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

# CREATE TABLE region (
#  region_id SERIAL PRIMARY KEY,
#  name varchar(40) NOT NULL CHECK (name <> ''),
#  station varchar(40) NOT NULL CHECK (name <> '')
# );
