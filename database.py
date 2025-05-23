import asyncpg

async def get_connection():
    return await asyncpg.connect(
        host="localhost",
        database="jsw",
        user="postgres",
        password="Sani@123"
    )