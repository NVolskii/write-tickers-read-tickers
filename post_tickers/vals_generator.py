from random import random
import time
import psycopg2


CREATE_TABLE_QUERY = '''DROP TABLE IF EXISTS tickers_values;

CREATE TABLE tickers_values(
   ticker_value_id INT GENERATED ALWAYS AS IDENTITY,
   ticker_name VARCHAR(255) NOT NULL,
   ticker_value INT NOT NULL,
   processed_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY(ticker_value_id)
);'''

INSERT_VALUES_QUERY = '''INSERT INTO tickers_values(
    ticker_name,
    ticker_value
)
VALUES (%s, %s)
'''

PG_CONF = {
    'dbname': 'postgres',
    'host': 'localhost',
    'port': 55000,
    'user': 'postgres',
    'password': 'postgrespw',
}

def create_table():
    with psycopg2.connect(**PG_CONF) as conn:
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_QUERY)


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement

def generate_tickers():
    return [(f'ticker_{i:02}', 0) for i in range(100)]

def main():
    tickers = generate_tickers()
    with psycopg2.connect(**PG_CONF) as conn:
        cur = conn.cursor()
        cur.executemany(
                INSERT_VALUES_QUERY, tickers
            )
        time.sleep(1)
        while True:
            tickers = [(tick, val + generate_movement()) for (tick, val) in tickers]
            cur.executemany(
                INSERT_VALUES_QUERY, tickers
            )
            conn.commit()
            time.sleep(1)


if __name__ == '__main__':
    create_table()
    main()