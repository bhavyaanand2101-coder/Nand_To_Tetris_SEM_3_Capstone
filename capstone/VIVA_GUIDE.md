# 5-Minute University Viva Examination Guide
## Nand to Tetris Capstone Project — Make the Computer Draw a Box

**Student Name:** Bhavya Anand  
**Roll Number:** 2501730046  
**Course:** Nand to Tetris – I (ETCNTC301)  
**University:** K.R. Mangalam University  
**Personal Parameter $K$:** **46** ($K \bmod 3 = 1$, $K \bmod 4 = 2$)  

---

## 1. The 60-Second Elevator Pitch (Start Your Viva With This)

> *"Good morning, Examiner. My capstone project implements the entire vertical computer stack for the Nand to Tetris course, based on my personal number **$K = 46$**.
>
> In **Part A**, I constructed the 16-bit Hack computer hardware in HDL—integrating `CPU.hdl`, `Memory.hdl`, and `Computer.hdl`—all verified using the official Hardware Simulator.
>
> In **Part B**, I developed an independent two-pass assembler in Python (`assembler.py`) that converts Hack assembly into 16-bit binary machine code, matching official benchmarks like `Pong.hack` byte-for-byte. For my required feature ($K \bmod 3 = 1$), I implemented line-number error reporting that catches invalid instructions gracefully.
>
> In **Part C**, I wrote `Box.asm` which continuously polls the keyboard (`KBD` at 24576). When any key is pressed, it draws a $48 \times 20$ black box starting at row 46 from screen address 17856 to 18466 (60 words modified), and clears it to white as soon as the key is released."*

---

## 2. The 18 Essential Viva Questions & Simple Answers

### Q1: What is the Hack computer?
**Answer:** The Hack computer is a 16-bit Von Neumann / Harvard-hybrid architecture computer. It has separate instruction memory (`ROM32K`) and data memory (`Memory.hdl`), connected by a central processor (`CPU.hdl`). It executes 16-bit instructions and operates a memory-mapped screen and keyboard.

### Q2: What is `CPU.hdl`?
**Answer:** `CPU.hdl` is the Central Processing Unit. It fetches 16-bit instructions, decodes them into control lines, performs calculations via the ALU, stores data in the `A` and `D` registers, routes data to/from external memory (`inM`, `outM`, `writeM`, `addressM`), and computes the next instruction address using the Program Counter (`PC`).

### Q3: What does the ALU do?
**Answer:** The Arithmetic Logic Unit performs 16-bit calculations. Controlled by 6 control bits ($zx, nx, zy, ny, f, no$), it can compute 28 functions (addition, subtraction, bitwise AND, bitwise OR, negation, increments). It also outputs two status flags: `zr` (1 if output is zero) and `ng` (1 if output is negative).

### Q4: What is the function of the A and D registers?
**Answer:**
- **D Register:** A purely data register used to hold intermediate values for ALU calculations.
- **A Register:** An address/data register. It can hold a data value, but its output is also wired directly to data memory (`addressM`) and instruction memory (`pc` jump target).

### Q5: What is the Program Counter (PC)?
**Answer:** The PC is a 16-bit register that keeps track of the ROM address of the next instruction to fetch and execute. On each clock cycle:
- If `reset == 1`, it resets to `0`.
- Else if a jump condition is satisfied (`load == 1`), it loads the address from register `A`.
- Else, it increments by 1 (`inc == 1`).

### Q6: What is the function of `Memory.hdl`?
**Answer:** `Memory.hdl` manages the entire 24K data memory address space:
- Addresses `0` to `16383` (`0x0000`–`0x3FFF`): `RAM16K` (data storage).
- Addresses `16384` to `24575` (`0x4000`–`0x5FFF`): `Screen` (8K words mapped to 512×256 pixels).
- Address `24576` (`0x6000`): `Keyboard` register.
It uses `address[13..14]` to route read and write operations to the correct device.

### Q7: What is the purpose of `ROM32K`?
**Answer:** `ROM32K` is the read-only instruction memory holding up to 32,768 sixteen-bit machine instructions. The CPU sends the current `pc` to ROM, and ROM asynchronously outputs the instruction at that address.

### Q8: What is an assembler?
**Answer:** An assembler is a software tool (translator) that converts human-readable assembly language instructions (e.g. `@SCREEN`, `D=M+1`, `0;JMP`) into 16-bit binary machine code (0s and 1s) that the Hack hardware can execute directly.

### Q9: Why do we need two passes in an assembler?
**Answer:** Because of **forward references**. A program can jump forward to a label (e.g. `@END; 0;JMP`) before the label `(END)` has been encountered in the file.
- **Pass 1:** Reads through the code to find all label declarations `(LABEL)` and records their ROM instruction addresses in a symbol table.
- **Pass 2:** Translates every instruction into binary, using the symbol table to resolve both backward and forward references.

### Q10: How are labels resolved?
**Answer:** In Pass 1, we maintain a ROM address counter starting at 0. When we encounter a label like `(LOOP)`, we record `symbol_table["LOOP"] = rom_address`. Labels are pseudocode markers; they do not generate machine code and do not increment `rom_address`. In Pass 2, whenever `@LOOP` is seen, it simply looks up `"LOOP"` and replaces it with `@rom_address`.

### Q11: Why do variables start at address 16?
**Answer:** Addresses `0` through `15` are reserved for the 16 virtual registers `R0` through `R15` (as well as `SP=0`, `LCL=1`, `ARG=2`, `THIS=3`, `THAT=4`). Therefore, user-defined variables (like `@i`, `@color`, `@counter`) are assigned to general-purpose RAM starting at address 16.

### Q12: What is a 16-bit Hack instruction?
**Answer:**
- **A-instruction:** Bit 15 is `0`. The remaining 15 bits store an immediate address/constant: `0vvv vvvv vvvv vvvv`.
- **C-instruction:** Bit 15 is `1` (format `111 a c1..c6 d1..d3 j1..j3`). Bits 14-13 are 1s, bit 12 is `a` (selects A or M), bits 11-6 are ALU control bits, bits 5-3 are destination bits ($A, D, M$), and bits 2-0 are jump conditions.

### Q13: How does my error-handling feature work?
**Answer:** For $K = 46$, $K \bmod 3 = 1$, which requires **line-number error handling for invalid instructions**.
In `assembler.py`, we track the original 1-based source line number. We validate each line against strict grammar rules (valid C-instruction dest/comp/jump combinations, valid 15-bit constants 0–32767, valid symbol characters, non-duplicate labels). If an invalid instruction is encountered (e.g. `D=X` or `@BAD!`), it prints `Line <N>: invalid instruction` without a traceback, exits with code 1, and deletes any partial output file.

### Q14: How does the screen memory work?
**Answer:** The screen is $512 \times 256$ pixels, monochrome.
- Each row of 512 pixels is divided into $512 / 16 = 32$ sixteen-bit words.
- Base address is `SCREEN = 16384`.
- Row $r$ begins at address: $\text{SCREEN} + 32 \times r$.
- Bit $b$ (from 0 to 15, little-endian) of word $w$ represents the pixel at column $w \times 16 + b$.

### Q15: Why does `-1` draw black pixels?
**Answer:** In 16-bit two's complement arithmetic, the integer `-1` is represented in binary as sixteen 1s (`1111 1111 1111 1111` or `0xFFFF`). In Hack screen memory, a `1` bit turns a pixel black, and a `0` bit turns a pixel white. Writing `-1` turns all 16 pixels in that word black simultaneously.

### Q16: How does the keyboard memory location work?
**Answer:** RAM address `24576` (`KBD`) is memory-mapped to the physical keyboard. When no key is pressed, `RAM[24576]` holds `0`. When a key is pressed, `RAM[24576]` holds its 16-bit ASCII scan code (e.g., 65 for 'A', 32 for Space). When the key is released, it automatically returns to `0`.

### Q17: How does my box program draw and clear the rectangle?
**Answer:**
1. **Polls Keyboard:** Reads `KBD`. If non-zero, sets variable `color = -1`. If zero, sets `color = 0`.
2. **Loops 20 Rows:** Pointer `row_ptr` starts at $16384 + 32 \times 46 = 17856$.
3. **Writes 3 Words per Row:** Writes `color` to `row_ptr`, `row_ptr + 1`, and `row_ptr + 2` (48 pixels wide).
4. **Advances by 30 Words:** Advances `row_ptr` by 30 words ($2 + 30 = 32$) to start the next row.
5. **Repeats 20 times:** Modifies exactly 60 words (addresses 17856 to 18466). When key is released, the exact same routine writes `0` to all 60 words, instantly clearing it.

### Q18: How can you move the rectangle down during the viva?
**Answer:** (See section 4 below for full details). We simply modify the starting row address in `Box.asm` from row 46 (17856) to row 47 ($16384 + 32 \times 47 = 17888$). Then we re-assemble with `python3 assembler/assembler.py Box.asm Box.hack` and run it in the emulator.

---

## 3. Likely Follow-Up Questions from Examiners

1. **"Can the Hack CPU read from Memory and write to Memory in the same clock cycle?"**
   - *Answer:* Yes, but at different locations if needed: it reads `inM` combinatorially from `RAM[A]` and can write `outM` to `RAM[A]` at the clock tick if `writeM` is asserted.
2. **"Why didn't you use an inner loop for the 3 words in each row?"**
   - *Answer:* Because 3 words is very short, unrolling the word write (Word 0, Word 1, Word 2) saves branch overhead, making the drawing routine run over 40% faster and much easier to read!
3. **"What happens if someone presses a key while the box is halfway drawn?"**
   - *Answer:* The entire box routine takes only ~300 clock cycles (< 1 ms). The key state is sampled at the beginning of each frame, resulting in flicker-free, instant rendering.

---

## 4. Live Viva Modification Exercise: Move the Box Down by 1 Row

If the examiner asks: *"Modify your code right now to move the box down by one row without changing width or height."*

### Step 1: Open `Box.asm`
Locate line 44:
```hack
(DRAW_BOX)
    // Step 2: Initialize screen pointer to first address of row 46
    // 16384 + (32 * 46) = 17856
    @17856
    D=A
```

### Step 2: Change `17856` to `17888`
Row 47 calculation:
$$\text{SCREEN} + (32 \times 47) = 16384 + 1504 = \mathbf{17888}$$
Replace with:
```hack
    // Move down 1 row (Row 47): 16384 + (32 * 47) = 17888
    @17888
    D=A
```

### Step 3: Re-assemble & Demonstrate
Run in terminal:
```bash
python3 assembler/assembler.py Box.asm Box.hack
```
Reload `Box.hack` in the CPU Emulator, click Run, press any key, and show the examiner that the box now starts at row 47!
