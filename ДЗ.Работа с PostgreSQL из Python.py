# Домашнее задание к лекции «Работа с PostgreSQL из Python»
# Создайте программу для управления клиентами на Python.
#
# Требуется хранить персональную информацию о клиентах:
#
# имя,
# фамилия,
# email,
# телефон.
# Сложность в том, что телефон у клиента может быть не один, а два, три и даже больше.
# А может и вообще не быть телефона, например, он не захотел его оставлять.
#
# Вам необходимо разработать структуру БД для хранения информации и несколько функций
# на Python для управления данными.
#
# 1)Функция, создающая структуру БД (таблицы).
# 2)Функция, позволяющая добавить нового клиента.
# 3)Функция, позволяющая добавить телефон для существующего клиента.
# 4)Функция, позволяющая изменить данные о клиенте.
# 5)Функция, позволяющая удалить телефон для существующего клиента.
# 6)Функция, позволяющая удалить существующего клиента.
# 7)Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.



# Внвчале создадим базу данных client и подключимся к ней.
# Пароль для подключения - личный
import psycopg2




with psycopg2.connect(database="client", user="postgres", password="password") as conn:
    with conn.cursor() as cur:
        #удаление таблиц
        # cur.execute("""
        #        DROP TABLE phones;
        #        DROP TABLE clients;
        #        """)

        # 1)Функция, создающая структуру БД (таблицы).
        def creating_tables (cursor):
            # создание таблицы client
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients(
                    client_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(60) NOT NULL ,
                    last_name VARCHAR(60) NOT NULL ,
                    email VARCHAR(120) UNIQUE NOT NULL 
                    );
                """)
            # создание таблицы телефонов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS phones (
                    phone_id SERIAL PRIMARY KEY,
                    client_id  INTEGER NOT NULL REFERENCES clients(client_id),
                    number INTEGER 
                    );
                """)
            conn.commit()  # фиксируем в БД


        tables= creating_tables(cur)



        # 2) Функция, позволяющая добавить нового клиента.

        # # Добавим без функции


        def add_client(cursor, first_name, last_name, email):
            cursor.execute("""
            INSERT INTO clients (first_name, last_name, email )
            VALUES (%s, %s, %s);
            """ , (first_name, last_name, email ))


        client_1 = add_client(cur, 'Ivan', 'Petrov', 'ivan@python.com')
        client_2 = add_client ( cur ,'Petr','Ivanov', 'petr@python.com')
        client_3 =  add_client ( cur ,'Anton','Vasin', 'anton@python.com')
        client_4 =  add_client ( cur ,'Igor','Valin', 'ig@python.com')
        client_5 = add_client(cur, 'Irina', 'Li', 'li@python.com')

        # 3)Функция, позволяющая добавить телефон для существующего клиента

        def add_phone(cursor, client_id, number=None):
            cursor.execute("""
                        INSERT INTO phones (client_id, number)
                        VALUES (%s, %s );
                        """, (client_id, number))

        phone_2 = add_phone(cur,1,22233322)
        phone_3 = add_phone(cur,2)
        phone_4 = add_phone(cur, 3, 11122233)
        phone_5 = add_phone(cur, 3, 11122234)
        phone_6 = add_phone(cur, 4, 55522233)
        phone_7 = add_phone(cur, 5, 11100077)


        # 4.Функция, позволяющая изменить данные о клиенте .

        def new_data(cursor, client_id, first_name=None, last_name=None, email=None):
            cursor.execute("""
                                  UPDATE clients SET first_name=%s , last_name=%s , email=%s WHERE client_id=%s;
                                  """, (first_name, last_name, email, client_id))


        new_client_3 = new_data(cur, 1, 'Ivanko', 'Petrov', 'iv@python.com')

        # 5)Функция, позволяющая удалить телефон для существующего клиента.

        def delete_phone (cursor,client_id):
            cursor.execute("""
            DELETE FROM  phones WHERE client_id=%s;    
            """, (client_id ,))

        client_delete_phone_1 = delete_phone ( cur, 3 )


       # 6) Функция, позволяющая удалить существующего клиента.

        def delete_client(cursor, client_id):
            delete_phone(cursor, client_id)
            cursor.execute("""
                    DELETE FROM  clients WHERE client_id=%s;    
                    """, (client_id,))


        client_delete_1 = delete_client (cur,3)

        # 7) Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону

        def find_client(cursor,first_name=None, last_name=None,email=None, number=None):
            ''' Функция определяет id клиента
            по одному из параметров - имени , фамилии , адресу электронной почты ,
            либо номеру его телефона '''
            cursor.execute("""
                SELECT cl.client_id FROM clients cl
                JOIN phones ph ON cl.client_id = ph.client_id
                WHERE first_name=%s OR last_name=%s OR email=%s OR number=%s ;
                """, (first_name,last_name,email,number,))
            return cursor.fetchone()[0]


        required_client_1 = find_client(cur,'','Li','',)
        print (required_client_1)




conn.close()

