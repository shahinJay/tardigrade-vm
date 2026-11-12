#isa.py
fixed_length = 16

INSTRUCTIONS = {
  "LOAD": {
    "opcode": 0b0001,
    "format": "010b",
    "length": 10,
    "operands": ("register", "value")
  },
  
  "READ": {
    "opcode": 0b0010,
    "format": "010b",
    "length": 10,
    "operands": ("register", "address")
  },
  "MOVE": {
    "opcode": 0b0011,
    "format": "08b",
    "length": 8,
    "operands": ("register", "register")
  },
  "STORE": {
    "opcode": 0b0100,
    "format": "010b",
    "length": 10,
    "operands": ("register", "address")
  },
  
  "ADD": { #5
    "opcode": 0b0101,
    "format": "010b",
    "length": 10,
    "operands": ("register", "register", "register")
  },
  "SUB": { #6
    "opcode": 0b0110,
    "format": "010b",
    "length": 10,
    "operands": ("register", "register", "register")
  },
  "MUL": { #7
    "opcode": 0b0111,
    "format": "010b",
    "length": 10,
    "operands": ("register", "register", "register")
  },

  "JUMP": { #8
    "opcode": 0b1000,
    "format": "08b",
    "length": 8,
    "operands": ("address",)
  },
  "JZ": { #9
    "opcode": 0b1001,
    "format": "010b",
    "length": 10,
    "operands": ("register", "address")
  },
  "JNZ": { #10
    "opcode": 0b1010,
    "format": "010b",
    "length": 10,
    "operands": ("register", "address")
  },

  "HALT": {
    "opcode": 0b1111,
    "format": "04b",
    "length": 4,
    "operands": ()
  }
}

OPCODE_TO_INSTR = {
  bin(spec["opcode"]) : name for name, spec in INSTRUCTIONS.items()
}

REGISTERS = {
  "R1" : 0b0001,
  "R2" : 0b0010,
  "R3" : 0b0011,
}

op_bit_len = {
  "opcode": 4,
  "register": 4,
  "value": 4, 
  "address": 4
}