import psycopg2
from psycopg2.extras import DictCursor


def connect():
    '''
    Подключение к БД
    '''
    return psycopg2.connect(dbname='postgres', user='postgres', password='coursework')


def purge_table(conn):
    '''
    Удаление таблицы из БД
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        truncate = "TRUNCATE shopping_list"
        cursor.execute(truncate)
        conn.commit()
    return


def get_items(conn, user_id):
    '''
    Получение списка покупок пользователя
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        select = f"SELECT product, quantity FROM shopping_list WHERE user_id = '{user_id}'" + \
                 f"AND quantity <> 0;"
        cursor.execute(select)
        records = cursor.fetchall()
    return records


def add_items(conn, user_id, products, quantities):
    '''
    Добавление продуктов в список покупок пользователя
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        rows = list(zip(*(products, quantities)))
        VALUES = ', '.join(f"('{user_id}', '{row[0]}', {row[1]}, current_timestamp(0))" for row in rows)
        insert = f"""INSERT INTO
                        shopping_list (user_id, product, quantity)
                     VALUES
                        {VALUES}
                     ON CONFLICT ON CONSTRAINT shopping_list_user_id_product_key DO UPDATE
                        SET quantity = shopping_list.quantity + excluded.quantity;"""
        cursor.execute(insert)
        conn.commit()
    return


def del_items(conn, user_id, products=None, quantities=None, all=False):
    '''
    Удаление продуктов из списка покупок пользователя
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        if all:
            update = f"""UPDATE shopping_list
                         SET quantity = 0
                         WHERE user_id = '{user_id}';"""
        else:
            rows = list(zip(*(products, quantities)))
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
    '''
    Проверка на нового пользователя
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        select = f"SELECT user_id FROM shopping_list WHERE user_id = '{user_id}'"
        cursor.execute(select)
        records = cursor.fetchall()
    return records


def update_freq(conn, user_id, products, frequencies):
    '''
    Обновление частоты рекомендаций товара
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        VALUES = ',\n'.join(f"({products[i]}, {frequencies[i]}" for i in range(len(products)))
        update = f"""UPDATE shopping_list
                     SET frequency = tt.frequency
                     FROM
                        ( VALUES
                            {VALUES}
                        ) as tt (product, frequency)
                     WHERE shopping_list.product = tt.product and user_id = '{user_id}';"""
        cursor.execute(update)
        conn.commit()
    return


def get_freq(conn, user_id, recommend=True):
    '''
    Получение частоты рекомендаций товара
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        select = f"SELECT product, frequency FROM shopping_list WHERE user_id = '{user_id}'" + \
                 f"AND quantity = 0;"
        cursor.execute(select)
        records = cursor.fetchall()
    return records


def del_freq(conn, user_id, products):
    '''
    Удаление частоты рекомендаций товара
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        CONDITIONS = f"user_id = '{user_id}' and (" + ' or '.join(f"product = {product}"
                                                                  for product in products) + ")"
        update = f"""UPDATE shopping_list
                     SET frequency = NULL
                     WHERE {CONDITIONS};"""
        cursor.execute(update)
        conn.commit()
    return
