from src.core.registers import RegisterFile
from src.core.memory import Memory
from src.core.instructions import Instruction

class PipelineState:
    """Holds data moving between pipeline stages."""
    def __init__(self):
        self.pc = 0
        self.inst = None
        self.rs1_val = 0
        self.rs2_val = 0
        self.alu_result = 0
        self.mem_data = 0
        self.valid = False

class PipelinedCore:
    def __init__(self, memory: Memory):
        self.rf = RegisterFile()
        self.mem = memory
        self.pc = 0

        # Inter-stage registers
        self.if_id = PipelineState()
        self.id_ex = PipelineState()
        self.ex_mem = PipelineState()
        self.mem_wb = PipelineState()

        # Cycle counter for runtime telemetry
        self.cycles = 0

    def step(self):
        """Executes one clock cycle across all 5 stages in reverse order."""
        self.cycles += 1

        # Stage 5: Write Back (WB)
        if self.mem_wb.valid and self.mem_wb.inst:
            inst = self.mem_wb.inst
            if inst.rd != 0:
                # Store loads write mem_data; ALU instructions write alu_result
                val_to_write = self.mem_wb.mem_data if inst.opcode == 0x03 else self.mem_wb.alu_result
                self.rf.write(inst.rd, val_to_write)

        # Stage 4: Memory Access (MEM)
        self.mem_wb = PipelineState()
        if self.ex_mem.valid and self.ex_mem.inst:
            inst = self.ex_mem.inst
            self.mem_wb.inst = inst
            self.mem_wb.alu_result = self.ex_mem.alu_result
            self.mem_wb.valid = True

            # Load instruction (LW)
            if inst.opcode == 0x03:
                self.mem_wb.mem_data = self.mem.read_word(self.ex_mem.alu_result)
            # Store instruction (SW)
            elif inst.opcode == 0x23:
                self.mem.write_word(self.ex_mem.alu_result, self.ex_mem.rs2_val)

        # Stage 3: Execute (EX)
        self.ex_mem = PipelineState()
        if self.id_ex.valid and self.id_ex.inst:
            inst = self.id_ex.inst
            self.ex_mem.inst = inst
            self.ex_mem.rs2_val = self.id_ex.rs2_val
            self.ex_mem.valid = True

            # OP-IMM (e.g., ADDI)
            if inst.opcode == 0x13:
                if inst.funct3 == 0x0:  # ADDI
                    self.ex_mem.alu_result = (self.id_ex.rs1_val + inst.imm) & 0xFFFFFFFF
            # OP (e.g., ADD, SUB)
            elif inst.opcode == 0x33:
                if inst.funct3 == 0x0 and inst.funct7 == 0x00:  # ADD
                    self.ex_mem.alu_result = (self.id_ex.rs1_val + self.id_ex.rs2_val) & 0xFFFFFFFF
                elif inst.funct3 == 0x0 and inst.funct7 == 0x20:  # SUB
                    self.ex_mem.alu_result = (self.id_ex.rs1_val - self.id_ex.rs2_val) & 0xFFFFFFFF

        # Stage 2: Instruction Decode (ID)
        self.id_ex = PipelineState()
        if self.if_id.valid and self.if_id.inst:
            inst = self.if_id.inst
            self.id_ex.inst = inst
            self.id_ex.pc = self.if_id.pc
            self.id_ex.rs1_val = self.rf.read(inst.rs1)
            self.id_ex.rs2_val = self.rf.read(inst.rs2)
            self.id_ex.valid = True

        # Stage 1: Instruction Fetch (IF)
        self.if_id = PipelineState()
        raw_inst = self.mem.read_word(self.pc)
        if raw_inst != 0:  # Fetch until NOP/0x00000000
            self.if_id.inst = Instruction(raw_inst)
            self.if_id.pc = self.pc
            self.if_id.valid = True
            self.pc += 4