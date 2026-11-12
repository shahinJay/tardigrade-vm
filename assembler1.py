#assembler.py
from instruction_set import INSTRUCTIONS, REGISTERS, op_bit_len

class Assembler:
  def __init__(self, program_file):
    self.program_file = program_file

  def printf_bin(self,label, item, size):
    print(label, format(item, size))
    
  def split_instruction(self, line):
    return tuple(line.split())
  
  def read_program_lines(self):
    with open(self.program_file, "r", encoding="utf-8") as file:
      return [line.strip() for line in file if line.strip()]

  def assemble(self):
    program = []
    lines = self.read_program_lines()

    for line in lines:
      nibbles = list(self.split_instruction(line))
      instr_ref = INSTRUCTIONS[nibbles[0]]
      opcode = instr_ref["opcode"]

      if len(nibbles) < len(instr_ref["operands"]) + 1:
        raise ValueError("LENGTH ERROR")

      instruction = opcode
      hbyt_shift = 1

      for opi in range(1, len(nibbles)):
        operand_type = instr_ref["operands"][opi - 1]
        if operand_type == "register":
          addend = REGISTERS[nibbles[opi]]
          instruction = (instruction<<4) | addend
          hbyt_shift += 1
        elif operand_type == "address":
          addend = int(nibbles[opi])
          instruction = (instruction<<4) | addend
          hbyt_shift += 1
        elif operand_type == "value":
          addend = int(nibbles[opi])
          instruction = (instruction<<4) | addend
          hbyt_shift += 1

      if hbyt_shift < 4:
        instruction = (instruction<<(16-(hbyt_shift*4)))

      instruction = format(instruction, "016b")
      program.append(instruction)
    
    return program
