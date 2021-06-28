import os
import psycopg2
from psycopg2.extras import DictCursor


def connect():
    '''
    Подключение к БД
    '''
    DATABASE_URL = os.environ['DATABASE_URL']
    return psycopg2.connect(DATABASE_URL, sslmode='require')


def purge_table(conn):
    '''
    Удаление таблицы из БД
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        truncate = "TRUNCATE shopping_list"
        cursor.execute(truncate)
        conn.commit()
    return


def get_items(conn, user_id, for_cost=False, for_recipes=False):
    '''
    Получение списка покупок пользователя
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        if for_cost == True:
            select = (f"SELECT product, quantity FROM shopping_list WHERE user_id = '{user_id}' "
                      f"AND quantity <> 0;")
        elif for_recipes == True:
            select = (f"SELECT product FROM shopping_list WHERE user_id = '{user_id}' "
                      f"AND quantity <> 0;")
        else:
            select = (f"SELECT product, quantity, units FROM shopping_list WHERE user_id = '{user_id}' "
                      f"AND quantity <> 0;")
        cursor.execute(select)
        records = cursor.fetchall()
    return records


def add_items(conn, user_id, products, quantities, units):
    '''
    Добавление продуктов в список покупок пользователя
    '''
    if products is None:
        return

    quantities = [quantity if isinstance(quantity, int) else 1 for quantity in quantities]
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        rows = list(zip(*(products, quantities, units)))
        VALUES = ', '.join((f"('{user_id}', '{row[0]}', {row[1]}, "
                            f"'{-1 if row[2] is None else row[2]}', current_timestamp(0))") for row in rows)
        insert = f"""INSERT INTO
                        shopping_list (user_id, product, quantity, units, created_on)
                     VALUES
                        {VALUES}
                     ON CONFLICT ON CONSTRAINT shopping_list_user_id_product_key DO UPDATE
                        SET quantity = shopping_list.quantity + excluded.quantity,
                            created_on = current_timestamp(0),
                            units = excluded.units;"""
        cursor.execute(insert)
        conn.commit()
    return


def del_items(conn, user_id, products=None, quantities=None, all=False):
    '''
    Удаление продуктов из списка покупок пользователя
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        if all or products is None:
            update = f"""UPDATE shopping_list
                         SET quantity = 0
                         WHERE user_id = '{user_id}';"""
        else:
            quantities = [quantity if isinstance(quantity, int) else 1000 for quantity in quantities]
            rows = list(zip(*(products, quantities)))
            CONDITIONS = '\n'.join((f"WHEN product = '{row[0]}'"
                                    f"THEN GREATEST(quantity - {row[1]}, 0)") for row in rows)
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


def update_freq(conn, user_id, products):
    '''
    Обновление частоты рекомендаций товара
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        update = f"""UPDATE shopping_list
                     SET frequency = array_append(frequency, current_timestamp(0) - shopping_list.created_on)
                     WHERE user_id = '{user_id}'
                           AND product IN ({', '.join("'" + product + "'" for product in products)})
                           AND quantity = 0;"""
        cursor.execute(update)
        conn.commit()
    return


def get_freq(conn, user_id, recommend=True):
    '''
    Получение частоты рекомендаций товара
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        select = (f"SELECT product, frequency, created_on FROM shopping_list WHERE user_id = '{user_id}' "
                  f"AND frequency is NOT NULL "
                  f"AND quantity = 0;")
        cursor.execute(select)
        records = cursor.fetchall()
    return records


def get_cost(conn, products):
    '''
    Получение стоимости товаров
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        select = (f"""SELECT product, price FROM product_prices
                      WHERE product IN ({', '.join("'" + product + "'" for product in products)});""")
        cursor.execute(select)
        records = cursor.fetchall()
    return records


def add_recipes(conn, user_id, recs_recipe):
    '''
    Добавление рекомендованных рецептов для пользователя
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        insert = f"""UPDATE shopping_list
                     SET recs = ARRAY[{', '.join("'" + rec_recipe + "'" for rec_recipe in recs_recipe)}]
                     WHERE user_id = '{user_id}'"""
        cursor.execute(insert)
        conn.commit()
    return


def get_recipes(conn, user_id):
    '''
    Получение рекомендованных рецептов для пользователя
    '''
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        select = (f"""SELECT recs FROM shopping_list
                      WHERE user_id = '{user_id}'
                      LIMIT 1;""")
        cursor.execute(select)
        records = cursor.fetchall()
    return records
