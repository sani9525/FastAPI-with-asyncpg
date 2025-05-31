from fastapi import FastAPI,HTTPException
from model import get_model
from database import get_connection
from schema import Res_model,User,Update_user,search_by_id
import json
from typing import Any

app=FastAPI()

@app.on_event("startup")
async def startup_event():
    await get_model()


async def read_json(path) -> Any:
    try:
        with open(path, "r") as file:
            content=file.read()
            data = json.loads(content) if content.strip() else []
    except FileNotFoundError:
        data = []
    return data


async def update_json(path,data: Any):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


@app.get("/get_users")
async def get_users():
    conn=await get_connection()
    if conn is None:
        raise HTTPException(status_code=500,detail="Failed to connect to the database")
    try:
        res=await conn.fetch('''select name,email from "user"''')
        return res
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        await conn.close()



@app.post("/add_users",response_model=Res_model)
async def add_users(data:User):
    d=await read_json("user.json")
    d.append(data.dict())
    await update_json("user.json",d)
    conn=await get_connection()
    if conn is None:
        raise HTTPException(status_code=500,detail="Failed to connect to the database")
    try:
        check=await conn.fetchrow('''SELECT * FROM "user" WHERE email=$1''',data.email)
        if check:
            raise HTTPException(status_code=400,detail="User already exists")
        usr_data='''INSERT INTO
                    "user"(name,email,password)
                    VALUES($1,$2,$3)
                    RETURNING name, email '''
        res=await conn.fetchrow(usr_data,data.name,data.email,data.password)
        return dict(res)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        await conn.close()


@app.post("/get_user_id")
async def get_user_by_id(data:search_by_id):
    conn=await get_connection()
    if conn is None:
        raise HTTPException(status_code=500,detail="Failed to connect to the database")
    try:
        res= await conn.fetchrow('''SELECT * from "user" where email=$1''',data.email)
        if res is None:
            raise HTTPException(status_code=404, detail="User not found")
        return dict(res)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        await conn.close()



@app.put("/update_user")
async def update_users(email:str,data: Update_user):
    conn=await get_connection()
    if conn is None:
        raise HTTPException(status_code=500,detail="Failed to connect to the database")
    try:
        found=await conn.fetchrow('''SELECT * FROM "user" WHERE email=$1''',email)
        if found is None:
            raise HTTPException(status_code=404,detail="User does not exists")
        up_user=('''UPDATE "user"
                   SET name=$1,password=$2
                   WHERE email=$3''')
        await conn.execute(up_user,data.name,data.password,email)
        return {"message":"User updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        await conn.close()




@app.delete("/delete_user")
async def del_user(email:str):
    conn=await get_connection()
    if conn is None:
        raise HTTPException(status_code=500,detail="Failed to connect to the database")
    try:
        await conn.execute('''DELETE FROM "user" WHERE email=$1''',email)
        return {"message":"User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        await conn.close()





if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)