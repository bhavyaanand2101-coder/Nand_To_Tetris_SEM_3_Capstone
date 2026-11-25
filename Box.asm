// ==================================================================
// Box.asm - Make the Computer Draw a Box
// Student: Bhavya Anand
// Roll Number: 2501730046
// Personal Number K = 46
// Course: Nand to Tetris - I (ETCNTC301)
// University: K.R. Mangalam University
//
// Specifications for K = 46:
// - Starting row: 46
// - Box height: 20 rows
// - Box width: 48 pixels (3 words per row)
// - First screen address: 16384 + (32 * 46) = 17856
// - Register D displays 46 (student personal number K)
// ==================================================================

(MAIN_LOOP)
    // Put Personal Number K = 46 into D register so D shows 46
    @46
    D=A

    // Step 1: Read keyboard register KBD (address 24576)
    @KBD
    D=M

    // If key is pressed (KBD != 0), jump to KEY_PRESSED
    @KEY_PRESSED
    D;JNE

    // Otherwise (key released): set color to white (0)
    @color
    M=0
    @DRAW_BOX
    0;JMP

(KEY_PRESSED)
    // Key is pressed: set color to black (-1)
    @color
    M=-1

(DRAW_BOX)
    // Initialize screen pointer to row 46: 16384 + (32 * 46) = 17856
    @17856
    D=A
    @row_ptr
    M=D

    // Initialize row counter to 20 rows
    @20
    D=A
    @row_count
    M=D

(ROW_LOOP)
    // Check if 20 rows completed
    @row_count
    D=M
    @FINISH_FRAME
    D;JEQ

    // Load color into D
    @color
    D=M

    // Word 0 (pixels 0..15)
    @row_ptr
    A=M
    M=D

    // Word 1 (pixels 16..31)
    @row_ptr
    M=M+1
    A=M
    M=D

    // Word 2 (pixels 32..47)
    @row_ptr
    M=M+1
    A=M
    M=D

    // Advance to next row (30 words forward)
    @30
    D=A
    @row_ptr
    D=D+M
    @row_ptr
    M=D

    // Decrement row counter
    @row_count
    M=M-1

    @ROW_LOOP
    0;JMP

(FINISH_FRAME)
    // Put Personal Number K = 46 into register D!
    @46
    D=A

    // Loop back to poll keyboard again
    @MAIN_LOOP
    0;JMP
