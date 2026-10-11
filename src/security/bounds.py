class MemoryBoundsChecker:
    def __init__(self):
        self.regions = {
            "TEXT":  {"start": 0x00000000, "end": 0x00000FFF, "perm": "RX"},
            "DATA":  {"start": 0x00001000, "end": 0x00001FFF, "perm": "RW"},
            "STACK": {"start": 0x00002000, "end": 0x00003FFF, "perm": "RW"},
        }

    def validate_access(self, address: int, access_type: str) -> bool:
        for region_name, bounds in self.regions.items():
            if bounds["start"] <= address <= bounds["end"]:
                if access_type in bounds["perm"]:
                    return True
                else:
                    print(f"[SECURITY VIOLATION] Permission Denied ({access_type}) in {region_name} region at 0x{address:08X}")
                    return False
        
        print(f"[SECURITY VIOLATION] Out-of-Bounds Access to unmapped memory at 0x{address:08X}")
        return False