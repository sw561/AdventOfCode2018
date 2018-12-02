#!/usr/bin/env bash
./01_frequency_changes/clever.py | diff 01_frequency_changes/output.txt -
./02_inventory/checksum.py | diff 02_inventory/output.txt -
