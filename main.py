import time
from assembler1 import Assembler
from control_unit import ControlUnit
from machine_state import state

time_scale = 0.1

def load_program_to_memory(program):
  state["m"].extend(program)

program_path = "./programs/test.tasm"
assembler = Assembler(program_path)
cu = ControlUnit()

def init_vm():
  program = assembler.assemble()
  load_program_to_memory(program)
  state["pc"] = 0 #hardcoding where the instructions start, for now
  cu.fetch()
  print("\nOP: ", cu.opcode, cu.operands)
  print("REG: ", state['r'])

def run_vm():
  state["running"] = True
  while state["running"]:
    print("\n\n-------------")
    cu.fetch()

    print(state["ir"])

    cu.decode()
    
    if not state["running"]:
      print("HALTING...")
      break

    cu.execute()
    print("\nOP: ", cu.opcode, cu.operands)
    print("REG: ", state['r'])
    print("PC: ", state["pc"])

    time.sleep(time_scale)

  print("MEMORY: ", state['m'])

init_vm()
run_vm()
