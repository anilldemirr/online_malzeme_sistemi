#!/usr/bin/env python
"""Verify syntax of new endpoint files."""
import py_compile
import sys

files = [
    'club_inventory/src/api/v1/endpoints/equipment.py',
    'club_inventory/src/api/v1/endpoints/transactions.py',
]

try:
    for file in files:
        print(f"Checking {file}...")
        py_compile.compile(file, doraise=True)
    print("✓ All files have valid syntax!")
except py_compile.PyCompileError as e:
    print(f"✗ Syntax error: {e}")
    sys.exit(1)
