class Instruction:
    def __init__(self, raw_instruction: int):
        self.raw = raw_instruction & 0xFFFFFFFF
        
        # Core opcode field (bits 0-6)
        self.opcode = self.raw & 0x7F
        
        # Register fields
        self.rd = (self.raw >> 7) & 0x1F
        self.funct3 = (self.raw >> 12) & 0x07
        self.rs1 = (self.raw >> 15) & 0x1F
        self.rs2 = (self.raw >> 20) & 0x1F
        self.funct7 = (self.raw >> 25) & 0x7F
        
        # Extracted Immediate based on format type
        self.imm = self._decode_immediate()

    def _decode_immediate(self) -> int:
        """Extracts and sign-extends immediates based on opcode patterns."""
        # I-type
        if self.opcode in [0x13, 0x03, 0x67]:
            imm = (self.raw >> 20) & 0xFFF
            return self._sign_extend(imm, 12)
            
        # S-type (Store)
        elif self.opcode == 0x23:
            imm = ((self.raw >> 25) << 5) | ((self.raw >> 7) & 0x1F)
            return self._sign_extend(imm, 12)
            
        # B-type (Branch)
        elif self.opcode == 0x63:
            imm = (((self.raw >> 31) & 0x1) << 12) | \
                  (((self.raw >> 7) & 0x1) << 11) | \
                  (((self.raw >> 25) & 0x3F) << 5) | \
                  (((self.raw >> 8) & 0xF) << 1)
            return self._sign_extend(imm, 13)
            
        # U-type (LUI / AUIPC)
        elif self.opcode in [0x37, 0x17]:
            return self.raw & 0xFFFFF000
            
        # J-type (JAL)
        elif self.opcode == 0x6F:
            imm = (((self.raw >> 31) & 0x1) << 20) | \
                  (((self.raw >> 12) & 0xFF) << 12) | \
                  (((self.raw >> 20) & 0x1) << 11) | \
                  (((self.raw >> 21) & 0x3F) << 1)
            return self._sign_extend(imm, 21)
            
        return 0

    @staticmethod
    def _sign_extend(val: int, bits: int) -> int:
        """Sign-extends an n-bit integer to a 32-bit signed Python integer."""
        if val & (1 << (bits - 1)):
            return val - (1 << bits)
        return val