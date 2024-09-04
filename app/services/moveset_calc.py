from .constants import MOVESET_DF, ELITE_DF

def find_moveset(pokemon_name, base_name, elite_tm):
    moveset = {}

    pokemon_moves = MOVESET_DF.loc[MOVESET_DF['Pokemon'].str.lower() == (pokemon_name)]
    pokemon_moves.sort_values(by=['ER'], ascending=False) # sort by ER (descending)

    if not elite_tm and base_name in ELITE_DF['name'].str.lower().values:
        elite_moves = ELITE_DF[ELITE_DF['name'].str.lower() == base_name]['elite'].values[0].split(', ') # getting elite moves for specific pokemon
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
    moveset = {}

    pokemon_moves = MOVESET_DF.loc[MOVESET_DF['Pokemon'].str.contains(base_name, case=False)]

    if pokemon_moves.empty:
        return None

    for _, row in pokemon_moves.iterrows():
        variant_name = row['Pokemon'].lower()
        moveset[variant_name] = find_moveset(variant_name, base_name, elite_tm)
    
    moveset = filter_moveset(moveset, variants)

    return moveset
