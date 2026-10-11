import os

class StackCanaryGuard:
    def __init__(self, canary_val: int = None):
        self.secret_canary = canary_val if canary_val is not None else int.from_bytes(os.urandom(4), 'little')
        self.canary_locations = {}

    def place_canary(self, stack_address: int) -> int:
        self.canary_locations[stack_address] = self.secret_canary
        return self.secret_canary

    def verify_canary(self, stack_address: int, current_val: int) -> bool:
        if stack_address not in self.canary_locations:
            return True
        
        expected = self.canary_locations[stack_address]
        if current_val != expected:
            print(f"[SECURITY TRAP] Stack Buffer Overflow Detected at 0x{stack_address:08X}!")
            print(f"Expected Canary: 0x{expected:08X}, Found: 0x{current_val:08X}")
            return False
        return True