import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.memory import Memory
from src.core.pipeline import PipelinedCore
from src.security.canary import StackCanaryGuard
from src.security.bounds import MemoryBoundsChecker

# ==========================================
# PART 1: STAGE 1 HARDWARE CORE PIPELINE TEST
# ==========================================
print("=== Stage 1: Pipeline Execution Test ===")
mem = Memory()
core = PipelinedCore(mem)

# Load machine code program into memory starting at 0x0000
# 1. addi x1, x0, 10   -> 0x00A00093
# 2. addi x2, x0, 20   -> 0x01400113
# 3. add  x3, x1, x2   -> 0x002081B3
program = [0x00A00093, 0x01400113, 0x002081B3]

for i, inst in enumerate(program):
    mem.write_word(i * 4, inst)

print("Running pipeline simulation...")
# Run for 10 clock cycles to clear the 5-stage pipeline
for _ in range(10):
    core.step()

print("\n--- Final Register File State ---")
print(f"x1 (Expected 10): {core.rf.read(1)}")
print(f"x2 (Expected 20): {core.rf.read(2)}")
print(f"Total Clock Cycles: {core.cycles}\n")

# ==========================================
# PART 2: STAGE 2 SECURITY MONITORING TEST
# ==========================================
print("=== Stage 2: Security Monitoring Test ===")
canary = StackCanaryGuard(canary_val=0xDEADBEEF)
bounds = MemoryBoundsChecker()

print("--- Testing Stack Canary Guard ---")
stack_addr = 0x00002000
canary.place_canary(stack_addr)

# Legitimate canary check
assert canary.verify_canary(stack_addr, 0xDEADBEEF) == True
print("Legitimate canary check passed!")

# Trigger simulated overflow attack
canary.verify_canary(stack_addr, 0x41414141)

print("\n--- Testing Memory Bounds Checker ---")
# Valid memory access
assert bounds.validate_access(0x00001004, "R") == True
print("Legitimate memory access allowed!")

# Trigger out-of-bounds access attack
bounds.validate_access(0x00009000, "W")