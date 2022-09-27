import psycopg2

import db.config


class SqlRepository:
    conn = None

    def __init__(self) -> None:
        try:
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(
                db.config.DATABASE_URL,
                sslmode="require",
                options="-c search_path=vb"
            )
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    async def print_version(self):
        cur = self.conn.cursor()
        try:
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            print(db_version)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cur.close()

    async def is_user_exist(self, user_id):
        cur = self.conn.cursor()
        try:
            cur.execute('''SELECT * FROM users WHERE user_id = %s''', [int(user_id)])
            some_response = cur.fetchone()
            return some_response is not None and len(some_response) > 0
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cur.close()

    async def save_user(self, user_id, username, language_code):
        cur = self.conn.cursor()
        try:
            cur.execute('''INSERT INTO users (user_id, username, language_code) values (%s,%s,%s)''',
                        [int(user_id), str(username), str(language_code)])
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()
        finally:
            cur.close()
