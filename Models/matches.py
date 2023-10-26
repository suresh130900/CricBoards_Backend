from pydantic import BaseModel

from DB.Db_Connect import db_connection

db = db_connection()
matches_played = db.get_collection("match")
print(matches_played)


class Matches(BaseModel):
    id: str
    city: str
    match_date: str
    season: str
    match_number: str
    team1: str
    team2: str
    venue: str
    toss_winner: str
    toss_decision: str
    superover: str
    winning_team: str
    won_by: str
    margin: str
    method: str
    player_of_match: str
    umpire1: str
    umpire2: str

