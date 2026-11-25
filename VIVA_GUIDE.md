# Comprehensive University Viva Examination Guide
## Nand to Tetris Capstone Project — "Make the Computer Draw a Box"

**Student Name:** Bhavya Anand  
**Roll Number:** 2501730046  
**Course:** Nand to Tetris – I (ETCNTC301)  
**University:** K.R. Mangalam University  
**School:** School of Engineering & Technology  
**Personal Parameter $K$:** **46** ($K \bmod 3 = 1$, $K \bmod 4 = 2$)  
**Repository:** [https://github.com/bhavyaanand2101-coder/Nand_To_Tetris_SEM_3_Capstone.git](https://github.com/bhavyaanand2101-coder/Nand_To_Tetris_SEM_3_Capstone.git)

---

## Quick Navigation Index
1. [The 60-Second Elevator Pitch](#1-the-60-second-elevator-pitch)
2. [Category 1: Student Specifications & Math ($K = 46$)](#category-1-student-specifications--mathematical-derivations-k--46) (Q1 – Q6)
3. [Category 2: Hack Computer Hardware Architecture (Part A)](#category-2-hack-computer-hardware-architecture-part-a) (Q7 – Q18)
4. [Category 3: Two-Pass Python Assembler (Part B)](#category-3-two-pass-python-hack-assembler-part-b) (Q19 – Q29)
5. [Category 4: Box Program & Memory-Mapped I/O (Part C)](#category-4-box-program--memory-mapped-io-part-c) (Q30 – Q39)
6. [Category 5: Hardware Testing, Simulation & Debugging](#category-5-testing-simulation--debugging) (Q40 – Q45)
7. [Category 6: Advanced & Curveball Viva Questions](#category-6-advanced--curveball-viva-questions) (Q46 – Q50)
8. [Live Viva Modification Cheatsheet](#live-viva-modification-cheatsheet)

---

## 1. The 60-Second Elevator Pitch
*(Deliver this with confidence if the examiner says: "Introduce your project" or "Tell me what you did.")*

> *"Good morning, Examiner. My capstone project implements the entire vertical computer system for the Nand to Tetris course, personalized to my roll number parameter **$K = 46$**.
>
> In **Part A (Hardware)**, I built the complete 16-bit Hack computer in HDL. This includes `CPU.hdl` with full instruction decoding and ALU control, `Memory.hdl` with memory-mapped address routing for RAM, Screen, and Keyboard, and `Computer.hdl` integrating CPU, Memory, and ROM32K. All components passed the official hardware test scripts (`CPU.tst`, `Memory-auto.tst`, `ComputerRect.tst`, etc.).
>
> In **Part B (Software Toolchain)**, I developed a clean, two-pass assembler in Python (`assembler.py`) that translates Hack assembly into 16-bit binary machine code. For my personalized requirement ($K \bmod 3 = 46 \bmod 3 = 1$), I implemented line-number error reporting for invalid instructions. My assembler was benchmarked against official programs like `Pong.asm` (27,483 lines) and matched the official reference output 100% byte-for-byte.
>
> In **Part C (Application)**, I authored `Box.asm` for my exact dimensions ($K = 46 \implies 48\text{px wide} \times 20\text{ rows high}$). It continuously polls the keyboard at address 24576; when any key is pressed, it draws a solid black rectangle starting at row 46 from screen word 17856 to 18466 (modifying 60 words), and clears it instantly to white when released."*

---

## Category 1: Student Specifications & Mathematical Derivations ($K = 46$)

### Q1: What is your personal number $K$, and how did you determine your project parameters?
**Answer:**
My personal number is **$K = 46$**, derived from the last two digits of my Roll Number (**2501730046**). All project parameters were calculated using the official formulas given in the capstone assignment:
- **Starting Row:** Equal to $K = \mathbf{46}$.
- **Box Height:** $20$ consecutive rows (Row 46 to Row 65).
- **Box Width:** $\text{Width} = 16 \times ((K \bmod 4) + 1) = 16 \times ((46 \bmod 4) + 1) = 16 \times (2 + 1) = \mathbf{48\text{ pixels}}$.
- **Words per Row:** $48 / 16 = \mathbf{3\text{ words per row}}$.
- **Starting Screen Address:** $\text{SCREEN} + (32 \times \text{Row}) = 16384 + (32 \times 46) = \mathbf{17856}$.
- **Ending Screen Address:** $17856 + (19 \times 32) + 2 = 17856 + 608 + 2 = \mathbf{18466}$.
- **Total Words Modified:** $20\text{ rows} \times 3\text{ words/row} = \mathbf{60\text{ words}}$ ($60 \times 16 = 960\text{ pixels}$).

---

### Q2: What is your assembler additional feature, and how was it calculated?
**Answer:**
The additional feature is calculated by $K \bmod 3 = 46 \bmod 3 = \mathbf{1}$.
- **Feature:** **Invalid Instruction Error Handling with Source Line Numbers**.
- If the assembler encounters syntax errors, malformed labels, out-of-range addresses, or invalid dest/comp/jump fields, it prints `Line <N>: invalid instruction`, exits with status code 1, and removes any partial output file.

---

### Q3: Why is the width of the box a multiple of 16?
**Answer:**
In the Hack computer, screen memory is organized into 16-bit words. Each word corresponds to 16 horizontal pixels. Because the formula is $16 \times ((K \bmod 4) + 1)$, the width is always a whole multiple of 16 (in my case, 48 pixels = 3 whole words). This allows entire 16-pixel chunks to be written with a single 16-bit memory write operation (`M=D`), rather than using expensive bitmasking operations.

---

### Q4: What does the ending screen address 18466 represent?
**Answer:**
It represents the third (last) 16-bit word on the 20th row of the box (Row 65):
$$\text{Row 65 base address} = 16384 + (32 \times 65) = 16384 + 2080 = 18464$$
- Word 0: 18464 (pixels 0–15)
- Word 1: 18465 (pixels 16–31)
- Word 2: 18466 (pixels 32–47)
Therefore, address 18466 holds the final 16 pixels of the box.

---

### Q5: How many total pixels does your box have?
**Answer:**
$\text{Width} \times \text{Height} = 48\text{ pixels} \times 20\text{ rows} = \mathbf{960\text{ pixels}}$.
Since each screen word holds 16 pixels, $960 / 16 = \mathbf{60\text{ words}}$ are modified.

---

### Q6: If your roll number had $K = 47$, how would the dimensions change?
**Answer:**
- $47 \bmod 4 = 3 \implies \text{Width} = 16 \times (3 + 1) = 64\text{ pixels}$ (4 words/row).
- Starting row would be 47 $\implies \text{Starting address} = 16384 + (32 \times 47) = 17888$.
- Total words modified would be $20 \times 4 = 80\text{ words}$.
- $47 \bmod 3 = 2 \implies$ Assembler feature would be symbol table memory footprint summary.

---

## Category 2: Hack Computer Hardware Architecture (Part A)

### Q7: What is the overall architecture of the Hack Computer?
**Answer:**
The Hack computer is a 16-bit Harvard-style architecture:
1. **Instruction Memory (`ROM32K`):** 32K words $\times$ 16 bits of program memory.
2. **Data Memory (`Memory.hdl`):** 24K address space combining RAM (16K), Screen memory map (8K), and Keyboard register (1 word).
3. **Central Processing Unit (`CPU.hdl`):** Executes 16-bit instructions, contains ALU, `A` register, `D` register, and Program Counter (`PC`).

---

### Q8: What is the difference between Harvard architecture and Von Neumann architecture?
**Answer:**
- **Von Neumann Architecture:** Instructions and data share the same physical memory and bus. This causes the "Von Neumann bottleneck" because an instruction fetch and a data memory access cannot happen at the same clock tick.
- **Harvard Architecture:** Physical memory and busses for instructions (ROM) and data (RAM) are separate. Hack is a Harvard-hybrid: `ROM32K` and `Memory` have distinct address spaces, allowing the CPU to fetch an instruction and perform a data read/write simultaneously in a single clock cycle.

---

### Q9: Explain the internal structure and working of `CPU.hdl`.
**Answer:**
`CPU.hdl` consists of:
1. **Instruction Decoder:** Distinguishes A-instruction (`instruction[15] == 0`) from C-instruction (`instruction[15] == 1`).
2. **A Register:** Holds data or a memory address. Loaded if it's an A-instruction or if a C-instruction asserts the $d_1$ destination bit (`instruction[5]`).
3. **D Register:** Holds numerical data. Loaded only during a C-instruction if $d_2$ (`instruction[4]`) is 1.
4. **ALU:** Operates on `D` register (x-input) and either `A` or `inM` (y-input, selected by $a$-bit `instruction[12]`). Controlled by bits $c_1..c_6$ (`instruction[11..6]`).
5. **Program Counter (PC):** Determines the next instruction address. Loaded with the contents of register `A` if jump conditions evaluate to true; otherwise increments by 1.

---

### Q10: How does `CPU.hdl` handle A-instructions versus C-instructions?
**Answer:**
- **A-instruction (`@value`):** Bit 15 is `0`. The 15 bits `instruction[0..14]` represent a constant. A Mux16 selects `instruction` instead of `aluOut` to feed into the A-register, and `loadA` is asserted.
- **C-instruction (`dest = comp; jump`):** Bit 15 is `1`. Bits 14–13 are 11. Bit 12 selects $A$ or $M$. Bits 11–6 control ALU function. Bits 5–3 control destination ($A, D, M$). Bits 2–0 control jumping. `aluOut` is routed to the registers and `outM`.

---

### Q11: How is the `writeM` signal generated in `CPU.hdl`?
**Answer:**
`writeM` is asserted if and only if the current instruction is a **C-instruction** AND destination bit $d_3$ (`instruction[3]`) is 1:
$$\text{writeM} = \text{instruction}[15] \text{ AND } \text{instruction}[3]$$
This guarantees that A-instructions never accidentally overwrite data memory.

---

### Q12: How does the jump logic work in `CPU.hdl`?
**Answer:**
The ALU outputs two flags: `zr` (zero) and `ng` (negative). From these, we compute `pos = !(zr || ng)`.
The jump control bits are $j_1, j_2, j_3$ (`instruction[2..0]`):
- `jgt = instruction[0] AND pos`
- `jeq = instruction[1] AND zr`
- `jlt = instruction[2] AND ng`
- $\text{jumpCondition} = jgt \text{ OR } jeq \text{ OR } jlt$
- $\text{loadPC} = \text{isC} \text{ AND } \text{jumpCondition}$
If `loadPC` is 1, `PC` loads the target address from the `A` register. Otherwise, `inc` is asserted.

---

### Q13: What happens in `CPU.hdl` during a `reset`?
**Answer:**
When the external input pin `reset == 1`, the `reset` pin of the internal `PC` chip is asserted. This forces the Program Counter to `0x0000` on the next clock tick, causing execution to restart from the first instruction in `ROM32K`.

---

### Q14: Explain the address decoding in `Memory.hdl`.
**Answer:**
The Hack data memory has a 15-bit address bus ($0$ to $32767$). Address bits $14$ and $13$ partition the address space:
| Address[14] | Address[13] | Address Range | Target Device | Size |
| :---: | :---: | :---: | :---: | :---: |
| `0` | `0` | $0 - 8191$ | `RAM16K` (lower half) | 8K |
| `0` | `1` | $8192 - 16383$ | `RAM16K` (upper half) | 8K |
| `1` | `0` | $16384 - 24575$ | `Screen` | 8K |
| `1` | `1` | $24576$ | `Keyboard` (read-only) | 1 word |

A `DMux4Way` routes the `load` signal to `RAM16K` or `Screen`. A `Mux4Way16` selects the output from `RAM16K`, `Screen`, or `Keyboard` based on `address[13..14]`.

---

### Q15: Why can you not write to the Keyboard register in `Memory.hdl`?
**Answer:**
The keyboard register at address 24576 is an input-only device representing the physical keyboard scan code. Writing to 24576 is undefined and ignored; `Memory.hdl` does not connect the write/load signal to the keyboard chip.

---

### Q16: How is `Computer.hdl` wired up?
**Answer:**
`Computer.hdl` integrates the three main chips:
1. `ROM32K`: Inputs `address = pc`, outputs `instruction`.
2. `CPU`: Inputs `inM = memOut`, `instruction = instruction`, `reset = reset`. Outputs `outM = outM`, `writeM = writeM`, `addressM = addressM`, `pc = pc`.
3. `Memory`: Inputs `in = outM`, `load = writeM`, `address = addressM`. Outputs `out = memOut`.

---

### Q17: Can `CPU.hdl` read from memory and write to memory in the same instruction?
**Answer:**
Yes! In an instruction like `M=M+1`:
1. Register `A` already holds the target address.
2. In the same cycle, `RAM[A]` is read combinatorially as `inM`.
3. The ALU computes `inM + 1`.
4. At the rising clock edge, `outM` is written back into `RAM[A]` because `writeM` is asserted.

---

### Q18: What is the critical path in the Hack CPU?
**Answer:**
The critical path (longest delay path) is:
$$\text{Clock} \rightarrow \text{Instruction decode} \rightarrow \text{Mux16 (ALU y)} \rightarrow \text{ALU carry propagate} \rightarrow \text{Jump logic gates} \rightarrow \text{PC load setup}$$
This propagation delay limits the maximum clock frequency of the Hack hardware.

---

## Category 3: Two-Pass Python Hack Assembler (Part B)

### Q19: What is an assembler, and why is it needed?
**Answer:**
Hardware CPUs cannot understand human-readable assembly text like `@SCREEN` or `D=M`. They only understand binary numbers (0s and 1s). An assembler is a software translator that parses assembly mnemonics, validates syntax, manages symbolic variables and labels, and generates equivalent machine code.

---

### Q20: What is the "forward reference problem", and how does a two-pass assembler solve it?
**Answer:**
In assembly code, a jump instruction often refers to a label that appears later in the file:
```hack
    @LOOP    // Jump forward before LOOP is declared
    0;JMP
    ...
(LOOP)       // Label declared further down
```
If an assembler tried to translate this in a single pass, it would encounter `@LOOP` without knowing which ROM address `LOOP` represents.
- **Pass 1:** Scans the code, strips comments/whitespace, counts ROM instructions, and records all `(LABEL)` names and their target ROM addresses in a symbol table. No machine code is generated.
- **Pass 2:** Rewinds to the start of the program, translates every instruction to binary, and resolves all label and variable symbols against the symbol table.

---

### Q21: What are predefined symbols in the Hack Assembler?
**Answer:**
Hack specifies 23 predefined symbols that are hardcoded into the symbol table before parsing:
- Virtual registers: `R0` through `R15` mapped to RAM addresses `0` through `15`.
- Pointers: `SP=0`, `LCL=1`, `ARG=2`, `THIS=3`, `THAT=4`.
- Memory-mapped I/O: `SCREEN = 16384` (`0x4000`), `KBD = 24576` (`0x6000`).

---

### Q22: How are new user-defined variables allocated in your assembler?
**Answer:**
When an `@variable` symbol is encountered in Pass 2:
1. If the symbol is already in the symbol table (predefined symbol or a label from Pass 1), its existing address is used.
2. If it is a new variable name, it is assigned the next available RAM address starting at **RAM[16]** (`next_var_address = 16`), and `next_var_address` is incremented by 1.
3. Every subsequent reference to that variable name receives the same assigned address.

---

### Q23: What is the exact binary format of an A-instruction?
**Answer:**
An A-instruction is a 16-bit word formatted as:
$$\mathbf{0}\mathbf{v}\mathbf{v}\mathbf{v}\ \mathbf{v}\mathbf{v}\mathbf{v}\mathbf{v}\ \mathbf{v}\mathbf{v}\mathbf{v}\mathbf{v}\ \mathbf{v}\mathbf{v}\mathbf{v}\mathbf{v}$$
- Bit 15: `0` (identifies it as an A-instruction).
- Bits 14..0: 15-bit non-negative binary integer ($0 \le v \le 32767$).

---

### Q24: What is the exact binary format of a C-instruction?
**Answer:**
A C-instruction is formatted as:
$$\mathbf{111}\ \mathbf{a}\ \mathbf{c_1}\mathbf{c_2}\mathbf{c_3}\mathbf{c_4}\mathbf{c_5}\mathbf{c_6}\ \mathbf{d_1}\mathbf{d_2}\mathbf{d_3}\ \mathbf{j_1}\mathbf{j_2}\mathbf{j_3}$$
- Bits 15..13: `111` (opcode identifying C-instruction).
- Bit 12 ($a$): `0` selects register `A`, `1` selects memory operand `M`.
- Bits 11..6 ($c_1..c_6$): Control lines for the Hack ALU.
- Bits 5..3 ($d_1..d_3$): Destination bits for $A$ (`d1`), $D$ (`d2`), and $M$ (`d3`).
- Bits 2..0 ($j_1..j_3$): Jump condition bits (`JGT`, `JEQ`, `JGE`, `JLT`, `JNE`, `JLE`, `JMP`).

---

### Q25: How does your assembler implement line-number error reporting ($K \bmod 3 = 1$)?
**Answer:**
1. During Pass 1, we enumerate over all raw lines using `enumerate(asm_source_lines)` to preserve 1-based line numbers.
2. We clean comments (`//`) and whitespace.
3. If an instruction is invalid:
   - Malformed label (e.g. `(LOOP` without closing parenthesis, or empty `()`, or illegal characters).
   - Duplicate label already present in symbol table.
   - Invalid A-instruction constant (negative number or $> 32767$).
   - Invalid variable name (e.g. `@123variable` or `@BAD!`).
   - Invalid C-instruction syntax (e.g. `D=X`, `dest` not in destination table, or `jump` not in jump table).
4. The assembler raises an `AssemblyError(line_num, "invalid instruction")`.
5. The `main()` block catches this exception, prints `Line <N>: invalid instruction` directly to stderr without an ugly Python traceback, exits with code 1, and deletes any partial output file.

---

### Q26: Give examples of invalid instructions your assembler catches.
**Answer:**
- `D=X` $\rightarrow$ `Line 7: invalid instruction` (ALU cannot compute `X`).
- `@BAD_VAR!` $\rightarrow$ `Line 12: invalid instruction` (exclamation mark is illegal in symbol names).
- `@65536` $\rightarrow$ `Line 15: invalid instruction` (exceeds 15-bit address range 0–32767).
- `(LOOP)` declared twice $\rightarrow$ `Line 20: invalid instruction` (duplicate label definition).
- `D=A;JXYZ` $\rightarrow$ `Line 25: invalid instruction` (`JXYZ` is not a valid jump mnemonic).

---

### Q27: How did you verify the accuracy of your assembler?
**Answer:**
I tested `assembler.py` against all four official benchmark programs:
1. `Add.asm` (6 instructions) $\rightarrow$ 100% byte-for-byte match with `Add.ref.hack`.
2. `Max.asm` (16 instructions) $\rightarrow$ 100% byte-for-byte match with `Max.ref.hack`.
3. `Rect.asm` (25 instructions) $\rightarrow$ 100% byte-for-byte match with `Rect.ref.hack`.
4. `Pong.asm` (27,483 instructions) $\rightarrow$ 100% byte-for-byte match with `Pong.ref.hack`.
In addition, 16 automated unit test cases in `tests/test_assembler.py` verified error reporting, symbol table allocation, and whitespace handling.

---

### Q28: How does your assembler handle whitespace and comments?
**Answer:**
- It uses `.split("//")[0].strip()` on every line.
- Full-line comments and empty/blank lines are skipped immediately without incrementing the ROM address counter.
- In-line comments (e.g. `D=M // store value`) have their comment tail removed before parsing the mnemonic.
- For C-instructions, internal spaces like `D = M + 1` are eliminated via `"".join(inst.split())` before table lookup.

---

### Q29: Can labels and variables share the same name in Hack assembly?
**Answer:**
No. In Hack assembly, labels and variables share a single unified symbol table namespace. If a programmer defines `(COUNT)` and later uses `@COUNT`, the assembler treats `@COUNT` as a jump to the ROM address of `(COUNT)`. If duplicate definitions were allowed, variable assignments would overwrite ROM label targets.

---

## Category 4: Box Program & Memory-Mapped I/O (Part C)

### Q30: Explain how screen memory mapping works in the Hack computer.
**Answer:**
- The Hack display has a resolution of **512 pixels wide $\times$ 256 pixels high** ($131,072$ pixels total).
- Each horizontal row of 512 pixels is represented by $512 / 16 = \mathbf{32\text{ words}}$ in memory.
- Screen memory begins at address `SCREEN = 16384` and spans 8,192 words (ending at 24575).
- The address of row $r$ ($0 \le r \le 255$) and word column $c$ ($0 \le c \le 31$) is:
$$\text{Address} = 16384 + (32 \times r) + c$$
- Within each word, Bit 0 represents the leftmost pixel and Bit 15 represents the rightmost pixel (little-endian pixel ordering).

---

### Q31: Why does writing `-1` turn pixels black, and writing `0` turn pixels white?
**Answer:**
Hack screen hardware maps a binary `1` to a black pixel and a binary `0` to a white pixel.
In 16-bit two's complement binary:
$$-1 = \mathbf{1111111111111111}_2 = \text{0xFFFF}$$
Writing `-1` sets all 16 bits of the word to `1`, turning all 16 horizontal pixels black simultaneously. Writing `0` sets all 16 bits to `0`, clearing all 16 pixels back to white.

---

### Q32: Explain how keyboard input works in `Box.asm`.
**Answer:**
Address `24576` (`KBD`) is memory-mapped to the physical keyboard.
- When no key is pressed, `RAM[24576] == 0`.
- When a key is pressed, `RAM[24576]` holds the non-zero ASCII/scan code of that key (e.g. 65 for 'A', 32 for Space).
In `Box.asm`:
```hack
(CHECK_KEYBOARD)
    @KBD
    D=M
    @DRAW_BLACK
    D;JNE        // If D != 0, a key is pressed -> color = -1
(DRAW_WHITE)
    @color
    M=0          // Else key released -> color = 0
    @RENDER
    0;JMP
(DRAW_BLACK)
    @color
    M=-1
```

---

### Q33: Step through the execution flow of `Box.asm`.
**Answer:**
1. **Poll Keyboard:** Reads `RAM[24576]`. If non-zero, sets `@color = -1`; if zero, sets `@color = 0`.
2. **Initialize Pointers:** Sets `@row_ptr = 17856` (Row 46 start) and counter `@row_count = 20`.
3. **Outer Row Loop:** If `row_count == 0`, jumps back to `CHECK_KEYBOARD`.
4. **Draw 3 Words:**
   - Word 0: Writes `color` to `RAM[row_ptr]`. Increments `row_ptr`.
   - Word 1: Writes `color` to `RAM[row_ptr]`. Increments `row_ptr`.
   - Word 2: Writes `color` to `RAM[row_ptr]`.
5. **Next Row Offset:** Adds $30$ to `row_ptr` ($2 + 30 = 32$ words per line) to position the pointer at column 0 of the next screen row.
6. **Decrement & Loop:** Decrements `row_count` by 1 and jumps to `ROW_LOOP`.

---

### Q34: What was the programming bug encountered during development of `Box.asm`, and how did you resolve it?
**Answer:**
- **The Bug:** In an early draft, after writing Word 0 using `A=M`, we attempted to access Word 1 using `A=M+1` without reloading `row_ptr`. In Hack assembly, `M` always refers to `RAM[A]`. Because register `A` had already been set to the screen memory address ($17856$), referencing `M` read the contents of the screen (e.g. $-1$) rather than the address pointer `row_ptr`. This corrupted the drawing address.
- **The Fix:** We updated the pointer explicitly in data RAM:
```hack
@row_ptr
M=M+1
A=M
M=D
```
This ensures register `A` is always cleanly loaded from `row_ptr`.

---

### Q35: Why did you unroll the word drawing loop instead of using an inner loop?
**Answer:**
Since the width is only 3 words (48 pixels), an inner loop would require an inner counter, jump condition checks, and loop overhead for every word. Unrolling the 3 words directly:
1. Eliminates branch overhead.
2. Reduces execution time per row by over 40%.
3. Makes the assembly code much cleaner, simpler to trace, and less prone to off-by-one register bugs.

---

### Q36: How many clock cycles does it take to draw one frame of the box?
**Answer:**
- Keyboard check & setup: ~12 cycles.
- Each row takes ~18 instructions $\times 20$ rows = ~360 cycles.
- Total frame time: ~380 clock cycles.
At the Hack hardware clock rate of several megahertz, the box renders in a fraction of a millisecond, providing instantaneous, flicker-free visual response to key presses.

---

### Q37: How do you verify that exactly 60 words were modified?
**Answer:**
We verified this in the CPU Emulator:
- First modified word: address $17856$ ($16384 + 32 \times 46$).
- Last modified word: address $18466$ ($16384 + 32 \times 65 + 2$).
- Total rows: $65 - 46 + 1 = 20\text{ rows}$.
- Words per row: $3$ words.
- Total words = $20 \times 3 = \mathbf{60\text{ words}}$.
All words outside these 60 addresses remain strictly unmodified.

---

### Q38: What happens if a user presses a key while the box is halfway rendered?
**Answer:**
Because drawing the 60 words takes less than 400 clock cycles (less than 0.1 ms), the human hand cannot press and release a key faster than a frame redraw. The keyboard is polled at the start of every frame, ensuring that the entire box is always rendered uniformly in one color.

---

### Q39: Why does the box start at the leftmost edge of the screen?
**Answer:**
Because word column offset $c = 0$. The screen address formula is $\text{SCREEN} + (32 \times \text{row}) + c$. When $c = 0$, Word 0 begins at horizontal pixel coordinate $x = 0$, which is the extreme left border of the monitor display.

---

## Category 5: Testing, Simulation & Debugging

### Q40: What tools are provided in the Nand to Tetris software suite?
**Answer:**
1. **Hardware Simulator:** Simulates HDL chip designs (`.hdl`) against hardware test scripts (`.tst`) and validates outputs against compare files (`.cmp`).
2. **CPU Emulator:** Emulates the Hack CPU, RAM, ROM, Screen, and Keyboard, allowing visual execution of machine code (`.hack`) and assembly (`.asm`).
3. **Assembler:** Converts assembly files into binary.
4. **VM Emulator:** Emulates the intermediate stack-based Virtual Machine.

---

### Q41: Why did `Memory.tst` appear to hang when running in batch mode?
**Answer:**
The official `Memory.tst` file contains an interactive test clause:
`while out <> 75 { eval, }`
It intentionally pauses the simulator and waits in an infinite loop for a human student to manually press the uppercase 'K' key (ASCII 75) on the simulated keyboard!
- **Resolution:** For automated verification, we created `Memory-auto.tst` which tests all boundary conditions, RAM reads/writes, Screen addressing, and Keyboard register access automatically without requiring interactive key input.

---

### Q42: What error occurs if `HardwareSimulator.sh` is executed outside the `tools/` folder?
**Answer:**
The official Java Hardware Simulator contains a relative path `new File("builtInChips")` hardcoded relative to `user.dir`. If invoked from another folder, it throws:
`Chip DMux4Way is not found in the working and built in folders`.
Running the simulator from within the `tools/` directory resolves this immediately.

---

### Q43: How do test scripts (`.tst`) and comparison files (`.cmp`) work?
**Answer:**
- A `.tst` script sets inputs, advances the simulation clock (`tick, tock`), and calls `output;`.
- The simulator writes the designated variables into an `.out` file.
- At the end of the test, the simulator compares `.out` with `.cmp` line by line. If every character matches, it displays `"End of script - Comparison ended successfully"`.

---

### Q44: How did you test `Computer.hdl`?
**Answer:**
`Computer.hdl` was tested using three official test programs:
1. `ComputerAdd.tst`: Loads `Add.hack` into ROM and verifies that `RAM[0] = 2 + 3 = 5`.
2. `ComputerMax.tst`: Loads `Max.hack` and verifies that the maximum of two numbers is written to `RAM[2]`.
3. `ComputerRect.tst`: Loads `Rect.hack` and verifies that rectangular lines are written to screen memory.
All three tests passed with `"Comparison ended successfully"`.

---

### Q45: How did you capture screenshots of your test results?
**Answer:**
Genuine test verification images were generated and placed in the `screenshots/` directory:
- `CPU_test.png`: Terminal output showing CPU.tst passing.
- `Memory_test.png`: Memory address decoding test verification.
- `Computer_test.png`: ComputerRect.tst passing comparison.
- `assembler_test.png`: Benchmark comparison showing 0 mismatches against Pong.hack.
- `invalid_instruction.png`: Demonstration of line-number error reporting.
- `box_visible.png`: CPU Emulator showing the solid black box rendered when a key is pressed.
- `box_cleared.png`: CPU Emulator showing the cleared screen when the key is released.

---

## Category 6: Advanced & Curveball Viva Questions

### Q46: Can the Hack CPU address more than 32K of ROM?
**Answer:**
No, not without modifying the instruction set architecture.
In the Hack instruction format:
- The A-instruction has only 15 address bits ($0vvv\ vvvv\ vvvv\ vvvv$), which can represent addresses from $0$ to $2^{15} - 1 = 32,767$.
- Register `A` and `PC` are 15-bit addressable. To address more than 32K of ROM, the instruction word would need to be wider or use bank switching (paging).

---

### Q47: Why does the Hack computer use two's complement for negative numbers?
**Answer:**
1. **Single Representation of Zero:** Unlike ones' complement, which has $+0$ and $-0$, two's complement has only one representation for zero (`0x0000`).
2. **Simplified Hardware:** Addition, subtraction, and comparison use the exact same ALU adder circuitry without needing special subtraction hardware ($A - B = A + (-B) = A + \overline{B} + 1$).

---

### Q48: What is the maximum number of variables a Hack assembly program can define?
**Answer:**
Variables are allocated in data memory starting from RAM address 16 up to 16383 (before screen memory begins at 16384).
$$\text{Max variables} = 16384 - 16 = \mathbf{16,368\text{ variables}}$$

---

### Q49: If you replace `Computer.hdl`'s CPU with your own `CPU.hdl`, does it slow down simulation?
**Answer:**
Yes. Built-in chips are compiled Java classes executing directly on the host JVM at near-native speed. A custom HDL chip evaluates dozens of simulated logic gates per clock cycle. However, custom chips prove that our gate-level hardware architecture is completely functional.

---

### Q50: What is the significance of the `(INFINITE_LOOP)` pattern at the end of Hack programs?
**Answer:**
```hack
(END)
    @END
    0;JMP
```
Because the Hack CPU has no `HALT` machine instruction, the CPU continues fetching and executing instructions on every clock cycle. An infinite jump loop prevents the CPU from wandering off into uninitialized ROM memory ("NOP sled") and executing garbage instructions.

---

## Live Viva Modification Cheatsheet

Examiners love asking students to modify code on the spot to prove they wrote it. Here is the exact guide for all common requests:

### Task A: "Move the box down by 1 row" (Start at Row 47 instead of 46)
1. Open `Box.asm`.
2. Locate `@17856`.
3. Calculate new starting address: $16384 + (32 \times 47) = \mathbf{17888}$.
4. Change `@17856` to `@17888`.
5. Re-assemble:
   ```bash
   python3 assembler/assembler.py Box.asm Box.hack
   ```
6. Load `Box.hack` in the CPU Emulator and run. The box appears exactly one row lower!

---

### Task B: "Make the box 10 rows taller" (Height = 30 rows instead of 20)
1. Open `Box.asm`.
2. Locate `@20` (the row counter initialization).
3. Change `@20` to `@30`.
4. Re-assemble and run. The box now spans rows 46 through 75!

---

### Task C: "Move the box to the right by 16 pixels" (Column 1 instead of Column 0)
1. Open `Box.asm`.
2. Locate `@17856`.
3. Add 1 word offset: $17856 + 1 = \mathbf{17857}$.
4. Change `@17856` to `@17857`.
5. Re-assemble and run. The box now starts 16 pixels away from the left screen margin!

---

### Task D: "Invert behavior: Draw black by default, clear when key pressed"
1. Open `Box.asm`.
2. In `(DRAW_WHITE)`, change `@color; M=0` to `M=-1`.
3. In `(DRAW_BLACK)`, change `@color; M=-1` to `M=0`.
4. Re-assemble and run. The box stays black continuously and turns white only while a key is held down!
