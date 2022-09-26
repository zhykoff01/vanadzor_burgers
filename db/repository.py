import psycopg2

import db.config


class SqlRepository:
    conn = None

    def __init__(self) -> None:
        try:
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(
                host="ec2-52-210-97-223.eu-west-1.compute.amazonaws.com",
                port="5432",
                user="kbyqdyjvlbgtby",
                password="4733ea467695edd4d3341d2e2761b6c761b52e593cd9d1c94b657b83ec62e040",
                database="dfvgjiu109718d",
                options="-c search_path=VB"
            )
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def print_version(self):
        cur = self.conn.cursor()
        try:
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            print(db_version)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cur.close()

    def is_user_exist(self, user_id):
        cur = self.conn.cursor()
        try:
            cur.execute('''SELECT * FROM users WHERE user_id = %s''', [int(user_id)])
            some_response = cur.fetchone()
            return len(some_response) > 0
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cur.close()

    def save_user(self, user_id, username):
        cur = self.conn.cursor()
        try:
            cur.execute('''INSERT INTO users (user_id, username) values (%s,%s)''', [int(user_id), str(username)])
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()
        finally:
            cur.close()
