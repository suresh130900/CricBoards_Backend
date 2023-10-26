import re
from bson import json_util
from fastapi import FastAPI, status, Depends, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import Models.matches as ms
import bcrypt
import Services.Match_service as Match_ser
from DB.Db_Connect import db_connection

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return json_util._json_convert(Match_ser.find_all_matches())


@app.post("/addMatch", status_code=status.HTTP_201_CREATED)
async def add_new(matches: ms.Matches):
    adding_match = Match_ser.add_matches(matches=matches)
    if adding_match:
        return {
            "error": "false",
            "Message": "Data Inserted SuccessFully"
        }
    else:
        return {
            "error": "true",
            "Message": "Something Went Wrong"
        }


@app.post("/update", status_code=status.HTTP_200_OK)
async def update_match(matches: ms.Matches):
    updating_match = update_match(matches=matches)
    if updating_match is -1:
        return {
            "error": "true",
            "Message": "Match Does not exists"
        }
    elif updating_match > 0:
        return {
            "error": "false",
            "Message": "Data Updated SuccessFully"
        }
    else:
        return {
            "error": "true",
            "Message": "Something Went Wrong"
        }


@app.delete("/delete/{match_number}", status_code=status.HTTP_200_OK)
async def deleting_match(match_number: str):
    response = Match_ser.delete_match(match_number=match_number)
    print(match_number)
    if response is -1:
        return {
            "error": "true",
            "Message": "Match Does not exits"
        }
    elif response > 0:
        return {
            "error": "false",
            "Message": "Data Deleted SuccessFully"
        }
    else:
        return {
            "error": "true",
            "Message": "Something Went Wrong"
        }


db = db_connection()

users = db.get_collection("users")


class User(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


def validate_email(email: str) -> bool:
    regex = r"[^@]+@[^@]+\.[^@]+"
    return re.fullmatch(regex, email)


@app.post("/user/signup")
async def signup_new(user: User):
    if validate_email(user.email):
        if users.find({'email': user.email}).retrieved > 0:
            return {
                'error': True,
                'message': user.email + " already exist, please login directly"
            }
        else:
            pass_bytes = bytes(user.password, 'utf-8')
            salt = bcrypt.gensalt()
            enc_pass = bcrypt.hashpw(pass_bytes, salt=salt)
            users.insert_one({'name': user.name, 'email': user.email, 'password': enc_pass})
            return {
                'error': False,
                'message': "" + user.name + " signup success !"
            }
    else:
        return {
            'error': True,
            'message': user.email + " is not valid"
        }


@app.post("/user/login")
async def login_user(user: UserLogin):
    if validate_email(user.email):
        u = users.find_one({'email': user.email})
        if u is not None:
            dec_pass = bcrypt.checkpw(bytes(user.password, 'utf-8'), u['password'])
            if dec_pass:
                return {
                    'error': False,
                    'message': 'match success'
                }
            else:
                return {
                    'error': True,
                    'message': 'match failed'
                }
        else:
            return {
                'error': True,
                'message': user.email + " does not exist, please signup first"
            }
    else:
        return {
            'error': True,
            'message': user.email + " is not valid"
        }
