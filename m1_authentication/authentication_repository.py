import os
import oracledb
from pathlib import Path
from dotenv import load_dotenv
from authentication_model import AuthenticationModel

oracledb.defaults.fetch_lobs = False

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class AuthenticationRepository:
    def __init__(self):
        self._connection = None

    async def _get_connection(self):
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')
        dsn = os.getenv('DSN')

        if not all([user, password, dsn]):
            raise ValueError("Missing one or more required DB environment variables")

        try:
            if self._connection is None:
                self._connection = await oracledb.connect_async(
                    user=user,
                    password=password,
                    dsn=dsn
                )
            else:
                try:
                    await self._connection.ping()
                except oracledb.Error:
                    print("Reconnecting due to broken connection...")
                    self._connection = await oracledb.connect_async(
                        user=user,
                        password=password,
                        dsn=dsn
                    )
        except Exception as e:
            print("Connection failed:", e)
            self._connection = None
            raise

        return self._connection

    async def insert_user(self, email, password):
        conn = await self._get_connection()

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO users (email, pass)
                    VALUES (:p_email, :p_pass)
                    """,
                    {'p_email': email, 'p_pass': password}
                )
                await conn.commit()
        except oracledb.IntegrityError as e:
            await conn.rollback()
            raise Exception("User already exists") from e
        except oracledb.Error as e:
            await conn.rollback()
            raise

    async def get_user(self, email):
        conn = await self._get_connection()

        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    SELECT id, email, pass FROM users
                    WHERE email = :p_email
                    """,
                    {'p_email': email}
                )

                row = await cursor.fetchone()

                return AuthenticationModel(id=row[0], email=row[1], password=row[2]) if row else None
        except oracledb.IntegrityError as e:
            raise Exception("User already exists") from e
        except oracledb.Error:
            raise
