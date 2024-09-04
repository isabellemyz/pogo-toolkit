import pandas as pd
import pandas as pd
import os

# Get the directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

POKEMON_DF = pd.read_csv(os.path.join(DATA_DIR, 'all.csv'))
TYPES_DF = pd.read_csv('https://raw.githubusercontent.com/zonination/pokemon-chart/master/chart.csv')
MOVESET_DF = pd.read_csv(os.path.join(DATA_DIR, 'movesets.csv'))
ELITE_DF = pd.read_csv(os.path.join(DATA_DIR, 'elite.csv'))
