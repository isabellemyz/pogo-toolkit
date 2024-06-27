import pandas as pd

moveset_df = pd.read_csv('/Users/isabellez/pogo-toolkit/app/data/movesets.csv')
elite_df = pd.read_csv('/Users/isabellez/pogo-toolkit/app/data/elite.csv')

def calculate_moveset(pokemon_name, elite_tm):
    pokemon_name = pokemon_name.lower() # for casing purposes
    moveset = {} # return moveset corresponding to highest ER FOR THAT POKEMON
    pokemon_moves = moveset_df.loc[moveset_df['Pokemon'].str.lower() == pokemon_name] # focus in on specific pokemon first
    pokemon_moves.sort_values(by=['ER'], ascending=False) # sort by ER (descending)

    if not elite_tm and pokemon_name in elite_df['name'].str.lower().values: # user does not want elite tm and pokemon does have elite tm options
        elite_moves = elite_df[elite_df['name'].str.lower() == pokemon_name]['elite'].values[0].split(', ') # getting elite moves for specific pokemon
        pokemon_moves = pokemon_moves[~pokemon_moves.apply(lambda row: any(move in elite_moves for move in [row['Fast Move'], row['Charged Move']]), axis=1)]
    
    moveset['fast move'] = pokemon_moves.loc[pokemon_moves['ER'].idxmax(), 'Fast Move']
    moveset['charged move'] = pokemon_moves.loc[pokemon_moves['ER'].idxmax(), 'Charged Move']

    return moveset