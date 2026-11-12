from instruction_set import INSTRUCTIONS, REGISTERS, OPCODE_TO_INSTR
from vm_operator import Operator
from machine_state import state

class ControlUnit:
  def __init__(self):
    self.operator = Operator()
    self.curr_instruction = None
    self.opcode = 0
    self.operands = []

  def sep_fields(self, code):
    fields = []

    for f in range(4):
      begin = f * 4
      end = f * 4 + 4
      fields.append(code[begin: end])
  
    return fields

  def check_opcode(self, opcode):
    opcode = bin(int(opcode, 2))
    return OPCODE_TO_INSTR[opcode]

  def pack_operands(self, fields):
    return [fields[o] for o in range(1, 4)]
  
  def decode(self):
    instruction = state["ir"]
    fields = self.sep_fields(instruction)
    self.opcode = fields[0]
    self.operands = self.pack_operands(fields)

  def execute(self):
    state["pc"] = self.operator.execute_and_advance(self.opcode, self.operands)
  
  def fetch(self):
    state["ir"] = state["m"][state["pc"]]



