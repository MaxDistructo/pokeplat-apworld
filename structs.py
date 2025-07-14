class PokemonPlatinumSlotData:
    # char[32]
    seed_name: str
    team_number: int
    slot_number: int
    # u16
    exp_modifier: int
    #u8
    blind_trainers: int

    def to_bytes(self) -> bytes:
        return (
            self.seed_name.encode('utf-8').ljust(32, b'\x00') +
            self.team_number.to_bytes(4, 'little') +
            self.slot_number.to_bytes(4, 'little') +
            self.exp_modifier.to_bytes(2, 'little') +
            self.blind_trainers.to_bytes(1, 'little')
        )

class PokemonPlatinumAPItem:
    # u16
    item_id: int
    # u8
    quantity: int

    def to_bytes(self) -> bytes:
        return (
            self.item_id.to_bytes(2, 'little') +
            self.quantity.to_bytes(1, 'little')
        )

class PokemonPlatinumAPData:
    # u16
    item_count: int
    # PokemonPlatinumAPItem[item_count]
    items: list[PokemonPlatinumAPItem]
    # u8
    locked: int
    # Bitfield
    badges: int

    def to_bytes(self) -> bytes:
        items_bytes = b''.join(item.to_bytes() for item in self.items)
        return (
            self.item_count.to_bytes(2, 'little') +
            items_bytes +
            self.locked.to_bytes(1, 'little') +
            self.badges.to_bytes(1, 'little')
        )