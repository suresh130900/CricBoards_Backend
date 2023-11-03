import json
import re
from fastapi import FastAPI, status, Depends, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import Models.matches as ms
import bcrypt
import Services.Match_service as Match_ser
from DB.Db_Connect import db_connection
from bson import json_util
import Services.test as test
import json


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


@app.get("/test")
async def test1():
    # return json_util._json_convert(test.all_matches("./Services/ipl_matches_2008_2022.csv").replace("/", '""'))
    return json.loads(test.all_matches("./Services/ipl_matches_2008_2022.csv"))


@app.get("/all_teams")
async def all_teams_test():
    return test.all_teams()


@app.get("/all_venue")
async def all_venue():
    return test.all_venues()


@app.get("/Matches_played")
async def matches_played():
    dict_data = [json.loads(item) for item in test.Matches_played_by_each_team()]
    return dict_data


@app.get("/Matches_won")
async def matches_won():
    # Convert the keys to strings
    data = test.Matches_won_by_each_team().replace("('", "").replace("',)", "")

    # Parse the modified data as JSON
    parsed_data = json.loads(data)

    # Now, you have a dictionary
    print(parsed_data)
    return parsed_data


@app.get("/Man_of_match")
async def man_of_match():
    return json.loads(test.Man_of_match())


@app.get("/top_batsman")
async def top_batsman():
    return json.loads(test.Top_batsman())


def Worst_bowler(data):
    merged_data = {}
    for key in data["bowler"]:
        bowler_name = data["bowler"][key]
        total_runs = data["total_run"][key]
        merged_data[bowler_name] = total_runs
    return merged_data


@app.get("/worst_bowler")
async def worst_bowler():
    return json.loads(test.Worst_bowler())


@app.get('/team_wise_bolwer')
def Bowler_team_wise():
    return json.loads(test.Bowler_team_performance())


@app.get("/virat_bumrah")
def Virat_Bumrah():
    return test.virat_bumrah()


@app.get("/runs_faced_by_batsman_facing_bowler")
def RunsFacedByBatsmanFacingBowler(batsman_name: str, bowler_name: str):
    return test.runs_faced_by_batsman_facing_bowler(batsman_name, bowler_name)


@app.get("/dismissal_counts")
def DismissalCounts():
    return json.loads(test.get_dismissal_counts())


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


