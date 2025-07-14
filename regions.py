from typing import Dict
from BaseClasses import Region
from worlds.pokemonplatinum.statics import GAME_NAME


class PokemonPlatinumRegion(Region):
    game = GAME_NAME
    region_name: str
    region_id: int

    def __init__(self, name: str, region_id: int):
        super().__init__(name)
        self.region_name = name
        self.region_id = region_id

    def __repr__(self):
        return f"{self.game} - {self.region_name} (ID: {self.region_id})"
    
def create_regions(world: "PokemonPlatinumWorld") -> Dict[str, Region]:
    """
    Create regions for the Pokemon Platinum world.
    This function initializes regions based on the game's static data.
    """
    
    