import argparse
import os
import re
import sys

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
parser = argparse.ArgumentParser(
    description='Convert ANSI color codes to HTML or Markdown.',
)
parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
parser.add_argument('--html', action='store_true', help='wrap output with html tags')
parser.add_argument('--title', type=str, metavar='\'ls -la\'', help='title for html output, invokes html flag')
parser.add_argument('--debug', action='store_true')
parser.add_argument('file', type=str, nargs='?', metavar='input.txt', help='read from file instead of stdin')
args = parser.parse_args()

# Supplying a title implies HTML output
if args.title:
    args.html = True
if args.html:
    html_start = f"<html><head><title>{args.title}</title></head><body><pre>"
    html_end = "</pre></body></html>"
else:
    html_start = ""
    html_end = ""


def line_worker(single_line):
    pattern = r"(\x1b\[0m)?\x1b\[([0-9]{1,2});?([0-9]{1,2})?m(.*)?\x1b\[[0-9]{1,2}(;[0-9]{1,2})?m"
    matches = re.findall(pattern, single_line)

    if args.debug:
        print(matches)

    for match in matches:
        foreground = int(match[1]) if match[1] else None
        background = int(match[2]) if match[2] else None

        if foreground in ansi_codes:
            foreground = ansi_codes[foreground]
        elif foreground:
            if args.debug:
                print(f"Error: Unknown ANSI code {foreground}")
            foreground = None

        if background in ansi_codes:
            background = ansi_codes[background]
        elif background:
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
            source = f
    except FileNotFoundError:
        print(f"Error: File {full_path} not found.")
    except PermissionError:
        print(f"Error: Permission denied to read file {full_path}.")
else:
    source = sys.stdin

# Output
print(html_start) if args.html else None
for line in source:
    line_worker(line)
print(html_end) if args.html else None
