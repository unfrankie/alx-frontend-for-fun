#!/usr/bin/python3
"""
Script to convert Markdown to HTML
"""
import sys
import os
import hashlib
import re


def parse_headings(line):
    """
    Parse Markdown headings to HTML
    """
    for i in range(6, 0, -1):
        if line.startswith('#' * i):
            return f"<h{i}>{line[i:].strip()}</h{i}>"
    return None


def parse_unordered_list(lines, index):
    """
    Parse Markdown unordered list to HTML
    """
    html = ["<ul>"]
    while index < len(lines) and lines[index].startswith('- '):
        item = lines[index][2:].strip()
        html.append(f"<li>{item}</li>")
        index += 1
    html.append("</ul>")
    return '\n'.join(html), index


def parse_ordered_list(lines, index):
    """
    Parse Markdown ordered list to HTML
    """
    html = ["<ol>"]
    while index < len(lines) and lines[index].startswith('* '):
        item = lines[index][2:].strip()
        html.append(f"<li>{item}</li>")
        index += 1
    html.append("</ol>")
    return '\n'.join(html), index


def parse_paragraph(lines, index):
    """
    Parse Markdown paragraphs to HTML
    """
    html = ["<p>"]
    while index < len(lines) and not lines[index].startswith(('#', '-', '*')):
        line = lines[index].strip()
        if line:
            html.append(line)
            if index + 1 < len(lines) and not lines[index + 1].startswith(
             ('#', '-', '*')
             ):
                html.append("<br/>")
        index += 1
    html.append("</p>")
    return '\n'.join(html), index


def parse_bold_and_emphasis(line):
    """
    Parse Markdown bold and emphasis to HTML
    """
    line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
    line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)
    return line


def parse_special_syntax(line):
    """
    Parse special Markdown syntax to HTML
    """
    line = re.sub(r'\[\[(.+?)\]\]',
                  lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)
    line = re.sub(r'\(\((.+?)\)\)',
                  lambda m: re.sub(r'[cC]', '', m.group(1)), line)
    return line


def markdown_to_html(markdown_file, html_file):
    """
    Convert Markdown file to HTML file
    """
    with open(markdown_file, 'r') as md_file:
        lines = md_file.readlines()

    html_lines = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if heading := parse_headings(line):
            html_lines.append(heading)
        elif line.startswith('- '):
            ul_html, index = parse_unordered_list(lines, index)
            html_lines.append(ul_html)
            continue
        elif line.startswith('* '):
            ol_html, index = parse_ordered_list(lines, index)
            html_lines.append(ol_html)
            continue
        else:
            paragraph_html, index = parse_paragraph(lines, index)
            html_lines.append(paragraph_html)
            continue
        index += 1

    html_content = '\n'.join(html_lines)
    html_content = parse_bold_and_emphasis(html_content)
    html_content = parse_special_syntax(html_content)

    with open(html_file, 'w') as html_file:
        html_file.write(html_content)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    markdown_to_html(markdown_file, html_file)
    sys.exit(0)
