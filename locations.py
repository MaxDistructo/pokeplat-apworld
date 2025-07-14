from typing import List, Optional
from BaseClasses import Location
from worlds.pokemonplatinum.statics import GAME_NAME


class PokemonPlatinumLocation(Location):
    game = GAME_NAME
    location_requirements: Optional[List[str]]
    location_name: str

