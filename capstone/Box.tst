// Box.tst - Test script for Box.hack on CPU Emulator
// Student: Bhavya Anand (Roll: 2501730046, K = 46)

load /Users/bhavya/Desktop/ /Sem_3/Nand To Tetris/Capstone/Box.hack,
output-file Box.out,
compare-to Box.cmp,
output-list RAM[17856]%D1.6.1 RAM[17857]%D1.6.1 RAM[17858]%D1.6.1 RAM[18464]%D1.6.1 RAM[18465]%D1.6.1 RAM[18466]%D1.6.1;

// Test Case 1: Key Pressed (ASCII 65 = 'A')
set RAM[24576] 65,
repeat 1500 {
    ticktock;
}
output;

// Test Case 2: Key Released (0)
set RAM[24576] 0,
repeat 1500 {
    ticktock;
}
output;
