import postgresql


def db_connet():
    con = postgresql.open('pq://postgres:torn@185.143.173.37:5432/dbmarket')
    test(con)


def test(con):
    con.execute(
        'CREATE TABLE formcat(' +
	    'id SERIAL PRIMARY KEY,' +
	    'name char(16) NOT NULL CHECK (name <> ''),' +
	    ')'
    )
    con.execute(
        'CREATE TABLE paymentcat(' +
	    'id SERIAL PRIMARY KEY,' +
	    'name char(16) NOT NULL CHECK (name <> ''),' +
	    ')'
    )
    con.execute(
        'CREATE TABLE countcat(' +
	    'id SERIAL PRIMARY KEY,' +
	    'name char(16) NOT NULL CHECK (name <> ''),' +
	    'description char(64),' +
	    ')'
    )
    con.execute(
        'CREATE TABLE point(' +
	    'id SERIAL PRIMARY KEY,' +
	    'name char(64) NOT NULL CHECK (name <> ''),' +
	    'form_id integer references formcat(id),' +
	    'payment_id integer references paymentcat(id),' +
	    'count_id integer references countcat(id),' +
	    ')'
    )
    con.execute(
        'CREATE TABLE trader(' +
	    'id SERIAL PRIMARY KEY,' +
	    'name char(16) NOT NULL CHECK (name <> ''),' +
	    ')'
    )
    con.execute(
        'CREATE TABLE trade(
	    'id SERIAL PRIMARY KEY,
	    'trader_id integer references trader(id),
	    'point_id integer references point(id),
	    'count integer,
	    'sale money,
	    'date DATE NOT NULL DEFAULT CURRENT_DATE
	    ')'
    )

# CREATE TABLE region (
#  region_id SERIAL PRIMARY KEY,
#  name varchar(40) NOT NULL CHECK (name <> ''),
#  station varchar(40) NOT NULL CHECK (name <> '')
# );
