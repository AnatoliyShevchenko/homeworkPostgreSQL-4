from typing import Any
import psycopg2
from psycopg2.extensions import (ISOLATION_LEVEL_AUTOCOMMIT, connection as Connection, cursor as Cursor)
from dotenv import load_dotenv

from config import (HOST, PORT, PASSWORD, USER,)

class Connection:
    def __init__(self) -> None:
        try:
            self.connection: Connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT
            )
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            print('Connection Successful')
            cursor = self.connection.cursor()
            cursor.execute("CREATE DATABASE workonclass3;")
            print('Database is successful created!')
        except:
            try:
                self.connection: Connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                database='workonclass3'
                )
                self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                print('Connection successful')
            except:
                print('all is created')

    def __new__(cls: type[Any]) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connection, cls).__new__(cls)

        return cls.instance

    def create_tables(self):
        with self.connection.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY, 
                    name VARCHAR(70), 
                    login VARCHAR(50) UNIQUE, 
                    password VARCHAR(50),
                    wallet INTEGER);

                CREATE TABLE IF NOT EXISTS articles(
                    id SERIAL PRIMARY KEY, 
                    title VARCHAR(70), 
                    content TEXT, 
                    user_id INTEGER);

                CREATE TABLE IF NOT EXISTS friends(
                    user_id INTEGER NOT NULL,
                    friend_id INTEGER NOT NULL);    
            """)
        self.connection.commit()
        print('[INFO] table is created!')

    def create_user(self, name: str, login: str, password: str, wallet: int) -> str:
        with self.connection.cursor() as cur:
            cur.execute(f"""
                INSERT INTO users(name, login, password, wallet)
                VALUES ('{name}','{login}','{password}', {wallet});
            """)
        self.connection.commit()
        print('[INFO] user is created!')

    def create_article(self, title: str, content: str, user_id: int) -> str:
        with self.connection.cursor() as cur:
            cur.execute(f"""
                INSERT INTO articles(title, content, user_id)
                VALUES ('{title}','{content}','{user_id}');
            """)
        self.connection.commit()
        print('[INFO] article is created!')

    def get_artile(self) -> list[tuple]:
        data: list[tuple] 
        with self.connection.cursor() as cur:
            cur.execute(f"""SELECT * FROM articles;""")
            data = cur.fetchall()
        self.connection.commit()
        print('[INFO] getting articles!')
        return data

    def get_user(self) -> list[tuple]:
        data: list[tuple] 
        with self.connection.cursor() as cur:
            cur.execute(f"""SELECT * FROM users;""")
            data = cur.fetchall()
        self.connection.commit()
        print('[INFO] user is created!')
        return data

    def add_friend(self, user_id, friend_id):
        with self.connection.cursor() as cur:
            cur.execute(f"""
                INSERT INTO friends (user_id, friend_id)
                VALUES ({user_id}, {friend_id});

                INSERT INTO friends (user_id, friend_id)
                VALUES ({friend_id}, {user_id});
            """)
            print(f"[INFO] User {user_id} add friend {friend_id}")
        self.connection.commit()

    def get_current_user(self, id: int):
        data: list[tuple] = []
        with self.connection.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM users WHERE id={id};
            """)
            data = cur.fetchall()

        return data

    def get_all_friends(self, id):
        data: list[tuple] = []
        friends_id: list[tuple] = []
        with self.connection.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM friends WHERE user_id={id};
            """)
            friends_id = cur.fetchall()

        for item in friends_id:
            with self.connection.cursor() as cur:
                cur.execute(f"""
                    SELECT * FROM users WHERE id={item[1]};
                """)
                data.append(cur.fetchall())

        return data

    def searching(self, name: str):
        data: list[tuple] = []
        temp = str(name)
        with self.connection.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM users WHERE name='{temp}';
            """)
            data = cur.fetchall()
            print(data)

        return data

    def close_connection(self):
        # self.cursor.close()
        self.connection.close()
        print('[INFO] connection is close')
