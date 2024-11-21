import sys

def remove_chars(filename, num_chars):
    """Removes the first num_chars characters from each line in a file.

    Args:
        filename (str): The name of the input file.
        num_chars (int): The number of characters to remove from each line.
    """

    with open(filename, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        new_line = line[num_chars:]
        new_lines.append(new_line)

    with open(filename, 'w') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python remove_chars.py <filename> <num_chars>")
        sys.exit(1)

    filename = sys.argv[1]
    num_chars = int(sys.argv[2])

    remove_chars(filename, num_chars)