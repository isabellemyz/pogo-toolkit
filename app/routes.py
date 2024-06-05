from flask import Blueprint, render_template, request, g
from .services.calculator import calculate_type_weakness
# from .services.scraper import get_latest_raid_info
from .services.scraper import find_bosses

main = Blueprint('main', __name__)

@main.before_request
def before_request():
    g.bosses = find_bosses('https://leekduck.com/boss/')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/weakness', methods=['POST'])
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

# @main.route('/raids')
# def raids():
#     bosses = find_bosses('https://leekduck.com/boss/')
#     return render_template('raid_info.html', bosses=bosses)
