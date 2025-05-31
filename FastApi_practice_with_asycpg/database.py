import asyncpg
import database
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

# async def get_connection():
#         return await asyncpg.connect(
#         host=os.getenv("DB_HOST"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         database=os.getenv("DB_NAME")
# )

async def get_connection():
        return await asyncpg.connect(
                host="localhost",
                user="postgres",
                password="Sani@123",
                database="FastAPI"
        )