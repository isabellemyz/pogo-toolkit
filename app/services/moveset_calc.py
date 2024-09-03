import pandas as pd
from .constants import MOVESET_DF, ELITE_DF
from .helpers import format_name

'''
* can enter main pokemon name and then optional specifications:
    * alolan, hisuian, galarian
    * (blank) form/forme
    * shadow
    * mega evolution
    * other
* based on each of these, query will manipulate so that it can match what's in the CSV
    * alolan, hisuian, galarian, shadow, mega: put before main pokemon name
        * if shadow & another one of those: put shadow first
    * (blank) form/forme, other: put in parentheses and append to main pokemon name
    * if something bizarre gets entered it will just come up blank
* if only main pokemon name is entered then return info for ALL VARIANTS
'''

# def calculate_moveset(pokemon_name, elite_tm, variants = []):

#     moveset = {} # return moveset corresponding to highest ER FOR THAT POKEMON
#     pokemon_moves = MOVESET_DF.loc[MOVESET_DF['Pokemon'].str.lower() == pokemon_name] # focus in on specific pokemon first
#     pokemon_moves.sort_values(by=['ER'], ascending=False) # sort by ER (descending)

#     if not elite_tm and pokemon_name in ELITE_DF['name'].str.lower().values: # user does not want elite tm and pokemon does have elite tm options
#         elite_moves = ELITE_DF[ELITE_DF['name'].str.lower() == pokemon_name]['elite'].values[0].split(', ') # getting elite moves for specific pokemon
#         pokemon_moves = pokemon_moves[~pokemon_moves.apply(lambda row: any(move in elite_moves for move in [row['Fast Move'], row['Charged Move']]), axis=1)] # filters out elite moves for specific pokemon
    
#     moveset['fast move'] = pokemon_moves.loc[pokemon_moves['ER'].idxmax(), 'Fast Move']
#     moveset['charged move'] = pokemon_moves.loc[pokemon_moves['ER'].idxmax(), 'Charged Move']

#     return moveset

def find_moveset(pokemon_name, elite_tm):
    moveset = {}

    pokemon_moves = MOVESET_DF.loc[MOVESET_DF['Pokemon'].str.lower() == (pokemon_name)]
    pokemon_moves.sort_values(by=['ER'], ascending=False) # sort by ER (descending)

    if not elite_tm and pokemon_name in ELITE_DF['name'].str.lower().values: # check this
        elite_moves = ELITE_DF[ELITE_DF['name'].str.lower() == pokemon_name]['elite'].values[0].split(', ') # getting elite moves for specific pokemon
        pokemon_moves = pokemon_moves[~pokemon_moves.apply(lambda row: any(move in elite_moves for move in [row['Fast Move'], row['Charged Move']]), axis=1)] # filters out elite moves for specific pokemon
    
    moveset['fast move'] = pokemon_moves.loc[pokemon_moves['ER'].idxmax(), 'Fast Move']
    moveset['charged move'] = pokemon_moves.loc[pokemon_moves['ER'].idxmax(), 'Charged Move']

    return moveset

def filter_moveset(moveset, variants):
    if variants:
        filtered_moveset = {
            name: moveset for name, moveset in moveset.items()
            if any(variant in name for variant in variants)
        }

        return filtered_moveset
    
    return moveset


def calculate_moveset(pokemon_name, variants, elite_tm):
    base_name = pokemon_name
    pokemon_name = format_name(pokemon_name, variants) # may be unnecessary

    moveset = {}

    pokemon_moves = MOVESET_DF.loc[MOVESET_DF['Pokemon'].str.contains(base_name, case=False)]

    if pokemon_moves.empty:
        return "POKÉMON NOT FOUND"

    for _, row in pokemon_moves.iterrows():
        variant_name = row['Pokemon'].lower()
        moveset[variant_name] = find_moveset(variant_name, elite_tm)
    
    moveset = filter_moveset(moveset, variants)

    print(moveset)

    return moveset
