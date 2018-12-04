#!/usr/bin/env bash
./01_frequency_changes/clever.py | diff 01_frequency_changes/output.txt -
./02_inventory/checksum.py | diff 02_inventory/output.txt -
./03_fabric_cutting/overlapping.py | diff 03_fabric_cutting/output.txt -
./04_guards/guard.py | diff 04_guards/output.txt -
