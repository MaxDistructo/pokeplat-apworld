from typing import Dict, Optional, Set
from NetUtils import ClientStatus
from worlds import _bizhawk
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk.context import BizHawkClientContext
from worlds.pokemonplatinum.statics import FLAGS_OFFSET, GAME_NAME, GLOBAL_PTR, NUM_FLAGS, SAVE_FILE_OFFSET, VERSION_POINTER_OFFSET
from .data.flags import Flags
from .options import Goal

def get_address_from_offset(ctx: "BizHawkClientContext", offset: int) -> int:
    """
    Convert an offset to an address based on the game's memory map.
    """
    # Platinum uses ASLR so we have to calculate the address of flags dynamically
    global_ptr = ctx.read_memory(GLOBAL_PTR, 3)
    version_ptr = ctx.read_memory(global_ptr + VERSION_POINTER_OFFSET, 3)

def read_from_save_file(ctx: "BizHawkClientContext", offset: int, size: int) -> bytes:
    # u24_le
    global_ptr = ctx.read_memory(GLOBAL_PTR, 3)
    version_ptr = ctx.read_memory(global_ptr + VERSION_POINTER_OFFSET, 3)
    save_file_ptr = version_ptr + SAVE_FILE_OFFSET
    return ctx.read_memory(save_file_ptr + offset, size)

def check_if_flag_set(flag: Flags, bitmap: bytes) -> bool:
    """
    Check if a specific flag is set in the bitmap.
    """
    byte_index = flag.value // 8
    bit_index = flag.value % 8
    if byte_index < len(bitmap):
        return (bitmap[byte_index] & (1 << bit_index)) != 0
    return False

class PokemonPlatinumClient(BizHawkClient):
    game = GAME_NAME
    system = "NDS"
    patch_suffix = ".applatinum"

    local_checked_locations: Set[int]
    local_set_events: Dict[str, bool]
    local_found_key_items: Dict[str, bool]
    local_defeated_legendaries: Dict[str, bool]
    goal_flag: Optional[int]

    current_map: Optional[int]

    def initialize_client(self):
        self.local_checked_locations = set()
        self.local_set_events = {}
        self.local_found_key_items = {}
        self.local_defeated_legendaries = {}
        self.goal_flag = None
        self.current_map = None

async def game_watcher(self, ctx: "BizHawkClientContext"):
    """
    Watch for game state changes, such as map changes or flag updates.
    """
    if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
        return
    if ctx.slot_data["goal"] == Goal.option_champion:
        self.goal_flag = Flags.FLAG_GAME_COMPLETED
    elif ctx.slot_data["goal"] == Goal.option_champion2:
        self.goal_flag = Flags.FLAG_CHAMPION_02
    
    try: 
        flags = read_from_save_file(ctx, FLAGS_OFFSET, NUM_FLAGS / 8)
        if not ctx.finished_game and check_if_flag_set(self.goal_flag, flags):
            ctx.finished_game = True
            await ctx.send_msgs([
                {
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL,
                }
            ])
    except _bizhawk.RequestFailedError:
        pass
        
