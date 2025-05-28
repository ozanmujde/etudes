"""
General utility tools for Advent of Code daily programming challenges.
"""

def parse_raw(day: str) -> list[str]:
    """Parse input file and return raw lines as strings."""
    input_file = f"input/day{day}.txt"
    with open(input_file, 'r') as file:
        return [line.strip() for line in file.readlines()]

def parse_pairs(day: str) -> tuple[list, list]:
    """Parse input file with pairs of numbers and return two separate lists."""
    lines = parse_raw(day)
    left_list = []
    right_list = []
    
    for line in lines:
        if line.strip():  # Skip empty lines
            parts = line.split()
            if len(parts) >= 2:
                left_list.append(int(parts[0]))
                right_list.append(int(parts[1]))
    
    return (left_list, right_list)

def parse_tuples(day: str) -> list[tuple]:
    """Parse input file with pairs and return list of tuples."""
    lines = parse_raw(day)
    tuples_list = []
    
    for line in lines:
        if line.strip():  # Skip empty lines
            parts = line.split()
            if len(parts) >= 2:
                tuples_list.append((int(parts[0]), int(parts[1])))
    
    return tuples_list

def parse_numbers(day: str) -> list[int]:
    """Parse input file and return all numbers as a flat list."""
    lines = parse_raw(day)
    numbers = []
    
    for line in lines:
        if line.strip():
            parts = line.split()
            for part in parts:
                try:
                    numbers.append(int(part))
                except ValueError:
                    pass  # Skip non-numeric values
    
    return numbers

def parse_grid(day: str) -> list[list[str]]:
    """Parse input file as a 2D grid of characters."""
    lines = parse_raw(day)
    return [list(line) for line in lines if line.strip()]

def parse_int_grid(day: str) -> list[list[int]]:
    """Parse input file as a 2D grid of integers."""
    lines = parse_raw(day)
    grid = []
    for line in lines:
        if line.strip():
            row = []
            for char in line:
                if char.isdigit():
                    row.append(int(char))
            if row:  # Only add non-empty rows
                grid.append(row)
    return grid

def parse_sections(day: str, separator: str = "") -> list[list[str]]:
    """Parse input file separated by blank lines into sections."""
    lines = parse_raw(day)
    sections = []
    current_section = []
    
    for line in lines:
        if line == separator:
            if current_section:
                sections.append(current_section)
                current_section = []
        else:
            current_section.append(line)
    
    # Add the last section if it exists
    if current_section:
        sections.append(current_section)
    
    return sections

# Backward compatibility - keeping the original function name
def parse(day: str) -> list[str]:
    """Parse input file and return raw lines (backward compatible)."""
    return parse_raw(day)

# Convenience functions for common patterns
def parse_csv_line(day: str, delimiter: str = ",") -> list[list[str]]:
    """Parse input file where each line contains comma-separated values."""
    lines = parse_raw(day)
    return [line.split(delimiter) for line in lines if line.strip()]

def parse_single_line_numbers(day: str, delimiter: str = None) -> list[int]:
    """Parse a single line of numbers separated by delimiter (default: any whitespace)."""
    lines = parse_raw(day)
    if not lines:
        return []
    
    line = lines[0]
    if delimiter:
        parts = line.split(delimiter)
    else:
        parts = line.split()
    
    return [int(part) for part in parts if part.strip()]

