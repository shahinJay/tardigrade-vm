# VM Architecture and Execution Flow

This document describes how the current VM is divided into modules and how an
assembly program moves through them. For instruction encodings and behavior,
see [isa.md](./isa.md).

## Components

| Module | Responsibility |
|---|---|
| `main.py` | Chooses the assembly source, creates the assembler and control unit, loads assembled instructions into memory, and runs the fetch/decode/execute loop. |
| `assembler1.py` | Reads the assembly file, splits each source line into a mnemonic and operands, and encodes each instruction as a 16-character binary string. |
| `isa.py` | Defines the instruction mnemonics, opcodes, operand kinds, register encodings, and opcode-to-name lookup. This is the shared instruction-set reference for the assembler and VM. |
| `control_unit.py` | Fetches the instruction at the program counter, splits its binary string into four nibbles, identifies the opcode and operand fields, and passes them to the operator. |
| `vm_operator.py` | Implements instruction effects: arithmetic, register and memory operations, branches, and halting. It also advances or sets the program counter. |
| `state.py` | Holds the VM's shared runtime state: registers (`r`), memory (`m`), instruction register (`ir`), program counter (`pc`), and running flag. |

## Data flow

```text
assembly source (.tasm)
        |
        v
   assembler1.py <---- instruction definitions ---- isa.py
        |
        | list of 16-character binary instructions
        v
 main.py loads program into state["m"]
        |
        v
 control_unit.py fetches at state["pc"]
        |
        | instruction string -> opcode + three 4-bit fields
        v
 vm_operator.py executes instruction
        |
        | reads/writes registers and memory; updates PC/running
        +--------------------> state.py
                                  |
                                  +---- next fetch uses updated PC
```

## Startup and execution cycle

1. `main.py` asks `Assembler` to read and assemble the selected `.tasm` file.
2. The resulting instruction strings are appended to `state["m"]`; the PC is
   initialized to zero.
3. While `state["running"]` is true:
   - The control unit fetches `state["m"][state["pc"]]` into `state["ir"]`.
   - It splits the 16-bit string into four 4-bit fields. The first field is
     the opcode; the other three are passed as operands.
   - The operator converts operand fields from binary strings to integers,
     dispatches based on the opcode, and performs the instruction's effect.
   - Ordinary operations advance the PC by one. Branch instructions may set it
     to their target. `HALT` clears the running flag.
4. `main.py` exits the loop when the VM is no longer running.

## Runtime state

- **Registers:** `state["r"]` is a list of three values. Assembly register
  names `R1`, `R2`, and `R3` encode as 1, 2, and 3; execution maps them to list
  indices 0, 1, and 2.
- **Memory:** `state["m"]` stores the assembled instruction strings and is also
  used by `READ` and `STORE` as data memory. Consequently, a store can replace
  an instruction if it targets that instruction's address.
- **Instruction register:** `state["ir"]` holds the fetched instruction.
- **Program counter:** `state["pc"]` is an index into memory. `JUMP`, `JZ`,
  and `JNZ` use absolute memory addresses.
- **Running flag:** `state["running"]` controls the main execution loop and
  is cleared by `HALT`.

## Current implementation notes

- Instructions are represented as 16-character strings rather than integer
  words.
- Each instruction has four 4-bit nibbles: opcode followed by up to three
  operand fields. Unused operand fields are zero-filled on the right.
- Direct values, register codes, and addresses are encoded in 4-bit fields.
- The assembler currently checks for too few operands but does not yet reject
  extra operands or validate every encoded value's range.
- VM state is module-level shared data. A fresh run should reset it before
  loading a program if execution is repeated in the same process.
- The modules currently print diagnostic output directly during execution.
