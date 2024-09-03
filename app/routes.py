from flask import Blueprint, render_template, request, g
from .services.weakness_calc import calculate_type_weakness
from .services.scraper import find_bosses
from .services.moveset_calc import calculate_moveset

main = Blueprint('main', __name__)

@main.before_request
def before_request():
    g.bosses = find_bosses('https://leekduck.com/boss/')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/weakness', methods=['POST'])
def weakness():
    pokemon_name = request.form['pokemon_name']
    variants = request.form['variants'].split(', ')
    weaknesses = calculate_type_weakness(pokemon_name, variants) # returns dict
    return render_template('index.html', pokemon_name_w=pokemon_name, weaknesses=weaknesses)

@main.route('/moveset', methods=['POST'])
def moveset():
    pokemon_name = request.form['pokemon_name']
    variants = request.form['variants'].split(', ')
    moveset = calculate_moveset(pokemon_name, variants, False) # TODO: integrate Elite TM flag on frontend and pass to backend
    return render_template('index.html', pokemon_name_m=pokemon_name, moveset=moveset)
