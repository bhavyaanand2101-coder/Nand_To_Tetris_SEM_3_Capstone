#!/usr/bin/env python3
"""
Hack Computer Assembler (assembler.py)
Author: Bhavya Anand (Roll No: 2501730046, K = 46)
Course: Nand to Tetris – I (ETCNTC301)
University: K.R. Mangalam University

Translates Hack assembly language (.asm) programs into Hack 16-bit
binary machine code (.hack).

Features:
- Two-pass assembler design (Pass 1: labels, Pass 2: code translation).
- Predefined Hack symbols (SP, LCL, ARG, THIS, THAT, R0-R15, SCREEN, KBD).
- Variable allocation starting at RAM address 16.
- Additional Feature (K mod 3 = 1):
  Invalid instruction error handling with original source line numbers
  (e.g., "Line 7: invalid instruction").
"""

import sys
import os
import re

# Predefined Symbols in Hack architecture
PREDEFINED_SYMBOLS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
}
for i in range(16):
    PREDEFINED_SYMBOLS[f"R{i}"] = i

# C-Instruction Computation (comp) Table: 7-bit string (a c1 c2 c3 c4 c5 c6)
COMP_TABLE = {
    # a = 0 (ALU operates on D and A)
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "A+D": "0000010",  # Commutative addition
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "A&D": "0000000",  # Commutative AND
    "D|A": "0010101",
    "A|D": "0010101",  # Commutative OR

    # a = 1 (ALU operates on D and M)
    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "M+D": "1000010",  # Commutative addition
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "M&D": "1000000",  # Commutative AND
    "D|M": "1010101",
    "M|D": "1010101",  # Commutative OR
}

# C-Instruction Destination (dest) Table: 3-bit string (d1 d2 d3)
DEST_TABLE = {
    "":    "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "DM":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111",
    "ADM": "111",
}

# C-Instruction Jump (jump) Table: 3-bit string (j1 j2 j3)
JUMP_TABLE = {
    "":    "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

# Valid symbol regex: letter/symbol followed by letters, digits, _, ., $, :
SYMBOL_REGEX = re.compile(r"^[a-zA-Z_.$:][a-zA-Z0-9_.$:]*$")


class AssemblyError(Exception):
    """Exception raised for assembly syntax and instruction errors with line numbers."""
    def __init__(self, line_num, message="invalid instruction"):
        self.line_num = line_num
        self.message = message
        super().__init__(f"Line {line_num}: {message}")


class HackAssembler:
    def __init__(self):
        self.symbol_table = dict(PREDEFINED_SYMBOLS)
        self.next_var_address = 16
        self.num_labels = 0
        self.num_variables = 0

    def clean_line(self, raw_line):
        """Remove comments and whitespace from a source line."""
        # Strip comments
        code = raw_line.split("//")[0]
        # Remove all whitespace for instruction parsing
        return code.strip()

    def assemble(self, asm_source_lines):
        """
        Two-pass assembly of Hack assembly code.
        Returns a list of 16-bit binary instruction strings.
        Raises AssemblyError on syntax or invalid instruction.
        """
        self.symbol_table = dict(PREDEFINED_SYMBOLS)
        self.next_var_address = 16
        self.num_labels = 0
        self.num_variables = 0

        # PASS 1: Read lines, strip comments/whitespace, resolve labels to ROM addresses.
        rom_address = 0
        cleaned_instructions = []  # list of tuples: (line_num, cleaned_text)

        for line_idx, raw_line in enumerate(asm_source_lines):
            line_num = line_idx + 1
            cleaned = self.clean_line(raw_line)
            if not cleaned:
                continue

            # Check if line is a label declaration: (LABEL)
            if cleaned.startswith("(") and cleaned.endswith(")"):
                label = cleaned[1:-1].strip()
                if not label or not SYMBOL_REGEX.match(label):
                    raise AssemblyError(line_num, "invalid instruction")
                if label in self.symbol_table:
                    # Duplicate label or collision with predefined symbol
                    raise AssemblyError(line_num, "invalid instruction")
                self.symbol_table[label] = rom_address
                self.num_labels += 1
            else:
                cleaned_instructions.append((line_num, cleaned))
                rom_address += 1

        # PASS 2: Translate instructions into 16-bit binary code.
        binary_code = []

        for line_num, inst in cleaned_instructions:
            if inst.startswith("@"):
                # A-instruction: @value
                binary = self._translate_a_instruction(inst, line_num)
            else:
                # C-instruction: dest=comp;jump
                binary = self._translate_c_instruction(inst, line_num)
            binary_code.append(binary)

        return binary_code

    def _translate_a_instruction(self, inst, line_num):
        """Translate an A-instruction into 0vvvvvvvvvvvvvvv (16 bits)."""
        val_str = inst[1:].strip()
        if not val_str:
            raise AssemblyError(line_num, "invalid instruction")

        # Check if numeric constant
        if val_str.isdigit():
            val = int(val_str)
            if val < 0 or val > 32767:
                raise AssemblyError(line_num, "invalid instruction")
            return f"0{val:015b}"

        # Otherwise it must be a valid symbol (label, predefined, or variable)
        if not SYMBOL_REGEX.match(val_str):
            raise AssemblyError(line_num, "invalid instruction")

        if val_str in self.symbol_table:
            val = self.symbol_table[val_str]
        else:
            # Allocate new variable in RAM starting at 16
            val = self.next_var_address
            self.symbol_table[val_str] = val
            self.next_var_address += 1
            self.num_variables += 1

        return f"0{val:015b}"

    def _translate_c_instruction(self, inst, line_num):
        """
        Translate a C-instruction into 111accccccdddjjj (16 bits).
        Format: dest=comp;jump (dest or jump optional).
        """
        # Remove internal spaces
        inst_no_space = "".join(inst.split())

        dest_part = ""
        jump_part = ""
        comp_part = ""

        # Parse dest
        if "=" in inst_no_space:
            dest_part, rest = inst_no_space.split("=", 1)
        else:
            rest = inst_no_space

        # Parse jump
        if ";" in rest:
            comp_part, jump_part = rest.split(";", 1)
        else:
            comp_part = rest

        # Validate destination
        if dest_part not in DEST_TABLE:
            raise AssemblyError(line_num, "invalid instruction")

        # Validate computation
        if comp_part not in COMP_TABLE:
            raise AssemblyError(line_num, "invalid instruction")

        # Validate jump
        if jump_part not in JUMP_TABLE:
            raise AssemblyError(line_num, "invalid instruction")

        comp_bits = COMP_TABLE[comp_part]
        dest_bits = DEST_TABLE[dest_part]
        jump_bits = JUMP_TABLE[jump_part]

        return f"111{comp_bits}{dest_bits}{jump_bits}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 assembler.py <file.asm> [output.hack]")
        sys.exit(1)

    asm_file = sys.argv[1]
    if not os.path.isfile(asm_file):
        print(f"Error: file not found: {asm_file}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        hack_file = sys.argv[2]
    else:
        base_name = os.path.splitext(asm_file)[0]
        hack_file = f"{base_name}.hack"

    try:
        with open(asm_file, "r") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {asm_file}: {e}")
        sys.exit(1)

    assembler = HackAssembler()
    try:
        binary_lines = assembler.assemble(lines)
    except AssemblyError as e:
        # Standard error handling feature based on K:
        # Print "Line <N>: invalid instruction" without python traceback.
        sys.stderr.write(f"{e}\n")
        # Ensure no partial hack file is left
        if os.path.exists(hack_file):
            try:
                os.remove(hack_file)
            except OSError:
                pass
        sys.exit(1)

    # Write output file
    try:
        with open(hack_file, "w") as f:
            for b in binary_lines:
                f.write(f"{b}\n")
    except Exception as e:
        print(f"Error writing {hack_file}: {e}")
        sys.exit(1)

    print(f"=== Hack Assembly Successful ===")
    print(f"Input file:             {asm_file}")
    print(f"Output file:            {hack_file}")
    print(f"Instructions assembled: {len(binary_lines)}")
    print(f"Labels defined:         {assembler.num_labels}")
    print(f"Variables allocated:    {assembler.num_variables}")
    print(f"Status:                 SUCCESS")


if __name__ == "__main__":
    main()
