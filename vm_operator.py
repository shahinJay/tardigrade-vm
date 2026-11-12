#vm_operator.py
from machine_state import state
from instruction_set import INSTRUCTIONS
from machine_state import state

class Operator:
  def __init__(self):
    pass

  def eval_reg(self, reg): # not perfect for now
    if 0 <= reg <= 2:
      return True
    else:
      raise ValueError(f"Invalid register: {reg}")

  def eval_addr(self, addr):
    if 0 <= addr < len(state["m"]):
      return True
    else:
      raise ValueError(f"Invalid memory address: {addr}")

  def add(self, reg1, reg2, dest):
    self.eval_reg(reg1)
    self.eval_reg(reg2)
    self.eval_reg(dest)

    state["r"][dest] = state["r"][reg1] + state["r"][reg2]
    return 1

  def sub(self, reg1, reg2, dest):
    self.eval_reg(reg1)
    self.eval_reg(reg2)
    self.eval_reg(dest)

    state["r"][dest] = state["r"][reg1] - state["r"][reg2]
    return 1

  def mul(self, reg1, reg2, dest):
    self.eval_reg(reg1)
    self.eval_reg(reg2)
    self.eval_reg(dest)

    state["r"][dest] = state["r"][reg1] * state["r"][reg2]
    return 1

  def load(self, reg, val):
    print("LOADING: ", reg,"<--", val)
    self.eval_reg(reg)
    state["r"][reg] = val
    return 1

  def read(self, reg, addr):
    self.eval_reg(reg)
    self.eval_addr(addr)
    state["r"][reg] = state["m"][addr]
    return 1

  def move(self, reg1, reg2):
    print("MOVING: ", reg1,"-->", reg2)
    self.eval_reg(reg1)
    self.eval_reg(reg2)
    state["r"][reg1] = state["r"][reg2]
    return 1

  def jz(self, reg, addr): #jump-if-zero : conditional
    self.eval_reg(reg)
    self.eval_addr(addr)
    return addr if state["r"][reg] == 0 else (state["pc"] + 1)

  def jnz(self, reg, addr): #jump-if-not-zero : conditional
    self.eval_reg(reg)
    self.eval_addr(addr)
    return addr if not state["r"][reg] == 0 else (state["pc"] + 1)

  def store(self, reg, addr):
    print("STORING: ", reg,"-->", addr)
    self.eval_reg(reg)
    self.eval_addr(addr)
    state["m"][addr] = state["r"][reg]
    return 1

  def halt(self):
    state["running"] = False
    return 0
  
  def execute_and_advance(self, opcode, operands): #interprets and executes, returns next pc address
    operands = [int(op, 2) for op in operands]

    match int(opcode, 2):
      case 1:
        return (state["pc"] + self.load(operands[0]-1, operands[1]))
      case 2:
        return (state["pc"] + self.read(operands[0]-1, operands[1]))
      case 3:
        return (state["pc"] + self.move(operands[0]-1, operands[1]-1))
      case 4:
        return (state["pc"] + self.store(operands[0]-1, operands[1]))
      case 5:
        return (state["pc"] + self.add(operands[0]-1, operands[1]-1, operands[2]-1))
      case 6:
        return (state["pc"] + self.sub(operands[0]-1, operands[1]-1, operands[2]-1))
      case 7:
        return (state["pc"] + self.mul(operands[0]-1, operands[1]-1, operands[2]-1))
      case 8:
        return operands[0]
      case 9:
        return self.jz(operands[0]-1, operands[1])
      case 10:
        return self.jnz(operands[0]-1, operands[1])
      case 15:
        return (state["pc"] + self.halt())
      case _:
        print("UNKNOWN INSTRUCTION")
        state["running"] = False
        return 0
      