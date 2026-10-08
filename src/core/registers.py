class RegisterFile:
    def __init__(self):
        # 32 general-purpose 32-bit registers (x0 to x31)
        self.regs = [0] * 32

    def read(self, reg_num: int) -> int:
        """Read value from register (x0 is hardwired to 0)."""
        if reg_num == 0:
            return 0
        return self.regs[reg_num] & 0xFFFFFFFF

    def write(self, reg_num: int, value: int):
        """Write 32-bit integer to register (x0 is hardwired to 0)."""
        if reg_num != 0:
            self.regs[reg_num] = value & 0xFFFFFFFF

    def __repr__(self):
        return "\n".join([f"x{i:02d}: 0x{self.regs[i]:08X}" for i in range(32)])