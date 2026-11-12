# Tiny VM Instruction Set

This document describes the current instruction set implemented by the VM.

## Instruction format

Every instruction is 16 bits, represented as four 4-bit nibbles:

```text
[ opcode ][ operand 1 ][ operand 2 ][ operand 3 ]
  4 bits     4 bits      4 bits      4 bits
```

The opcode is always the leftmost nibble. Operands follow in the order shown
in the instruction syntax. Unused operand nibbles are zero-filled on the
right. For example, `LOAD R1 3` is encoded as:

```text
0001 0001 0011 0000
```

Each encoded operand occupies one nibble, so values and addresses must be in
the range 0-15. Register operands use the register codes below. Register names
are one-based (`R1` through `R3`); the VM maps them to its internal
zero-based register array.

## Registers

| Register | Encoded value |
|---|---|
| `R1` | `0001` |
| `R2` | `0010` |
| `R3` | `0011` |

## Instructions

In the descriptions below, `A`, `B`, and `D` are register operands; `N` is an
immediate value; and `addr` is a memory or instruction address.

| Mnemonic | Opcode | Syntax | Behavior |
|---|---|---|---|
| `LOAD` | `0001` | `LOAD D N` | Set register `D` to immediate value `N`. |
| `READ` | `0010` | `READ D addr` | Load the value at memory address `addr` into `D`. |
| `MOVE` | `0011` | `MOVE D A` | Copy the value in `A` into `D`. |
| `STORE` | `0100` | `STORE A addr` | Write the value in `A` to memory address `addr`. |
| `ADD` | `0101` | `ADD A B D` | Set `D` to `A + B`. |
| `SUB` | `0110` | `SUB A B D` | Set `D` to `A - B`. |
| `MUL` | `0111` | `MUL A B D` | Set `D` to `A * B`. |
| `JUMP` | `1000` | `JUMP addr` | Set the program counter to `addr`. |
| `JZ` | `1001` | `JZ A addr` | Jump to `addr` if `A` is zero; otherwise continue to the next instruction. |
| `JNZ` | `1010` | `JNZ A addr` | Jump to `addr` if `A` is not zero; otherwise continue to the next instruction. |
| `HALT` | `1111` | `HALT` | Stop VM execution. |

Arithmetic results use Python integers in the current implementation; they are
not restricted to 4 bits. The 4-bit limit applies to values encoded directly
in an instruction.

## Program counter and memory

The program counter (PC) indexes instructions in memory. Normal instructions
advance it by one. `JUMP` sets it to the given absolute address, and `JZ` and
`JNZ` do so only when their condition is met.

The current VM stores instructions and data in the same memory list. As a
result, `STORE` can overwrite an instruction if its address points to one.
Addresses must refer to an existing memory entry.

## Reserved opcodes

Opcode `0000` and opcodes `1011` through `1110` have no assigned instruction.
They are not padding or skip instructions; the current VM treats them as
unknown instructions and stops execution.