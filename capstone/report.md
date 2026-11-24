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
