"""
General utility tools for Advent of Code daily programming challenges.
"""

from typing import Callable, Union, Literal

def smart_convert(value: str, target_type: str = "auto") -> Union[int, float, str]:
    """Convert string to specified type or auto-detect."""
    if not isinstance(value, str):
        return value
    
    value = value.strip()
    if not value:
        return value
    
    if target_type == "str" or target_type == "string":
        return value
    elif target_type == "int":
        return int(value)
    elif target_type == "float":
        return float(value)
    elif target_type == "auto" or target_type == "number":
        # Try integer first, then float
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value
    elif target_type == "mixed":
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value
    else:
        raise ValueError(f"Unknown target_type: {target_type}")

def parse_pairs(day: str, parse_type: str = "int") -> tuple[list, list]:
    """Parse input file with pairs of numbers and return two separate lists."""
    lines = parse(day)
    left_list = []
    right_list = []
    
    for line in lines:
        if line.strip():  # Skip empty lines
            parts = line.split()
            if len(parts) >= 2:
                left_list.append(smart_convert(parts[0], parse_type))
                right_list.append(smart_convert(parts[1], parse_type))
    
    return (left_list, right_list)

def parse_tuples(day: str, parse_type: str = "int") -> list[tuple]:
    """Parse input file with pairs and return list of tuples."""
    lines = parse(day)
    tuples_list = []
    
    for line in lines:
        if line.strip():  # Skip empty lines
            parts = line.split()
            if len(parts) >= 2:
                tuples_list.append((
                    smart_convert(parts[0], parse_type),
                    smart_convert(parts[1], parse_type)
                ))
    
    return tuples_list

def parse_numbers(day: str, parse_type: str = "int") -> list[Union[int, float]]:
    """Parse input file and return all numbers as a flat list."""
    lines = parse(day)
    numbers = []
    
    for line in lines:
        if line.strip():
            parts = line.split()
            for part in parts:
                try:
                    converted = smart_convert(part, parse_type)
                    if isinstance(converted, (int, float)):
                        numbers.append(converted)
                except (ValueError, TypeError):
                    pass  # Skip non-numeric values
    
    return numbers

def parse_grid(day: str, parse_type: str = "str") -> list[list[Union[str, int, float]]]:
    """Parse input file as a 2D grid."""
    lines = parse(day)
    grid = []
    for line in lines:
        if line.strip():
            if parse_type == "str" or parse_type == "string":
                grid.append(list(line))
            else:
                row = []
                for char in line:
                    try:
                        row.append(smart_convert(char, parse_type))
                    except (ValueError, TypeError):
                        if parse_type in ["auto", "mixed"]:
                            row.append(char)  # Keep as string if conversion fails
                        else:
                            continue  # Skip if strict type conversion fails
                if row:
                    grid.append(row)
    return grid

def parse_int_grid(day: str, parse_type: str = "int") -> list[list[Union[int, float]]]:
    """Parse input file as a 2D grid of numbers."""
    lines = parse(day)
    grid = []
    for line in lines:
        if line.strip():
            row = []
            for char in line:
                if char.isdigit() or (char == '.' and parse_type == "float"):
                    try:
                        row.append(smart_convert(char, parse_type))
                    except (ValueError, TypeError):
                        continue
            if row:  # Only add non-empty rows
                grid.append(row)
    return grid

def parse_sections(day: str, separator: str = "", parse_type: str = "str") -> list[list[Union[str, int, float]]]:
    """Parse input file separated by blank lines into sections."""
    lines = parse(day)
    sections = []
    current_section = []
    
    for line in lines:
        if line == separator:
            if current_section:
                sections.append(current_section)
                current_section = []
        else:
            if parse_type == "str" or parse_type == "string":
                current_section.append(line)
            else:
                try:
                    current_section.append(smart_convert(line, parse_type))
                except (ValueError, TypeError):
                    if parse_type in ["auto", "mixed"]:
                        current_section.append(line)
                    # Skip if strict conversion fails
    
    # Add the last section if it exists
    if current_section:
        sections.append(current_section)
    
    return sections

def parse(day: int, parse_type: str = "str") -> list[Union[str, int, float]]:
    """Parse input file and return raw lines."""
    input_file = f"input/day{day}.txt"
    with open(input_file, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        
        if parse_type == "str" or parse_type == "string":
            return lines
        else:
            result = []
            for line in lines:
                try:
                    result.append(smart_convert(line, parse_type))
                except (ValueError, TypeError):
                    if parse_type in ["auto", "mixed"]:
                        result.append(line)
                    # Skip if strict conversion fails
            return result

def parse_csv_line(day: int, delimiter: str = ",", parse_type: str = "str") -> list[list[Union[str, int, float]]]:
    """Parse input file where each line contains delimiter-separated values."""
    lines = parse(day, "str")  # Always get raw strings first
    result = []
    
    for line in lines:
        if line.strip():
            parts = line.split(delimiter)
            if parse_type == "str" or parse_type == "string":
                result.append(parts)
            else:
                row = []
                for part in parts:
                    try:
                        converted = smart_convert(part, parse_type)
                        row.append(converted)
                    except (ValueError, TypeError):
                        if parse_type in ["auto", "mixed"]:
                            row.append(part)  # Keep as string if conversion fails
                        # Skip if strict conversion fails
                if row:
                    result.append(row)
    
    return result

def parse_csv_numbers(day: int, delimiter: str = ",", parse_type: str = "auto") -> list[list[Union[int, float]]]:
    """Parse input file where each line contains delimiter-separated numbers."""
    lines = parse(day, "str")
    result = []
    
    for line in lines:
        if line.strip():
            parts = line.split(delimiter)
            row = []
            for part in parts:
                try:
                    converted = smart_convert(part, parse_type)
                    if isinstance(converted, (int, float)):
                        row.append(converted)
                except (ValueError, TypeError):
                    continue  # Skip non-numeric values
            if row:  # Only add rows with actual numbers
                result.append(row)
    
    return result

def parse_csv_mixed(day: int, delimiter: str = ",", parse_type: str = "mixed") -> list[list[Union[int, float, str]]]:
    """Parse input file with automatic type conversion."""
    return parse_csv_line(day, delimiter, parse_type)

def parse_single_line_numbers(day: int, delimiter: str = None, parse_type: str = "int") -> list[Union[int, float]]:
    """Parse a single line of numbers separated by delimiter."""
    lines = parse(day, "str")
    if not lines:
        return []
    
    line = lines[0]
    if delimiter:
        parts = line.split(delimiter)
    else:
        parts = line.split()
    
    result = []
    for part in parts:
        if part.strip():
            try:
                result.append(smart_convert(part, parse_type))
            except (ValueError, TypeError):
                continue  # Skip values that can't be converted
    
    return result

def parse_in_single_line(day: int, parse_type: str = "str") -> list[Union[str, int, float]]:
    """Parse input file and return a single line of data."""
    lines = parse(day, "str")
    if not lines:
        return ""
    else:
        return "".join(lines)

def quantify_method(data: any, method: Callable) -> int:
    """
    Quantify the result of a method applied to the data.
    """
    return sum(method(item) for item in data)
