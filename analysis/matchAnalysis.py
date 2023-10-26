import Models.matches as all_matches


def allMatches():
    return (
        all_matches.matches_played.find({
            'city',
            'match_date',
            'team1',
            'team2',
            'winning_team',
            'venue',
            'match_number'
        })
    )