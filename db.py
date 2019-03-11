import postgresql


def db_connet():
    con = postgresql.open('pq://torn:torn@185.143.173.37:5432/dbmarket')
    # test(con)
    # fill_dics(con)
    insert_to()


def insert_to():
    con = postgresql.open('pq://torn:torn@185.143.173.37:5432/dbmarket')
    # ins = con.prepare("INSERT INTO Point (name, password) VALUES ($1, $2)")
    # "WITH ins (name, form, payment, address) AS (VALUES ({}, {}, {}, {}))" \
    # "INSERT INTO Point (name, form_id, payment_id, address) " \
    # "SELECT ins.description, FormDict.id, PaymentDict.id" \
    # "FROM " \
    # "FormDict JOIN ins ON ins.form = FormDict.id" \
    # "PaymentDict JOIN ins ON ins.payment = PaymentDict.id"

    # con.execute("CREATE OR REPLACE PROCEDURE insert_point() LANGUAGE plpgsql AS $$ $$; ")

    # con.execute("CREATE OR REPLACE PROCEDURE insert_point(" +
    #             # "char(64), char(64), char(64), char(64)"
    #             ") " +
    #             "LANGUAGE plpgsql " +
    #             "AS $$ " +
    #             # "DECLARE " \
    #             # "form_id int; " \
    #             # "payment_id int; " \
    #             # "BEGIN " +
    #             # "form_id := SELECT id FROM FormDict WHERE name=$2; " \
    #             # "payment_id := SELECT id FROM PaymentDict WHERE name=$3; " \
    #             # "INSERT INTO Point (name, form_id, payment_id, address) VALUES ($1, $2, $3, $4); " \
    #             # "END; " +
    #             "$$; "
    #             )
    # proc = "CALL insert_point({}, {}, {}, {});".format('name', 'sale point', 'cash', 'Райымбека 91')
    # con.execute(proc)

    # con.execute("CREATE OR REPLACE FUNCTION get_production_deployment(appId integer) " +
    #             "RETURNS TABLE(empId INTEGER, empName VARCHAR) LANGUAGE plpgsql AS " +
    #             "$$ " +
    #             "BEGIN " +
    #             "RETURN QUERY " +
    #             "SELECT id, name " +
    #             "FROM FormDict; " +
    #             "END; " +
    #             "$$; "
    #             )
    # con.execute("DROP FUNCTION IF EXISTS insert_point(name char(64), form char(64), payment char(64), address char(64))")
    con.execute("CREATE OR REPLACE FUNCTION insert_point(" +
                "name char(64), form char(16), payment char(16), address char(64)) " +
                "RETURNS integer " +
                "LANGUAGE plpgsql AS " +
                "$$ " +
                "DECLARE " +
                "form_id int; " +
                "payment_id int; " +
                "BEGIN " +
                "form_id := (SELECT id FROM FormDict WHERE name=form); " +
                "payment_id := (SELECT id FROM PaymentDict WHERE name=payment); " +
                "INSERT INTO Point (name, form_id, payment_id, address) " +
                "VALUES (name, form_id, payment_id, address); " +
                "RETURN 1;" +
                "END; " +
                "$$; "
                )
    # # proc = "EXECUTE insert_point(\'{}\', \'{}\', \'{}\', \'{}\');".format('name', 'sale point', 'cash', 'Райымбека 91')
    print('111')
    insert_point = con.proc('insert_point(char(64), char(16), char(16), char(64))')
    print('112233')
    prc =insert_point('name', 'sale point', 'cash', 'Райымбека 91')
    print(prc)
    print('222')


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
    con.execute('DROP TABLE IF EXISTS FormDict')
    con.execute(
        'CREATE TABLE FormDict(' +
        'id SERIAL NOT NULL UNIQUE PRIMARY KEY,' +
        'name char(16)' +
        ')'
    )
    con.execute('DROP TABLE IF EXISTS PaymentDict')
    con.execute(
        'CREATE TABLE PaymentDict(' +
        'id SERIAL NOT NULL UNIQUE PRIMARY KEY,' +
        'name char(16)' +
        ')'
    )
    con.execute('DROP TABLE IF EXISTS Point')
    con.execute(
        'CREATE TABLE Point(' +
        'id SERIAL NOT NULL UNIQUE PRIMARY KEY,' +
        'name char(64),' +
        'form_id integer NOT NULL REFERENCES FormDict ON DELETE RESTRICT,' +
        'payment_id integer NOT NULL REFERENCES PaymentDict ON DELETE RESTRICT,' +
        'address char(64)' +
        ')'
    )
    con.execute('DROP TABLE IF EXISTS PointContact')
    con.execute(
        'CREATE TABLE PointContact(' +
        'id SERIAL PRIMARY KEY,' +
        'point_id integer REFERENCES Point(id),' +
        'name char(64),' +
        'contact char(64)' +
        ')'
    )
    con.execute('DROP TABLE IF EXISTS Trader')
    con.execute(
        'CREATE TABLE Trader(' +
        'id SERIAL PRIMARY KEY,' +
        'name char(16)' +
        ')'
    )
    con.execute('DROP TABLE IF EXISTS Trade')
    con.execute(
        'CREATE TABLE Trade(' +
        'id SERIAL PRIMARY KEY,' +
        'trader_id integer references Trader(id),' +
        'point_id integer references Point(id),' +
        'count integer,' +
        'sale money,' +
        'date DATE NOT NULL DEFAULT CURRENT_DATE' +
        ')'
    )
