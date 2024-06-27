import pandas as pd

pokemon_df = pd.read_csv('/Users/isabellez/pogo-toolkit/app/data/all.csv')
types_url = 'https://raw.githubusercontent.com/zonination/pokemon-chart/master/chart.csv'
types_df = pd.read_csv(types_url)
types_df.set_index('Attacking', inplace=True) # set attacking column as index for the dataframe

def calculate_type_weakness(pokemon_name):
    # focus in on specific pokemon
    pokemon = pokemon_df.loc[pokemon_df['name'].str.lower() == pokemon_name.lower()]
    print('og df', pokemon_df)
    print('pokemon df', pokemon)

    # check that pokemon exists
    if pokemon.empty:
        return "POKÉMON NOT FOUND"

    # find type(s) of pokemon
    types = pokemon.iloc[0][['type1', 'type2']].dropna().values
    print('types', types)
    # print(types)
    # print(type(types))

    # this type is DEFENDING so we look at column names

    # streamlined process:
    # take weaknesses
    # take resistances
    # get rid of any overlap (will be none for single types)

    weaknesses = []
    strengths = []

    for type_ in types:
        type_col = types_df.loc[:, type_]

        weak_against = type_col[type_col == 2].index.tolist()
        strong_against = type_col[type_col == 0.5].index.tolist()

        weaknesses.extend(weak_against)
        strengths.extend(strong_against)

    # for dual types - strengths cancel out weaknesses
    for weakness in weaknesses[:]:
            if weakness in strengths:
                # print(weakness)
                weaknesses.remove(weakness)
            else:
                weaknesses[weaknesses.index(weakness)] = weaknesses[weaknesses.index(weakness)].upper()
    
    # return ", ".join(weaknesses)
    print('weaknesses', weaknesses)
    return weaknesses