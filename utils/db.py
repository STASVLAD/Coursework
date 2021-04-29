import psycopg2
from psycopg2.extras import DictCursor


def connect():
    return psycopg2.connect(dbname='postgres', user='postgres', password='coursework')


def purge_table(conn):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        truncate = "TRUNCATE shopping_list"
        cursor.execute(truncate)
        conn.commit()
    return


def get_items(conn, user_id):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        select = f"SELECT product, quantity FROM shopping_list WHERE user_id = '{user_id}'" + \
                 f"AND quantity <> 0;"
        cursor.execute(select)
        records = cursor.fetchall()
    return records


def add_items(conn, user_id, products, quantity):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        rows = list(zip(*(products, quantity)))
        VALUES = ', '.join(f"('{user_id}', '{row[0]}', {row[1]}, current_timestamp(0))" for row in rows)
        insert = f"""INSERT INTO 
                        shopping_list (user_id, product, quantity, created_on)
                     VALUES 
                        {VALUES}
                     ON CONFLICT ON CONSTRAINT shopping_list_user_id_product_key DO UPDATE
                        SET quantity = shopping_list.quantity + excluded.quantity,
                            created_on = current_timestamp(0);"""
        cursor.execute(insert)
        conn.commit()
    return


def del_items(conn, user_id, products=None, quantity=None, all=False):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        if all:
            update = f"""UPDATE shopping_list
                         SET quantity = 0
                         WHERE user_id = '{user_id}';"""
        else:
            rows = list(zip(*(products, quantity)))
            CONDITIONS = '\n'.join(f"WHEN product = '{row[0]}'" +
                                   f"THEN GREATEST(quantity - {row[1]}, 0)" for row in rows)
            update = f"""UPDATE shopping_list
                         SET quantity = CASE
                            {CONDITIONS}
                            ELSE quantity
                         END
                         WHERE user_id = '{user_id}';"""
        cursor.execute(update)
        conn.commit()
    return


def is_new_user(conn, user_id):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        select = f"SELECT user_id FROM shopping_list WHERE user_id = '{user_id}'"
        cursor.execute(select)
        records = cursor.fetchall()
    return records
