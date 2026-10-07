import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.memory import Memory
from src.core.pipeline import PipelinedCore

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
print(f"Total Clock Cycles: {core.cycles}")