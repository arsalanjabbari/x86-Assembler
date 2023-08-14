# x86-Assembler

This repository contains a Python project that implements an assembler for a custom instruction set architecture. The assembler takes assembly code as input and converts it into machine code. The supported instructions include ADD, SUB, AND, OR, and JMP. The assembler also supports working with registers and memory.

## Table of Contents
- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Conclusion](#conclusion)

## Introduction
This project aims to create an assembler in Python that translates assembly code into machine code for a custom instruction set architecture. The assembler supports various instructions and memory operations, making it a versatile tool for developers working with this architecture.

## Project Overview
The project provides a Python script (`main.py`) that performs the assembly-to-machine code conversion. It employs a set of rules and functions to validate and process assembly instructions, operands, registers, and memory addresses.

## Features
- Converts assembly code to machine code for supported instructions.
- Handles memory operations and register manipulation.
- Validates the correctness of instruction syntax and operands.
- Generates machine code based on opcode tables and operand properties.

## Getting Started
To use the assembler, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/arsalanjabbari/x86-Assembler
   cd x86-Assembler
   ```

2. Open the `main.py` script in a text editor or IDE of your choice.

3. Modify the `inp.txt` file to contain your assembly code instructions, with one instruction per line.

4. Run the `main.py` script:
   ```
   python main.py
   ```

5. The script will process the assembly code from `inp.txt` and display the corresponding machine code output.

## Conclusion
The provided Python project offers a basic assembler implementation that can convert assembly code into machine code for supported instructions. It demonstrates the process of opcode handling, operand validation, and machine code generation. You can further extend and enhance this project to support additional instructions, error handling, and more advanced features.
