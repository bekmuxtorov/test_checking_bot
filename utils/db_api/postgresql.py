from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        phone_number VARCHAR(20) NOT NULL,
        created_at timestamp with time zone NOT NULL DEFAULT NOW()  
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_tests(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Tests (
        id SERIAL PRIMARY KEY, 
        test_count INT NOT NULL,
        answers VARCHAR(255) NOT NULL,
        created_user BIGINT REFERENCES Users(telegram_id) ON DELETE CASCADE ON UPDATE CASCADE,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW() 
        )
        """
        await self.execute(sql, execute=True)

    async def create_table_results(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Results (
        id SERIAL PRIMARY KEY, 
        test BIGINT REFERENCES Tests(id) ON DELETE CASCADE ON UPDATE CASCADE,
        telegram_user BIGINT REFERENCES Users(telegram_id) ON DELETE CASCADE ON UPDATE CASCADE,
        user_answers VARCHAR(255) NOT NULL,
        true_count INT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW() 
        )
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    # users
    async def add_user(self, full_name, username, telegram_id, phone_number, created_at):
        sql = "INSERT INTO Users (full_name, username, telegram_id, phone_number, created_at) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, full_name, username, telegram_id, phone_number, created_at, fetchrow=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        user = await self.execute(sql, *parameters, fetchrow=True)
        return {
            "id": user[0],
            "full_name": user[1],
            "username": user[2],
            "telegram_id": user[3],
            "phone_number": user[4],
        } if user else None

    # tests
    async def add_test(self, test_count, answers, created_user, created_at):
        print(f"oldin: {created_at}")
        sql = "INSERT INTO Tests (test_count, answers, created_user, created_at) VALUES($1, $2, $3, $4) returning *"
        test = await self.execute(sql, test_count, answers, created_user, created_at, fetchrow=True)
        print(f"keyin: {test}")
        return {
            "id": test[0],
            "test_count": test[1],
            "answers": test[2],
            "created_user": test[3],
            "created_at": test[4]
        } if test else None

    async def select_test(self, **kwargs):
        sql = "SELECT * FROM Tests WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        test = await self.execute(sql, *parameters, fetchrow=True)
        return {
            "id": test[0],
            "test_count": test[1],
            "answers": test[2],
            "created_user": test[3],
            "created_at": test[4]
        } if test else None

    # results
    async def add_result(self, test, telegram_user, user_answers, true_count, created_at):
        sql = "INSERT INTO Results (test, telegram_user, user_answers, true_count, created_at) VALUES($1, $2, $3, $4, $5) returning *"
        result = await self.execute(sql, test, telegram_user, user_answers, true_count, created_at, fetchrow=True)
        return {
            "id": result[0],
            "test": result[1],
            "user": result[2],
            "user_answers": result[3],
            "true_answers": result[4],
            "created_at": result[5],
        } if result else None

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        user = await self.execute(sql, *parameters, fetchrow=True)
        return user

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
