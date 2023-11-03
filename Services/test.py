import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json

matches = pd.read_csv("./Services/ipl_matches_2008_2022.csv")
delivery = pd.read_csv("./Services/ipl_ball_by_ball_2008_2022.csv")


def all_matches(n):
    all_Matches = pd.read_csv(n)
    print(all_Matches.to_json())
    return all_Matches.to_json()


def all_teams():
    all_Teams = matches['team1'].tolist() + matches['team2'].tolist()
    all_Teams = list(set(all_Teams))
    return all_Teams


def all_venues():
    all_Venues = matches['venue'].tolist()
    all_Venues = list(set(all_Venues))
    return all_Venues


def Matches_played_by_each_team():
    x = matches['team1'].value_counts()
    y = matches['team2'].value_counts()
    return x.to_json(), y.to_json()


def Matches_won_by_each_team():
    all_matches_won = pd.DataFrame({"Winner": matches['winning_team']}).value_counts()
    print(all_matches_won)
    return all_matches_won.to_json()


def Man_of_match():
    MoM = matches['player_of_match'].value_counts().head()
    print(MoM)
    return MoM.to_json()


def Top_batsman():
    top_batsman = delivery.groupby('batter')['batsman_run'].agg('sum').reset_index().sort_values('batsman_run',
                                                                                                 ascending=False).head(
        10)
    top_batsman.set_index('batter', inplace=True)
    return top_batsman.to_json()


def Worst_bowler():
    worst_bowler = delivery.groupby('bowler')['total_run'].agg('sum').reset_index().sort_values('total_run',
                                                                                                ascending=False).head(
        10)
    merged_data = {}

    for index, row in worst_bowler.iterrows():
        merged_data[row['bowler']] = row['total_run']

    return json.dumps(merged_data)


def Bowler_team_performance():
    mask = delivery['bowler'] == 'PP Chawla'
    return delivery[mask].groupby('batting_team')['total_run'].agg('sum').to_json()


# Now, if you want to know that how many runs Virat Kohli scored when he faced Jasprit Bumrah, use the following code:
def virat_bumrah():
    mask = delivery['bowler'] == 'JJ Bumrah'
    mask2 = delivery['batter'] == 'V Kohli'
    runs = delivery[mask].groupby('batter')['batsman_run'].agg('count').sort_values(ascending=False)['V Kohli']
    return json.dumps(int(runs))  # Convert to a regular Python int and then to JSON


def runs_faced_by_batsman_facing_bowler(batsman_name, bowler_name):
    mask = delivery['batter'] == batsman_name
    mask2 = delivery['bowler'] == bowler_name
    runs = delivery[mask & mask2]['batsman_run'].count()
    return json.dumps(int(runs))


def get_dismissal_counts():
    dismissal_counts = delivery['dismisal_kind'].value_counts().reset_index()
    dismissal_counts.columns = ['dismisal_kind', 'count']
    dismissal_counts_json = dismissal_counts.to_json(orient='records')
    return dismissal_counts_json
