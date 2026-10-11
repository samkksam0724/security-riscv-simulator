from src.security.canary import StackCanaryGuard
from src.security.bounds import MemoryBoundsChecker

class SecurityMonitor:
    def __init__(self, core):
        """
        Attaches the security monitor directly to the RISC-V CPU pipeline core.
        """
        self.core = core
        self.canary_guard = StackCanaryGuard()
        self.bounds_checker = MemoryBoundsChecker()
        self.security_violations = []

    def inspect_memory_access(self, address: int, access_type: str, data: int = None) -> bool:
        """
        Intercepts memory operations in the MEM stage to validate permissions and canary integrity.
        """
        # 1. Check memory boundary and permission flags (R/W/X)
        if not self.bounds_checker.validate_access(address, access_type):
            violation_msg = f"[CYCLE {self.core.cycles}] Boundary Violation at Address: 0x{address:08X} ({access_type})"
            self.security_violations.append(violation_msg)
            return False

        # 2. Inspect active stack canary if accessing the STACK region
        if self.bounds_checker.regions["STACK"]["start"] <= address <= self.bounds_checker.regions["STACK"]["end"]:
            if access_type == "R" and data is not None:
                if not self.canary_guard.verify_canary(address, data):
                    violation_msg = f"[CYCLE {self.core.cycles}] Stack Canary Corruption at Address: 0x{address:08X}"
                    self.security_violations.append(violation_msg)
                    return False

        return True

    def get_audit_log(self):
        """Returns all security traps flagged during execution."""
        return self.security_violations