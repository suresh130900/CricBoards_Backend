# Finding the Matches
import Models.matches as all_matches


def find_all_matches():
    return all_matches.matches_played.find({})


# Adding Matches
def add_matches(matches: all_matches.Matches):
    inserted_coll = matches.matches_played.insert_one({
        "id": matches.id,
        "city": matches.city,
        "match_date": matches.match_date,
        "season": matches.season,
        "match_number": matches.match_number,
        "team1": matches.team1,
        "team2": matches.team2,
        "venue": matches.venue,
        "toss_winner": matches.toss_winner,
        "toss_decision": matches.toss_decision,
        "superover": matches.superover,
        "winning_team": matches.winning_team,
        "won_by": matches.won_by,
        "margin": matches.margin,
        "method": matches.method,
        "player_of_match": matches.player_of_match,
        "umpire1": matches.umpire1,
        "umpire2": matches.umpire2
    })

    return inserted_coll.acknowledged


# Deleting Matches
def delete_match(match_number: str):
    check_match = all_matches.matches_played.find_one({"match_number": match_number})
    print(check_match)
    if check_match is not None:
        delete = all_matches.matches_played.delete_one({"match_number": match_number})
        return delete.acknowledged
    else:
        return -1


# Updating the Matches
def update_match(matches: all_matches.Matches):
    check_match = matches.matches_played.find_one({"id": matches.id})
    if check_match is not None:
        updating = matches.matches_played.update_one(
            {"id": matches.id},
            {"$set": {
                "id": matches.id,
                "city": matches.city,
                "match_date": matches.match_date,
                "season": matches.season,
                "match_number": matches.match_number,
                "team1": matches.team1,
                "team2": matches.team2,
                "venue": matches.venue,
                "toss_winner": matches.toss_winner,
                "toss_decision": matches.toss_decision,
                "superover": matches.superover,
                "winning_team": matches.winning_team,
                "won_by": matches.won_by,
                "margin": matches.margin,
                "method": matches.method,
                "player_of_match": matches.player_of_match,
                "umpire1": matches.umpire1,
                "umpire2": matches.umpire2}
            })
        return updating.modified_count
    else:
        return -1


