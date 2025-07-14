from worlds.Files import APProcedurePatch, APTokenMixin
from worlds.pokemonplatinum.statics import GAME_NAME


class PokemonPlatinumProcedurePatch(APProcedurePatch, APTokenMixin):
    game = GAME_NAME
    # POKEMON PL (CPUE01, Rev.00)
    hash = "d66ad7a2a0068b5d46e0781ca4953ae9"
    patch_file_ending = ".applatinum"
    result_file_ending = ".nds"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"])
    ]