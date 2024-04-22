import schemeas
from database import database
from fastapi import APIRouter, Depends
from dotenv import load_dotenv
import os
from typing import Annotated
import sqlite3

load_dotenv()
DATABASE_PATH = os.getenv("DATABASE_PATH")

router = APIRouter(tags=["users"])

@router.post("/register/")
def register_user(request: schemeas.UserCreate, connection: Annotated[sqlite3.Connection, Depends(database.get_db)]):
    with connection:
        cursor = connection.cursor()
        if (cursor.execute("""
                            SELECT username
                            FROM Users
                            WHERE
                            username=(?)
                            """, (request.username,)).fetchone() != None):
            return {"message", "Username Already Exists"}
        
        if (cursor.execute("""
                            SELECT email
                            FROM Users
                            WHERE
                            email=(?)
                            """, (request.email,)).fetchone() != None):
            return {"message", "Email Already Exists"}
        
        cursor.execute("""
                        INSERT INTO Users ('username', 'hashed_password', 'email', 'user_type') VALUES (?, ?, ?, ?)
                        """, 
                        (request.username, request.password, request.email, request.accountType)
                        )
    return request