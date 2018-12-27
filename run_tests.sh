#!/usr/bin/env bash
./01_frequency_changes/clever.py | diff 01_frequency_changes/output.txt -
./02_inventory/checksum.py | diff 02_inventory/output.txt -
./03_fabric_cutting/overlapping.py | diff 03_fabric_cutting/output.txt -
./04_guards/guard.py | diff 04_guards/output.txt -
./05_polymer/polymer.py | diff 05_polymer/output.txt -
./06_voronoi/chronal.py | diff 06_voronoi/output.txt -
./07_gantt/tasks.py | diff 07_gantt/output.txt -
./08_metadata/metadata.py | diff 08_metadata/output.txt -
./09_marble/marble.py | diff 09_marble/output.txt -
./10_stars/stars_align.py | diff 10_stars/output.txt -
./11_fuel_cell/power.py | diff 11_fuel_cell/output.txt -
./12_plants/plants.py | diff 12_plants/output.txt -
./13_mine_cart/mine.py | diff 13_mine_cart/output.txt -
./14_recipes/recipes.py | diff 14_recipes/output.txt -
./15_elves_goblins/elves.py | diff 15_elves_goblins/output.txt -
./16_reverse_assembly/code.py | diff 16_reverse_assembly/output.txt -
./17_water/flow.py | diff 17_water/output.txt -
