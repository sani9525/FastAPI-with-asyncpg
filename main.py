from fastapi import FastAPI
from model import create_table
from database import get_connection
from schema import UserSchema

app=FastAPI()


@app.on_event("startup")
async def on_startup():
    await create_table()



# getting all the data in database
@app.get("/get_data")
async def get_data():
    conn=await get_connection()
    try:
        return await conn.fetch("SELECT * FROM UserData")
    except Exception as e:
        return e
    finally:
        await conn.close()


# getting data by id from database
@app.get("/getData_by_id/{user_id}")
async def get_data_id(user_id:int):
    conn=await get_connection()
    try:
        row=await conn.fetchrow("SELECT * FROM UserData WHERE id = $1",user_id)
        if row:
            return dict(row)
        else:
            return {"message":"User not found!"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        await conn.close()


# posting user data to the database
@app.post("/add_user")
async def add_user(data:UserSchema):
    conn=await get_connection()
    try:
        insert_data='''INSERT INTO UserData(id, name, email) VALUES($1,$2,$3)'''
        insert_val=(data.id,data.name,data.email)
        await conn.execute(insert_data,*insert_val)
        return {"message": "User added successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        await conn.close()


# updating data to the database

@app.put("/update_user")
async def update_user(data:UserSchema):
    conn=await get_connection()
    try:
        update_data="UPDATE UserData SET name=$1, email=$2 WHERE id=$3"
        update_val=(data.name,data.email,data.id)
        await conn.execute(update_data,*update_val)
        return {"message":"User updated successfully"}
    except Exception as e:
        return {"error":str(e)}
    finally:
        await conn.close()


#deleting the data from database

@app.delete("/delete_user/{user_id}")
async def delete_user(user_id:int):
    conn=await get_connection()
    try:
        delete_user="DELETE FROM UserData WHERE id=$1"
        await conn.execute(delete_user,user_id)
        return {"message":"User deleted successfully"}
    except Exception as e:
        return {"error":str(e)}
    finally:
        await conn.close()
