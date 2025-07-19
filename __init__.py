import json
import settings
import typing
from .options import PokemonPlatinumGameOptions  # the options we defined earlier
from .items import mygame_items  # data used below to add items to the World
from .locations import mygame_locations  # same as above'
from .statics import BASE_ID, GAME_NAME
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, RegionType, ItemClassification


class MyGameItem(Item):  # or from Items import MyGameItem
    game = GAME_NAME  # name of the game/world this item is from


class MyGameLocation(Location):  # or from Locations import MyGameLocation
    game = GAME_NAME  # name of the game/world this location is in


class MyGameSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """Insert help text for host.yaml here."""

    rom_file: RomFile = RomFile("Pokemon Platinum (US).nds")


class MyGameWorld(World):
    """Insert description of the world/game here."""
    game = GAME_NAME  # name of the game/world
    options_dataclass = PokemonPlatinumGameOptions  # options the player can set
    options: PokemonPlatinumGameOptions  # typing hints for option results
    settings: typing.ClassVar[MyGameSettings]  # will be automatically assigned from type hint
    topology_present = True  # show path to required location checks in spoiler

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    base_id = BASE_ID
    # instead of dynamic numbering, IDs could be part of data

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: id for
                       id, name in enumerate(mygame_items, base_id)}
    location_name_to_id = {name: id for
                           id, name in enumerate(mygame_locations, base_id)}

    def generate_early(self) -> None:
        item_pool = []
        if self.options.overworld_items:
            visible_items = json.loads("./data/items.json")
        if self.options.hidden_items:
            hidden_items = json.loads("./data/hidden_items.json")
        if self.options.trainer_checks:
            trainer_checks = json.loads("./data/trainers.json")
