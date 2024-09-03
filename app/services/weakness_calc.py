import pandas as pd
from .constants import POKEMON_DF, TYPES_DF

types_df = TYPES_DF
types_df.set_index('Attacking', inplace=True) # set attacking column as index for the dataframe

def find_weaknesses(pokemon_name):
    pokemon = POKEMON_DF.loc[POKEMON_DF['name'].str.lower() == pokemon_name] # look at specific one
    # print('#find weaknesses', pokemon_name)
    # print('find weaknesses df', pokemon)

    types = pokemon.iloc[0][['type1', 'type2']].dropna().values

    # print('# find weaknesses types', types)

    weaknesses = set()
    strengths = set()

    for type_ in types:
        type_col = types_df.loc[:, type_]
        # print('#find weaknesses type col', type_col)

        weak_against = type_col[type_col == 2].index.tolist()
        strong_against = type_col[type_col == 0.5].index.tolist()

        weaknesses.update(weak_against)
        strengths.update(strong_against)

        # print('#find weaknesses weaknesses before filter', weaknesses)
        # print('#find weaknesses strengths before filter', strengths)
    
    weaknesses = list(weaknesses)
    strengths = list(strengths)

    # for dual types - strengths cancel out weaknesses
    for weakness in weaknesses[:]:
            if weakness in strengths:
                # print(weakness)
                weaknesses.remove(weakness)
    
    # print('#find weaknesses weaknesses after filter', weaknesses)

    return weaknesses


def filter_variants(weaknesses, variants):
    print(variants)
    if variants:
        filtered_weaknesses = {
            name: weakness for name, weakness in weaknesses.items()
            if any(variant in name for variant in variants)
        }

        return filtered_weaknesses
    
    return weaknesses

def calculate_type_weakness(pokemon_name, variants):
    print(variants)

    base_name = pokemon_name.lower()

    # print(base_name)
    # pokemon_name = format_name(pokemon_name, variants)

    weaknesses = {}

    pokemon = POKEMON_DF.loc[POKEMON_DF['name'].str.contains(base_name, case=False)]

    if pokemon.empty:
        return "POKÉMON NOT FOUND"

    for _, row in pokemon.iterrows():
        variant_name = row['name'].lower()
        weaknesses[variant_name] = find_weaknesses(variant_name)
    
    weaknesses = filter_variants(weaknesses, variants)

    return weaknesses