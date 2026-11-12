# tardigrade-vm

A tiny, zero-dependency 16-bit Von Neumann virtual machine and custom assembly (`.tasm`) toolchain built from first principles in Python.

`tardigrade` models the core hardware execution pipeline—from assembling human-readable instructions into 16-bit nibble-packed words down to a unified instruction/data memory space and fetch-decode-execute loop.

## Features

- **Custom 16-Bit ISA:** 4-bit opcode + three 4-bit operand fields supporting register loads, unified memory read/write, arithmetic (`ADD`, `SUB`, `MUL`), and conditional/unconditional branching (`JUMP`, `JZ`, `JNZ`).
- **From-Scratch Assembler (`assembler1.py`):** Translates `.tasm` source files into 16-bit binary representations using bitwise shifting and nibble packing.
- **Von Neumann Execution Engine:** Unified memory model (`machine_state.py`) where instructions and data share the same address space, driven by a dedicated control unit (`control_unit.py`) and operator (`vm_operator.py`).
- **Zero External Dependencies:** Pure Python standard library implementation designed as a reference prototype ahead of a bare-metal C rewrite and cycle-by-cycle visualizer.

## Project Structure

```text
tardigrade/
├── docs/
│   ├── architecture.md           # Module responsibilities, data flow, and execution cycle
│   └── isa.md                    # 16-bit instruction format, opcodes, and register specs
├── programs/
│   ├── factorial.tasm            # Iterative factorial calculation using conditional branching
│   ├── instruction_coverage.tasm # Test suite exercising all supported opcodes
│   └── test.tasm                 # Scratchpad assembly test program
├── tests/
│   └── test.tasm                 # Unit test assembly file
├── assembler1.py                 # Bit-packing .tasm assembler
├── control_unit.py               # Instruction fetch and nibble decoding
├── instruction_set.py            # Shared opcode, operand, and register definitions
├── machine_state.py              # Shared VM runtime state (registers, memory, PC, IR)
├── vm_operator.py                # Instruction execution and program counter control
└── main.py                       # Entry point to assemble, load, and run programs
```

## Quickstart

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/tardigrade.git
   cd tardigrade
   ```

2. **Run the VM:**
   ```bash
   python main.py
   ```
   *(Configure the target `.tasm` file inside `main.py`, such as `programs/factorial.tasm`.)*

### Example `.tasm` Program

```asm
LOAD R1 5
LOAD R2 1
MUL R1 R2 R2
LOAD R3 1
SUB R1 R3 R1
JNZ R1 2
HALT
```

## Documentation

- **[Architecture & Execution Flow](docs/architecture.md):** Detailed breakdown of the module pipeline, startup sequence, and runtime state.
- **[Instruction Set Architecture (ISA)](docs/isa.md):** Full opcode table, 16-bit nibble layout, register encodings, and memory rules.

## Roadmap

- [ ] Two-pass label resolution in the assembler (`loop:` / `end:`)
- [ ] Pygame cycle-by-cycle visual debugger (live memory, register, and instruction-fetch highlighting with adjustable timescale)
- [ ] Full port to zero-dependency C backed by a contiguous memory arena