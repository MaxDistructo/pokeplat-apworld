from BaseClasses import Item
from worlds.pokemonplatinum.statics import GAME_NAME


class PokemonPlatinumItem(Item):
    game = GAME_NAME
    item_name: str
    flag_id: int

    def __init__(self, name: str, player: str, location_name: str, item_name: str):
        super().__init__(name, player, location_name)
        self.item_name = item_name

    def __str__(self) -> str:
        return f"{self.item_name} at {self.location_name} ({self.player})"
    
GAME_ITEMS = {
    PokemonPlatinumItem("")
}