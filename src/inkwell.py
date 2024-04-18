import os
import sys
import re
import argparse

__version__ = "0.0.0"
__version_info__ = tuple([int(num) for num in __version__.split('.')])

closer = r'\x1b\[0m|\x1b\[39;49m'
starter = r'\x1b\['

# Define ANSI color codes
ansi_codes = {
    1: 'bold',
    4: 'underline',
    31: 'red',
    32: 'green',
    33: 'yellow',
    34: 'blue',
    35: 'magenta',
    36: 'cyan',
    37: 'white',
}

# Define HTML and Markdown replacements
tags = {
    'bold':      'font-weight',
    'underline': 'text-decoration',
    'red':       'color',
    'green':     'color',
    'yellow':    'color',
    'blue':      'color',
    'magenta':   'color',
    'cyan':      'color',
    'white':     'color',
}

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
parser.add_argument('--file', type=str)
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()


def line_worker(single_line):
    pattern = r"(\x1b\[0m)?\x1b\[([0-9]{1,2});?([0-9]{1,2})?m(.*)?\x1b\[[0-9]{1,2}(;[0-9]{1,2})?m"
    matches = re.findall(pattern, single_line)

    if args.debug:
        print(matches)

    for match in matches:
        foreground = int(match[1])
        background = int(match[2])

        if foreground in ansi_codes:
            foreground = ansi_codes[foreground]
        else:
            if args.debug:
                print(f"Error: Unknown ANSI code {foreground}")
            foreground = None

        if background in ansi_codes:
            background = ansi_codes[background]
        else:
            if args.debug:
                print(f"Error: Unknown ANSI code {background}")
            background = None

        text = match[3]

        if args.debug:
            print(f"Foreground: {foreground}, Background: {background}, Text: {text}")

        # Replace ANSI color codes with HTML or Markdown
        span = "<span style='"
        if foreground:
            span += tags[foreground] + ": " + foreground + ";"
        if background:
            span += tags[background] + ": " + background + ";"
        span += "'>" + text + "</span>"

        new_line = re.sub(pattern, span, single_line)
        print(new_line, end='')


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
