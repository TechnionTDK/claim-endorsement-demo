import sys

def add_comma(filename):
    """Adds a comma to the end of each line in a file that doesn't end with a curly brace.

    Args:
        filename (str): The name of the input file.
    """

    with open(filename, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.strip() == '':
            continue
        if "{" not in line and "}" not in line:
            seperated=line.strip().split(':',1)
            print(seperated)
            line=seperated[1][:-1]+":" +seperated[0]+","+"\n"
            new_lines.append(line)
            continue


       # line=line.replace('{','[')
        line=line.replace('}','},')
        new_lines.append(line)

    with open(filename, 'w') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python add_comma.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    add_comma(filename)