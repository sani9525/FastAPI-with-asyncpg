from database import get_connection

user_data='''
CREATE TABLE IF NOT EXISTS UserData(
    id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100) UNIQUE
)'''

async def create_table():
    conn=await get_connection()
    try:
        await conn.execute(user_data)
    except Exception as e:
        return e
    finally:
        await conn.close()