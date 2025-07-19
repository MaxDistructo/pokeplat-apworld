from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Range, Toggle

class Goal(Choice):
    """
    Determines what you goal is to consider the game beaten.

    - Champion: Become the champion
    - Champion2: Beat the Champion and Elite 4 twice
    """
    display_name = "Goal"
    default = 0
    option_champion = 0
    option_champion2 = 1
    
class RandomizeBadges(Choice):
    """
    Adds Badges to the pool.

    - Vanilla: Gym leaders give their own badge
    - Shuffle: Gym leaders give a random badge
    - Completely Random: Badges can be found anywhere
    """
    display_name = "Randomize Badges"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2

class RandomizeHms(Choice):
    """
    Adds HMs to the pool.

    - Vanilla: HMs are at their vanilla locations
    - Shuffle: HMs are shuffled among vanilla HM locations
    - Completely Random: HMs can be found anywhere
    """
    display_name = "Randomize HMs"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2

class RandomizeKeyItems(DefaultOnToggle):
    """
    Adds most key items to the pool.

    These are usually required to unlock a location or region
    """
    display_name = "Randomize Key Items"

class RandomizeEventTickets(Toggle):
    """
    Adds the event tickets to the pool, which let you access legendaries by sailing from Lilycove.
    """
    display_name = "Randomize Event Tickets"

class RandomizeRods(Toggle):
    """
    Adds fishing rods to the pool.
    """
    display_name = "Randomize Fishing Rods"

class RandomizeOverworldItems(DefaultOnToggle):
    """
    Adds items on the ground with a Pokeball sprite to the pool.
    """
    display_name = "Randomize Overworld Items"

class RandomizeHiddenItems(Toggle):
    """
    Adds hidden items to the pool.
    """
    display_name = "Randomize Hidden Items"

class RandomizeNpcGifts(Toggle):
    """
    Adds most gifts received from NPCs to the pool (not including key items or HMs).
    """
    display_name = "Randomize NPC Gifts"

class ExpModifier(Range):
    """
    Multiplies gained experience by a percentage.

    100 is default
    50 is half
    200 is double
    etc.
    """
    display_name = "Exp Modifier"
    range_start = 0
    range_end = 1000
    default = 100

class BlindTrainers(Toggle):
    """
    Trainers will not start a battle with you unless you talk to them.
    """
    display_name = "Blind Trainers"

class TrainerSanity(Choice):
    """
    Randomizes trainers, their levels and their parties.

    - Off: No randomization
    - Shuffle: Trainers are shuffled among each other
    - Completely Random: Trainers are completely randomized
    """
    display_name = "Trainersanity"
    default = 0
    option_off = 0
    option_shuffle = 1
    option_completely_random = 2

class TrainerChecks(Choice):
    """
    Determines if trainer checks are enabled.

    - Off: No trainer checks
    - On: Trainer checks are enabled
    """
    display_name = "Trainer Checks"
    default = 0
    option_off = 0
    option_on = 1

class PokemonPlatinumGameOptions(PerGameCommonOptions):
    goal: Goal
    badges: RandomizeBadges
    hms: RandomizeHms
    key_items: RandomizeKeyItems
    event_tickets: RandomizeEventTickets
    rods: RandomizeRods
    overworld_items: RandomizeOverworldItems
    hidden_items: RandomizeHiddenItems
    npc_gifts: RandomizeNpcGifts
    trainersanity: TrainerSanity
    trainer_checks: TrainerChecks
    
    exp_modifier: ExpModifier
    blind_trainers: BlindTrainers