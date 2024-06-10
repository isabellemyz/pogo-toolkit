import pandas as pd

moveset_df = pd.read_csv('/Users/isabellez/pogo-toolkit/app/data/comprehensive_dps.csv')

def calculate_moveset(pokemon_name):
    # return moveset corresponding to highest ER FOR THAT POKEMON
    moveset = {}

    # focus in on specific pokemon first
    pokemon = moveset_df.loc[moveset_df['Pokemon'].str.lower() == pokemon_name.lower()]
    pokemon.sort_values(by=['ER'], ascending=False)

    moveset['fast move'] = pokemon.loc[pokemon['ER'].idxmax(), 'Fast Move']
    moveset['charged move'] = pokemon.loc[pokemon['ER'].idxmax(), 'Charged Move']

    return moveset