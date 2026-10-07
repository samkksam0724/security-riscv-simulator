class Memory:
    def __init__(self, size_bytes: int = 1024 * 1024):  # 1 MB default memory
        self.size = size_bytes
        self.memory = bytearray(size_bytes)

    def read_word(self, address: int) -> int:
        """Reads a 32-bit word from word-aligned memory (little-endian)."""
        if address < 0 or address + 3 >= self.size:
            raise ValueError(f"Memory read out of bounds at 0x{address:08X}")
        return int.from_bytes(self.memory[address:address+4], byteorder='little')

    def write_word(self, address: int, value: int):
        """Writes a 32-bit word to word-aligned memory (little-endian)."""
        if address < 0 or address + 3 >= self.size:
            raise ValueError(f"Memory write out of bounds at 0x{address:08X}")
        self.memory[address:address+4] = (value & 0xFFFFFFFF).to_bytes(4, byteorder='little')