#!/usr/bin/python3
"""
markdown2html.py - Converts Markdown to HTML
"""

import sys
import os
import re
import hashlib

def md5(content):
    """Returns the MD5 hash of the given content."""
    return hashlib.md5(content.encode()).hexdigest()

def custom_replace(line):
    """Performs custom replacements on the given line."""
    line = re.sub(r'\[\[(.+?)\]\]',
                  lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)
    line = re.sub(r'\(\((.+?)\)\)',
                  lambda m: re.sub(r'[cC]', '', m.group(1)), line)
    return line

def convert_markdown_to_html(markdown_file, html_file):
    """Converts the given Markdown file to an HTML file."""
    with open(markdown_file, 'r') as md:
        lines = md.readlines()

    with open(html_file, 'w') as html:
        in_ul_list = False
        in_ol_list = False
        in_paragraph = False
        for line in lines:
            line = line.strip()
            line = custom_replace(line)
            line = line.replace('**', '<b>').replace('__', '<em>')
            line = line.replace('<b>', '</b>', 1).replace('<em>', '</em>', 1)
            if line.startswith('#'):
                if in_ul_list:
                    html.write('</ul>\n')
                    in_ul_list = False
                if in_ol_list:
                    html.write('</ol>\n')
                    in_ol_list = False
                if in_paragraph:
                    html.write('</p>\n')
                    in_paragraph = False
                level = len(line.split(' ')[0])
                content = ' '.join(line.split(' ')[1:])
                html.write(f'<h{level}>{content}</h{level}>\n')
            elif line.startswith('-'):
                if in_ol_list:
                    html.write('</ol>\n')
                    in_ol_list = False
                if not in_ul_list:
                    if in_paragraph:
                        html.write('</p>\n')
                        in_paragraph = False
                    html.write('<ul>\n')
                    in_ul_list = True
                content = line[1:].strip()
                html.write(f'<li>{content}</li>\n')
            elif line.startswith('*'):
                if in_ul_list:
                    html.write('</ul>\n')
                    in_ul_list = False
                if not in_ol_list:
                    if in_paragraph:
                        html.write('</p>\n')
                        in_paragraph = False
                    html.write('<ol>\n')
                    in_ol_list = True
                content = line[1:].strip()
                html.write(f'<li>{content}</li>\n')
            else:
                if in_ul_list:
                    html.write('</ul>\n')
                    in_ul_list = False
                if in_ol_list:
                    html.write('</ol>\n')
                    in_ol_list = False
                if line == '':
                    if in_paragraph:
                        html.write('</p>\n')
                        in_paragraph = False
                else:
                    if not in_paragraph:
                        html.write('<p>\n')
                        in_paragraph = True
                    html.write(f'{line}<br/>\n')
        if in_ul_list:
            html.write('</ul>\n')
        if in_ol_list:
            html.write('</ol>\n')
        if in_paragraph:
            html.write('</p>\n')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)
    markdown_file = sys.argv[1]
    html_file = sys.argv[2]
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        exit(1)
    convert_markdown_to_html(markdown_file, html_file)
    exit(0)
