from database import get_connection

create_table='''
CREATE TABLE IF NOT EXISTS "user"(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
)'''

async def get_model():
    conn=await get_connection()
    if conn is None:
        print("failed to connect to the database")
        return {"message":"failed to connect to the database"}
    try:
        await conn.execute(create_table)
    except Exception as e:
        return {"message": str(e)}
    finally:
        await conn.close()