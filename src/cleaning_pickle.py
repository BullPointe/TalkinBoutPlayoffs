import pandas as pd

def update_tables(pc1):
    # starts by loading pickle from scrape.py
    # pc1.tables = pc1.load_in_tables_from_pickle('pc1_tables_dict.pickle')
    defense_players = pc1.tables['Defense']
    passing_players = pc1.tables['Passing']
    rushing_players = pc1.tables['Rushing']
    #print(df['Fumbles returned for a touchdown'])
    # need to add support for fumbes returned for touchdown
    pc1.tables['Team Defense'] = defense_players.groupby(defense_players['Team']).agg({'Sacks':'sum','Interceptions':'sum','Interception Return Touchdowns':'sum','Forced Fumbles':'sum','Safeties':'sum','Fumbles returned for a touchdown':'sum'})
    pc1.tables['Team Offense'] = pd.merge(passing_players.groupby(passing_players['Team']).agg({'Passing Yards':'sum'}), rushing_players.groupby(rushing_players['Team']).agg({'Rushing Yards':'sum'}), on='Team')
    # print(pc1.tables['TeamOffense'])
    