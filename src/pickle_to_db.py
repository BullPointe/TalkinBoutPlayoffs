import pickle
from scrape import PlayerStatistics

def main():
    # starts by loading pickle from scrape.py
    pc1 = PlayerStatistics()
    pc1.tables = pc1.load_in_tables_from_pickle('pc1_tables_dict.pickle')
    df = pc1.tables['Defense']
    print(df['Fumbles returned for a touchdown'])
    aggregation_functions = {'Sacks':'sum','Interceptions':'sum','Interception Return Touchdowns':'sum','Forced Fumbles':'sum','Safeties':'sum'}
    df_new = df.groupby(df['Team']).agg(aggregation_functions)
    print(df_new)
    

if __name__ == "__main__":
    main()
