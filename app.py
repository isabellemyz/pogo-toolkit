from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__, static_url_path='/static')

pokemon_list_url = 'https://gist.githubusercontent.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6/raw/92200bc0a673d5ce2110aaad4544ed6c4010f687/pokemon.csv'
types_chart_url = 'https://raw.githubusercontent.com/zonination/pokemon-chart/master/chart.csv'

pokemon_df = pd.read_csv(pokemon_list_url)
types_chart_df = pd.read_csv(types_chart_url)
types_chart_df.set_index('Attacking', inplace=True) # set attacking column as index for the dataframe

def calculate_type_weakness(pokemon_name):
    # focus in on specific pokemon
    pokemon = pokemon_df.loc[pokemon_df['Name'].str.lower() == pokemon_name.lower()]

    # check that pokemon exists
    if pokemon.empty:
        return f"\"{pokemon_name}\" not found"

    # find type(s) of pokemon
    types = pokemon.iloc[0][['Type 1', 'Type 2']].dropna().values
    # print(types)
    # print(type(types))

    # now the hard part...
    # this type is DEFENDING so we look at column names

    # streamlined process:
    # take weaknesses
    # take resistances
    # get rid of any overlap (will be none for single types)

    weaknesses = []
    strengths = []

    for type_ in types:
        type_col = types_chart_df.loc[:, type_]

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
    return weaknesses

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weakness', methods=['POST'])
def weakness():
    pokemon_name = request.form['pokemon_name'].capitalize()
    weaknesses = calculate_type_weakness(pokemon_name)
    all_weaknesses = [
        {"name": "BUG", "color": "#A6B91A"},
        {"name": "DARK", "color": "#705746"},
        {"name": "DRAGON", "color": "#6F35FC"},
        {"name": "ELECTRIC", "color": "#F7D02C"},
        {"name": "FAIRY", "color": "#D685AD"},
        {"name": "FIGHTING", "color": "#C22E28"},
        {"name": "FIRE", "color": "#EE8130"},
        {"name": "FLYING", "color": "#A98FF3"},
        {"name": "GHOST", "color": "#735797"},
        {"name": "GRASS", "color": "#7AC74C"},
        {"name": "GROUND", "color": "#E2BF65"},
        {"name": "ICE", "color": "#96D9D6"},
        {"name": "NORMAL", "color": "#A8A77A"},
        {"name": "POISON", "color": "#A33EA1"},
        {"name": "PSYCHIC", "color": "#F95587"},
        {"name": "ROCK", "color": "#B6A136"},
        {"name": "STEEL", "color": "#B7B7CE"},
        {"name": "WATER", "color": "#6390F0"}  
    ]
    return render_template('index.html', pokemon_name=pokemon_name, weaknesses=weaknesses, all_weaknesses=all_weaknesses)

if __name__ == "__main__":
    app.run(debug=True)

# def main():
#     while True:
#         pokemon_name = input("Enter a Pokémon name (or 'exit' to quit): ").strip().capitalize()
#         if pokemon_name.lower() == 'exit':
#             break
#         weaknesses = calculate_type_weakness(pokemon_name)
#         print(f"Weaknesses for {pokemon_name}: {weaknesses}")

# if __name__ == "__main__":
#     main()