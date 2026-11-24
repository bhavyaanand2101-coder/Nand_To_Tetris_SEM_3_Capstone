// ==================================================================
// Box.asm - Make the Computer Draw a Box
// Student: Bhavya Anand
// Roll Number: 2501730046
// Course: Nand to Tetris - I (ETCNTC301)
// University: K.R. Mangalam University
//
// Personal Number K = 46
//
// Specifications:
// - Starting row: 46
// - Ending row: 65 (Height = 20 rows)
// - Starting column: 0 (leftmost edge)
// - Width: 16 * ((46 mod 4) + 1) = 48 pixels
// - Words per row: 48 / 16 = 3 words
// - First screen address: SCREEN + 32 * 46 = 16384 + 1472 = 17856
// - Last screen address:  16384 + 32 * 65 + 2 = 18464 + 2 = 18466
// - Total words modified: 20 * 3 = 60 words
//
// Behavior:
// - When any key is pressed (KBD != 0): Draw a black box (all 1s).
// - When key is released (KBD == 0): Clear the box to white (all 0s).
// - Loops continuously.
// ==================================================================

(MAIN_LOOP)
    // Step 1: Read keyboard memory-mapped register KBD (address 24576)
    @KBD
    D=M

    // If key is pressed (KBD != 0), jump to KEY_PRESSED to set black
    @KEY_PRESSED
    D;JNE

    // Otherwise, key is not pressed (KBD == 0): set color to white (0)
    @color
    M=0
    @DRAW_BOX
    0;JMP

(KEY_PRESSED)
    // Key is pressed: set color to black (-1 = 1111111111111111 in binary)
    @color
    M=-1

(DRAW_BOX)
    // Step 2: Initialize screen pointer to first address of row 46
    // 16384 + (32 * 46) = 17856
    @17856
    D=A
    @row_ptr
    M=D

    // Step 3: Initialize row counter to 20 rows
    @20
    D=A
    @row_count
    M=D

(ROW_LOOP)
    // Check if all 20 rows have been drawn
    @row_count
    D=M
    @MAIN_LOOP
    D;JEQ           // When row_count == 0, finished box -> poll keyboard again

    // Load the current drawing color into D register
    @color
    D=M

    // --- Draw Word 0 (pixels 0 to 15 of current row) ---
    @row_ptr
    A=M
    M=D

    // --- Draw Word 1 (pixels 16 to 31 of current row) ---
    @row_ptr
    M=M+1
    A=M
    M=D

    // --- Draw Word 2 (pixels 32 to 47 of current row) ---
    @row_ptr
    M=M+1
    A=M
    M=D

    // --- Advance pointer to start of next screen row ---
    // Current row_ptr is at (row_start + 2).
    // The next row starts at (row_start + 32).
    // Difference: 32 - 2 = 30 words to reach the next row start.
    @30
    D=A
    @row_ptr
    M=M+D

    // Decrement row counter
    @row_count
    M=M-1

    // Repeat for the next row
    @ROW_LOOP
    0;JMP
