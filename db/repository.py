from config import database


class SqlRepository:

    async def is_user_exist(self, user_id):
        await database.execute('''SELECT * FROM users WHERE user_id = %s''', [int(user_id)])
        some_response = database.fetch_one()
        return len(some_response) > 0

    async def save_user(self, user_id, username):
        await database.execute('''INSERT INTO users(user_id, username) values (%s, %s)''',
                               [int(user_id), str(username)])

