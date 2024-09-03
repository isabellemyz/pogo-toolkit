def format_name(pokemon_name, variants):
    pokemon_name = pokemon_name.lower()

    if variants:
        copy = variants.copy()
        for variant in copy:
            variant = variant.lower() # for casing purposes
        
        for variant in ['alolan', 'hisuian', 'galarian', 'mega']:
            if variant in copy:
                pokemon_name = f"{variant} {pokemon_name}"
                copy.remove(variant)
        
        if 'shadow' in variant:
            pokemon_name = f"shadow {pokemon_name}"
            copy.remove('shadow')
        
        if copy:
            pokemon_name += f"{pokemon_name} {' '.join(copy)}"

    return pokemon_name