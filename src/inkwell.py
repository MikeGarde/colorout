import os
import sys
import re
import argparse

__version__ = "0.0.0"
__version_info__ = tuple([int(num) for num in __version__.split('.')])

closer = r'\x1b\[0m|\x1b\[39;49m'

# Define ANSI color codes
ansi_codes = {
    'bold':      r'\x1b\[1m',
    'underline': r'\x1b\[4m',
    'red':       r'\x1b\[31m',
    'green':     r'\x1b\[32m',
    'yellow':    r'\x1b\[33m',
    'blue':      r'\x1b\[34m',
    'magenta':   r'\x1b\[35m',
    'cyan':      r'\x1b\[36m',
    'white':     r'\x1b\[37m',
}

# Define HTML and Markdown replacements
md_tags = {
    'bold':      ('<span style="font-weight:bold">', '</span>'),
    'underline': ('<span style="text-decoration:underline">', '</span>'),
    'red':       ('<span style="color:red">', '</span>'),
    'green':     ('<span style="color:green">', '</span>'),
    'yellow':    ('<span style="color:yellow">', '</span>'),
    'blue':      ('<span style="color:blue">', '</span>'),
    'magenta':   ('<span style="color:magenta">', '</span>'),
    'cyan':      ('<span style="color:cyan">', '</span>'),
    'white':     ('<span style="color:white">', '</span>'),
}

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
parser.add_argument('--md', action='store_true')
parser.add_argument('--html', action='store_true')
parser.add_argument('--file', type=str)
args = parser.parse_args()

if args.md and args.html:
    print("Error: Cannot use --md and --html flags together.")
    sys.exit(1)
if not args.md and not args.html:
    args.md = True


def line_worker(line):
    # Replace bold ANSI code first
    def replacer(m):
        return f'{md_tags["bold"][0]}{m.group(1)}{md_tags["bold"][1]}'

    line = re.sub(f'{ansi_codes["bold"]}(.*?)(?={closer})', replacer, line)
    # Replace ANSI color codes with HTML or Markdown
    for code in ansi_codes:
        if code == "bold":
            continue
        # Find all occurrences of the current ANSI code
        matches = re.findall(f'{ansi_codes[code]}(.*?)(?={closer})', line)

        # Replace each occurrence with the corresponding HTML tag
        for match in matches:
            def replacer(m):
                return f'{md_tags[code][0]}{m.group(1)}{md_tags[code][1]}'

            line = re.sub(f'{ansi_codes[code]}(.*?)(?={closer})', replacer, line)

    print(line, end='')


if args.file:
    full_path = os.path.abspath(args.file)
    # Read from file
    try:
        with open(full_path, 'r') as f:
            for line in f:
                line_worker(line)
    except FileNotFoundError:
        print(f"Error: File {full_path} not found.")
    except PermissionError:
        print(f"Error: Permission denied to read file {full_path}.")
else:
    # Read from stdin
    for line in sys.stdin:
        line_worker(line)
