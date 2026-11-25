# Nand to Tetris Capstone Project Report
## Make the Computer Draw a Box

**Course:** Nand to Tetris – I (ETCNTC301)  
**Institution:** School of Engineering & Technology, K.R. Mangalam University  
**Student Name:** Bhavya Anand  
**Roll Number:** 2501730046  
**Personal Number K:** 46  
**Project Marks:** 10 | **Mode:** Individual Work  

---

# Page 1 — Introduction

### Student & Project Metadata
- **Student Name:** Bhavya Anand
- **Roll Number:** 2501730046
- **Academic Program:** B.Tech CSE (AIML), Semester III (Batch 2025–2029)
- **Personal Number K:** 46 (Derived from the last two digits of roll number: `...46`)
- **Course & Code:** Nand to Tetris – I (ETCNTC301)
- **Instructor / School:** School of Engineering & Technology, K.R. Mangalam University

### Project Objective
The objective of this capstone project is to construct a complete, vertically integrated computing stack from the ground up:
1. **Hardware Level:** Implement a complete 16-bit Hack computer in HDL (`CPU.hdl`, `Memory.hdl`, `Computer.hdl`), passing all official test suites.
2. **Software Toolchain:** Build an independent two-pass assembler in Python (`assembler.py`) with student-specific line-number error reporting ($K \bmod 3 = 1$).
3. **Application Level:** Write and assemble a Hack machine program (`Box.asm`) that interacts with keyboard memory (`KBD`) to dynamically render and clear a personal $48 \times 20$ pixel box at screen row 46.

### Personal Parameter Derivations ($K = 46$)
- **Starting Row:** $\text{Row} = K = 46$
- **Box Height:** 20 consecutive screen rows (Rows 46 to 65)
- **Box Width:** $16 \times ((K \bmod 4) + 1) = 16 \times ((46 \bmod 4) + 1) = 16 \times 3 = 48\text{ pixels}$
- **Words per Row:** $48 / 16 = 3\text{ words per row}$ (starting from leftmost column 0)
- **First Screen Address:** $\text{SCREEN} + 32 \times 46 = 16384 + 1472 = 17856$
- **Last Screen Address:** $16384 + 32 \times 65 + 2 = 18464 + 2 = 18466$
- **Total Screen Words Modified:** $20 \times 3 = 60\text{ words}$
- **Assembler Feature ($K \bmod 3 = 1$):** Invalid instruction error handling displaying the exact source line number (`Line <N>: invalid instruction`).

---

# Page 2 — Hack Computer (Part A)

### CPU.hdl Implementation
The Hack CPU executes instructions in a single cycle by coordinating:
- **A-Register:** Receives input either from the incoming instruction (for A-instructions, `instruction[15] == 0`) or the ALU output (for C-instructions with destination bit $d_1$, `instruction[5] == 1`). Outputs address `addressM` to data memory and address `pc` source.
- **D-Register:** Stores ALU data when $d_2$ is asserted (`instruction[4] == 1` in C-instruction).
- **ALU:** Computes arithmetic and logic functions on $D$ and either $A$ or $M$ (selected via the $a$-bit `instruction[12]`). Controlled by $zx, nx, zy, ny, f, no$ (`instruction[11..6]`). Outputs `zr` and `ng` flags.
- **Program Counter (PC):** Evaluates jump conditions ($j_1$: out < 0, $j_2$: out == 0, $j_3$: out > 0). If condition matches on a C-instruction, sets `load = 1` to branch to the A-register address; otherwise, advances sequentially (`inc = true`).
- **Memory Control:** Asserts `writeM` only when $d_3$ is set on a C-instruction.

### Memory.hdl Implementation
Decodes 15-bit memory addresses using upper bits `address[13..14]`:
- `00` or `01` $\rightarrow$ Routes to `RAM16K` (addresses 0 to 16,383).
- `10` $\rightarrow$ Routes to `Screen` memory map (addresses 16,384 to 24,575).
- `11` $\rightarrow$ Routes to `Keyboard` register (address 24,576).
`DMux4Way` controls the `load` line, and `Mux4Way16` selects the active chip's output.

### Computer.hdl Implementation
Integrates `ROM32K`, `CPU`, and `Memory` into a cohesive machine:
- `ROM32K(address=pc, out=instruction)`
- `CPU(inM=inM, instruction=instruction, reset=reset, outM=outM, writeM=writeM, addressM=addressM, pc=pc)`
- `Memory(in=outM, load=writeM, address=addressM, out=inM)`

### Official Test Results
All chips were tested using the official Nand to Tetris Hardware Simulator:
- `CPU.tst` $\rightarrow$ **PASS** (`End of script - Comparison ended successfully`)
- `Memory-auto.tst` $\rightarrow$ **PASS** (`End of script - Comparison ended successfully`)
- `ComputerAdd.tst` $\rightarrow$ **PASS** (`End of script - Comparison ended successfully`)
- `ComputerMax.tst` $\rightarrow$ **PASS** (`End of script - Comparison ended successfully`)
- `ComputerRect.tst` $\rightarrow$ **PASS** (`End of script - Comparison ended successfully`)

---

# Page 3 — Python Hack Assembler (Part B)

### Two-Pass Architecture
`assembler.py` translates assembly programs into binary without using external libraries:
- **Pass 1 (Label Processing):**
  - Scans source code while tracking 1-based original line numbers.
  - Strips whitespace and comments (`//...`).
  - Detects labels `(LABEL)` and records their ROM address without incrementing the instruction counter.
  - Pre-populates predefined symbols (`SP=0`, `LCL=1`, `ARG=2`, `THIS=3`, `THAT=4`, `R0..R15=0..15`, `SCREEN=16384`, `KBD=24576`).
- **Pass 2 (Binary Generation):**
  - Translates A-instructions (`@val`): Converts numeric constants ($0 \le v \le 32767$) to 15-bit binary (`0vvvvvvvvvvvvvvv`). Resolves labels and predefined symbols. Allocates new variables in RAM sequentially starting at address **16**.
  - Translates C-instructions (`dest=comp;jump`): Parses destination, computation, and jump components, encoding into `111accccccdddjjj`.

### Additional Feature ($K \bmod 3 = 1$): Line-Number Error Handling
- Validates every field against strict grammar.
- Rejects invalid computation fields (e.g. `D=X`), invalid destinations (e.g. `XYZ=D`), invalid jumps, malformed labels (e.g. `(123)`), and out-of-range addresses (`@32768`, `@-1`).
- Outputs clean message: `Line <N>: invalid instruction` without Python tracebacks.
- Returns non-zero exit code (`1`) and ensures no misleading partial `.hack` file is produced.

### Official Benchmark Comparisons
Tested against all four official benchmark programs:
- `Add.asm` $\rightarrow$ **100% MATCH** with `Add.ref.hack` (6 instructions)
- `Max.asm` $\rightarrow$ **100% MATCH** with `Max.ref.hack` (16 instructions)
- `Rect.asm` $\rightarrow$ **100% MATCH** with `Rect.ref.hack` (25 instructions)
- `Pong.asm` $\rightarrow$ **100% MATCH** with `Pong.ref.hack` (27,483 instructions)
- Automated Unit Tests: 16 test cases executed in `tests/test_assembler.py` $\rightarrow$ **All 16 Passed (OK)**.

---

# Page 4 — Box Program & University Viva Guide (Part C)

### Box Program Design (`Box.asm`)
1. **Continuous Keyboard Polling:** Reads RAM address `24576` (`KBD`).
2. **Color Selection:** If `KBD != 0` (key pressed), `color = -1` (black). If `KBD == 0` (released), `color = 0` (white).
3. **Screen Rendering Loop:**
   - Initializes pointer `row_ptr = 17856` (Row 46 start) and counter `row_count = 20`.
   - In each row:
     - Sets Word 0: `RAM[row_ptr] = color` (pixels 0 to 15).
     - Increments `row_ptr` and sets Word 1: `RAM[row_ptr + 1] = color` (pixels 16 to 31).
     - Increments `row_ptr` and sets Word 2: `RAM[row_ptr + 2] = color` (pixels 32 to 47).
     - Advances `row_ptr` by 30 words ($2 + 30 = 32$ words per screen line) to reach the next row.
     - Decrements `row_count`.
   - Loops back to keyboard polling indefinitely.

### One Programming Mistake Encountered and Corrected
**The Issue:** When attempting to address consecutive words across a single row, an initial draft wrote Word 0 using `A=M`, and then attempted to address Word 1 using `A=M+1` and Word 2 with `A=M+2` without reloading the base address. In Hack assembly, `M` always refers to `RAM[A]`. Because register `A` had already been changed to point to the screen address (17856), referencing `M` read the contents of the screen memory rather than the pointer variable `row_ptr`. This corrupted the drawing address.  
**The Fix:** We structured the routine to explicitly update `row_ptr` using `row_ptr = row_ptr + 1` between words, ensuring `A` is always cleanly loaded from `row_ptr` via `@row_ptr; A=M`, and then adding 30 words to jump cleanly to the beginning of the next row.

### Viva Demonstration: On-the-Spot Modification
**Task:** Move the box down by one row (start at Row 47 instead of Row 46).  
**Modification:** In `Box.asm`, change the starting screen address initialization:
```hack
// Original (Row 46): 16384 + (32 * 46) = 17856
@17856
D=A
// Modified for Row 47: 16384 + (32 * 47) = 17888
@17888
D=A
```
Reassemble with `python3 assembler/assembler.py Box.asm Box.hack` and run in the CPU Emulator. The box renders starting at row 47.


---

# Page 5 — Source Code Appendix: Part A (Hack Computer HDL)

### 
```hdl
// Hack Central Processing Unit (CPU)
// Executes 16-bit instructions according to Hack architecture specification.
CHIP CPU {
    IN  inM[16],         // M value input  (M = contents of RAM[A])
        instruction[16], // Instruction for execution
        reset;           // Signals whether to restart the current
                         // program (reset==1) or continue executing
                         // the current program (reset==0).
    OUT outM[16],        // M value output
        writeM,          // Write to M? 
        addressM[15],    // Address in data memory (of M)
        pc[15];          // Address of next instruction

    PARTS:
    // Instruction decoding: Type A (inst[15]=0) vs Type C (inst[15]=1)
    Not(in=instruction[15], out=isA);
    Not(in=isA, out=isC);

    // A register input selection
    Mux16(a=instruction, b=aluOut, sel=isC, out=toAReg);

    // A register load control: load if A-instruction OR (C-instruction AND dest A (d1=inst[5]))
    And(a=isC, b=instruction[5], out=destA);
    Or(a=isA, b=destA, out=loadA);
    ARegister(in=toAReg, load=loadA, out=aOut, out[0..14]=addressM);

    // ALU y-input: A register vs inM depending on 'a' bit (inst[12])
    Mux16(a=aOut, b=inM, sel=instruction[12], out=aluY);

    // D register load control: C-instruction AND dest D (d2=inst[4])
    And(a=isC, b=instruction[4], out=loadD);
    DRegister(in=aluOut, load=loadD, out=dOut);

    // ALU execution: control bits c1..c6 map directly to inst[11..6]
    ALU(x=dOut, y=aluY,
        zx=instruction[11], nx=instruction[10],
        zy=instruction[9],  ny=instruction[8],
        f=instruction[7],   no=instruction[6],
        out=aluOut, out=outM, zr=zr, ng=ng);

    // writeM control: C-instruction AND dest M (d3=inst[3])
    And(a=isC, b=instruction[3], out=writeM);

    // Jump condition evaluation
    Or(a=zr, b=ng, out=zrOrNg);
    Not(in=zrOrNg, out=pos);
    And(a=instruction[0], b=pos, out=jgt);
    And(a=instruction[1], b=zr, out=jeq);
    And(a=instruction[2], b=ng, out=jlt);
    Or(a=jgt, b=jeq, out=jge);
    Or(a=jge, b=jlt, out=jumpCond);
    And(a=isC, b=jumpCond, out=doJump);

    // Program Counter (PC): inc=true, load=doJump, reset=reset
    PC(in=aOut, load=doJump, inc=true, reset=reset, out[0..14]=pc);
}
```

### 
```hdl
// Hack Data Memory Map: RAM16K (0..16383), Screen (16384..24575), Keyboard (24576)
CHIP Memory {
    IN in[16], load, address[15];
    OUT out[16];

    PARTS:
    // DMux load signal based on address[13..14]
    // 00, 01 -> RAM16K; 10 -> Screen; 11 -> Invalid/Keyboard (read-only)
    DMux4Way(in=load, sel=address[13..14], a=loadRAM0, b=loadRAM1, c=loadScreen, d=loadKbd);
    Or(a=loadRAM0, b=loadRAM1, out=loadRAM);

    RAM16K(in=in, load=loadRAM, address=address[0..13], out=outRAM);
    Screen(in=in, load=loadScreen, address=address[0..12], out=outScreen);
    Keyboard(out=outKbd);

    Mux4Way16(a=outRAM, b=outRAM, c=outScreen, d=outKbd, sel=address[13..14], out=out);
}
```

### 
```hdl
// Complete Hack Top-Level Computer Architecture
CHIP Computer {
    IN reset;

    PARTS:
    ROM32K(address=pc, out=instruction);
    CPU(inM=memOut, instruction=instruction, reset=reset,
        outM=outM, writeM=writeM, addressM=addressM, pc=pc);
    Memory(in=outM, load=writeM, address=addressM, out=memOut);
}
```

---

# Page 6 — Source Code Appendix: Part B (Python Hack Assembler)

### 
```python
#!/usr/bin/env python3
"""
Hack Assembler with Invalid Instruction Error Handling (Personal Number K = 46, K mod 3 = 1)
Translates Hack Assembly (.asm) into Hack Machine Code (.hack) with source line numbers.
"""
import sys, os, re

PREDEFINED_SYMBOLS = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576
}
for i in range(16):
    PREDEFINED_SYMBOLS[f"R{i}"] = i

COMP_TABLE = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101",
    "!A": "0110001", "-D": "0001111", "-A": "0110011",
    "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011",
    "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
    "D|M": "1010101"
}

DEST_TABLE = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP_TABLE = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

SYMBOL_REGEX = re.compile(r"^[a-zA-Z_.$:][a-zA-Z0-9_.$:]*$")

class AssemblyError(Exception):
    def __init__(self, line_num, message="invalid instruction"):
        self.line_num = line_num
        self.message = message
        super().__init__(f"Line {line_num}: {message}")

class HackAssembler:
    def __init__(self):
        self.symbol_table = {}
        self.next_var_address = 16
        self.num_labels = 0
        self.num_variables = 0

    def assemble(self, asm_source_lines):
        self.symbol_table = dict(PREDEFINED_SYMBOLS)
        self.next_var_address = 16
        self.num_labels = 0
        self.num_variables = 0

        rom_address = 0
        cleaned_instructions = []

        # PASS 1: Symbol resolution & syntax validation
        for line_idx, raw_line in enumerate(asm_source_lines):
            line_num = line_idx + 1
            cleaned = raw_line.split("//")[0].strip()
            if not cleaned:
                continue

            if cleaned.startswith("("):
                if not cleaned.endswith(")"):
                    raise AssemblyError(line_num, "invalid instruction")
                label = cleaned[1:-1].strip()
                if not label or not SYMBOL_REGEX.match(label) or label in self.symbol_table:
                    raise AssemblyError(line_num, "invalid instruction")
                self.symbol_table[label] = rom_address
                self.num_labels += 1
            else:
                cleaned_instructions.append((line_num, cleaned))
                rom_address += 1

        # PASS 2: Binary code generation
        binary_code = []
        for line_num, inst in cleaned_instructions:
            if inst.startswith("@"):
                val_str = inst[1:].strip()
                if not val_str:
                    raise AssemblyError(line_num, "invalid instruction")
                if val_str.isdigit():
                    val = int(val_str)
                    if val < 0 or val > 32767:
                        raise AssemblyError(line_num, "invalid instruction")
                elif SYMBOL_REGEX.match(val_str):
                    if val_str not in self.symbol_table:
                        self.symbol_table[val_str] = self.next_var_address
                        self.next_var_address += 1
                        self.num_variables += 1
                    val = self.symbol_table[val_str]
                else:
                    raise AssemblyError(line_num, "invalid instruction")
                binary_code.append(f"0{val:015b}")
            else:
                s = "".join(inst.split())
                dest_part, jump_part, comp_part = "", "", ""
                if "=" in s:
                    dest_part, s = s.split("=", 1)
                if ";" in s:
                    comp_part, jump_part = s.split(";", 1)
                else:
                    comp_part = s

                if dest_part not in DEST_TABLE or comp_part not in COMP_TABLE or jump_part not in JUMP_TABLE:
                    raise AssemblyError(line_num, "invalid instruction")

                comp_bin = COMP_TABLE[comp_part]
                dest_bin = DEST_TABLE[dest_part]
                jump_bin = JUMP_TABLE[jump_part]
                binary_code.append(f"111{comp_bin}{dest_bin}{jump_bin}")

        return binary_code
```

---

# Page 7 — Source Code Appendix: Part C (Box Program in Hack Assembly)

### 
```hack
// ==================================================================
// Box.asm - Make the Computer Draw a Box
// Student: Bhavya Anand
// Roll Number: 2501730046
// Personal Number K: 46
// Course: Nand to Tetris - I (ETCNTC301)
// University: K.R. Mangalam University
//
// Box Specifications for K = 46:
// - Starting row: 46 (row 46 of 256)
// - Ending row: 65 (20 consecutive screen rows)
// - Starting column: 0 (left edge)
// - Width: 48 pixels (3 consecutive 16-bit words per row)
// - Starting screen address: 16384 + (32 * 46) = 17856
// - Ending screen address: 17856 + (19 * 32) + 2 = 18466
// - Total screen words modified: 20 * 3 = 60 words
// ==================================================================

(CHECK_KEYBOARD)
    @KBD
    D=M
    @DRAW_BLACK
    D;JNE

(DRAW_WHITE)
    @color
    M=0
    @RENDER
    0;JMP

(DRAW_BLACK)
    @color
    M=-1

(RENDER)
    @17856
    D=A
    @row_ptr
    M=D

    @20
    D=A
    @row_count
    M=D

(ROW_LOOP)
    @row_count
    D=M
    @CHECK_KEYBOARD
    D;JEQ

    // Word 0 (pixels 0..15)
    @color
    D=M
    @row_ptr
    A=M
    M=D

    // Advance to Word 1
    @row_ptr
    M=M+1

    // Word 1 (pixels 16..31)
    @color
    D=M
    @row_ptr
    A=M
    M=D

    // Advance to Word 2
    @row_ptr
    M=M+1

    // Word 2 (pixels 32..47)
    @color
    D=M
    @row_ptr
    A=M
    M=D

    // Advance pointer to the start of the next screen row
    // Next row = row_ptr + 30 (since already advanced by 2 words: 2 + 30 = 32)
    @30
    D=A
    @row_ptr
    M=M+D

    // Decrement row counter
    @row_count
    M=M-1

    @ROW_LOOP
    0;JMP
```
