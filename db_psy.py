import psycopg2
from config import db_config


def db_connet():

    conn = None
    try:
        conn = psycopg2.connect(db_config())
        test(conn)
        fill_dics(conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("err")
    finally:
        if conn is not None:
            conn.close()

    insert_point('name1', 'sale point', 'real', 'Дильмухамеда 91')
    insert_point_contact('name1', 'Kamil', '8 701 449 19 12')
    insert_trader('Erba')
    insert_trade('Erba', 'name1', '10', '15000')


def insert_point_contact(point_name, contact_name, contact):
    conn = None
    try:
        conn = psycopg2.connect(db_config())
        params = {'var_point_name': point_name, 'var_contact_name': contact_name, 'var_contact': contact}
        exec_to(conn, 'insert_point_contact', params)
        conn.commit()
    except Exception as error:
        print('err| {}'.format(error))
    finally:
        if conn is not None:
            conn.close()


def insert_point(name, formfactor, payment, address):
    conn = None
    try:
        conn = psycopg2.connect(db_config())
        params = {'var_name': name, 'var_form': formfactor, 'var_payment': payment, 'var_address': address}
        exec_to(conn, 'insert_point', params)
        conn.commit()
    except Exception as error:
        print('err| {}'.format(error))
    finally:
        if conn is not None:
            conn.close()


def insert_trader(name):
    conn = None
    try:
        conn = psycopg2.connect(db_config())
        params = {'var_trader_name': name}
        exec_to(conn, 'insert_trader', params)
        conn.commit()
    except Exception as error:
        print('err| {}'.format(error))
    finally:
        if conn is not None:
            conn.close()


def insert_trade(trader_name, point_name, count, sale):
    conn = None
    try:
        conn = psycopg2.connect(db_config())
        params = {'var_trader_name': trader_name, 'var_point_name': point_name, 'var_count': count, 'var_sale': sale}
        exec_to(conn, 'insert_trade', params)
        conn.commit()
    except Exception as error:
        print('err| {}'.format(error))
    finally:
        if conn is not None:
            conn.close()


def exec_to(conn, func, params):
    cur = conn.cursor()
    cur.callproc(func, params)
    cur.close()


def fill_dics(conn):
    cur = conn.cursor()
    # formdict
    cur.execute("INSERT INTO FormDict (name) VALUES ('market point')")
    cur.execute("INSERT INTO FormDict (name) VALUES ('chain point')")
    cur.execute("INSERT INTO FormDict (name) VALUES ('sale point')")

    #paymentdict
    cur.execute("INSERT INTO PaymentDict (name) VALUES ('cash')")
    cur.execute("INSERT INTO PaymentDict(name) VALUES ('real')")
    cur.execute("INSERT INTO PaymentDict(name) VALUES ('cons')")
    cur.execute("INSERT INTO PaymentDict(name) VALUES ('unknown')")
    cur.close()
    conn.commit()


def test(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS FormDict')
    cur.execute(
        'CREATE TABLE FormDict(' +
        'id SERIAL NOT NULL UNIQUE PRIMARY KEY,' +
        'name char(16)' +
        ')'
    )
    cur.execute('DROP TABLE IF EXISTS PaymentDict')
    cur.execute(
        'CREATE TABLE PaymentDict(' +
        'id SERIAL NOT NULL UNIQUE PRIMARY KEY,' +
        'name char(16)' +
        ')'
    )
    cur.execute('DROP TABLE IF EXISTS Point')
    cur.execute(
        'CREATE TABLE Point(' +
        'id SERIAL NOT NULL UNIQUE PRIMARY KEY,' +
        'name char(32),' +
        'form_id integer NOT NULL REFERENCES FormDict ON DELETE RESTRICT,' +
        'payment_id integer NOT NULL REFERENCES PaymentDict ON DELETE RESTRICT,' +
        'address char(32)' +
        ')'
    )
    cur.execute('DROP TABLE IF EXISTS PointContact')
    cur.execute(
        'CREATE TABLE PointContact(' +
        'id SERIAL PRIMARY KEY,' +
        'point_id integer REFERENCES Point(id),' +
        'name char(32),' +
        'contact char(32)' +
        ')'
    )
    cur.execute('DROP TABLE IF EXISTS Trader')
    cur.execute(
        'CREATE TABLE Trader(' +
        'id SERIAL PRIMARY KEY,' +
        'name char(16)' +
        ')'
    )
    cur.execute('DROP TABLE IF EXISTS Trade')
    cur.execute(
        'CREATE TABLE Trade(' +
        'id SERIAL PRIMARY KEY,' +
        'trader_id integer references Trader(id),' +
        'point_id integer references Point(id),' +
        'count integer,' +
        'sale money,' +
        'date DATE NOT NULL DEFAULT CURRENT_DATE' +
        ')'
    )
    cur.execute("CREATE OR REPLACE FUNCTION insert_point(" +
                "var_name char(32), " +
                "var_form char(16), " +
                "var_payment char(16), " +
                "var_address char(32)) " +
                "RETURNS integer AS $$ " +
                "DECLARE " +
                "form_id int; " +
                "payment_id int; " +
                "BEGIN " +
                "form_id := (SELECT id FROM FormDict WHERE name=var_form); " +
                "payment_id := (SELECT id FROM PaymentDict WHERE name=var_payment); " +
                "INSERT INTO Point (name, form_id, payment_id, address) " +
                "VALUES (var_name, form_id, payment_id, var_address); " +
                "RETURN 1;" +
                "END; " +
                "$$ LANGUAGE plpgsql ; "
                )
    cur.execute("CREATE OR REPLACE FUNCTION insert_point_contact(" +
                "var_point_name char(32), " +
                "var_contact_name char(32), " +
                "var_contact char(32)) " +
                "RETURNS integer AS $$ " +
                "DECLARE " +
                "point_id int; " +
                "BEGIN " +
                "point_id := (SELECT id FROM Point WHERE name=var_point_name); " +
                "INSERT INTO PointContact (point_id, name, contact) " +
                "VALUES (point_id, var_contact_name, var_contact); " +
                "RETURN 1;" +
                "END; " +
                "$$ LANGUAGE plpgsql ; "
                )
    cur.execute("CREATE OR REPLACE FUNCTION insert_trader(" +
                "var_trader_name char(32)) "
                "RETURNS integer AS $$ " +
                "BEGIN " +
                "INSERT INTO Trader (name) " +
                "VALUES (var_trader_name); " +
                "RETURN 1;" +
                "END; " +
                "$$ LANGUAGE plpgsql ; "
                )
    cur.execute("CREATE OR REPLACE FUNCTION insert_trade(" +
                "var_trader_name char(32), " +
                "var_point_name char(32), " +
                "var_count integer, " +
                "var_sale money) " +
                "RETURNS integer AS $$ " +
                "DECLARE " +
                "point_id int; " +
                "trader_id int; " +
                "BEGIN " +
                "trader_id := (SELECT id FROM Trader WHERE name=var_trader_name); " +
                "point_id := (SELECT id FROM Point WHERE name=var_point_name); " +
                "INSERT INTO Trade (trader_id, point_id, count, sale) " +
                "VALUES (trader_id, point_id, var_count, var_sale); " +
                "RETURN 1;" +
                "END; " +
                "$$ LANGUAGE plpgsql ; "
                )
    cur.close()
    conn.commit()
