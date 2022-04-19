#!/bin/python3
import os

####
# Takes MD line, returns eqv HTML
##
def md_to_html(md_line):
    out = ''
    if md_line == '\n':
        return out

    prevc = ''
    non_md_so = hash_count = 0
    is_paragraph = is_heading = False
    for index, c in enumerate(md_line):
        # Header
        if (not index and c == '#'):
            is_heading = True
        # Paragraph
        elif (not index and c != '#'):
            is_paragraph = True
            non_md_so = 0

        if is_heading:
            if c == '#':
                hash_count += 1
            elif c == ' ' and prevc == '#':
                non_md_so = index + 1
        elif c == '\n':
            break
        prevc = c

    if (is_heading):
        hlevel = str(hash_count)
        out = '<h' + hlevel + '>' + md_line[non_md_so:-1] + '</h' + hlevel + '>\n'
    elif (is_paragraph):
        out = '<p>' + md_line[non_md_so:-1] + '</p>\n'
    else:
        assert(0)
    return out

####
# Naively generate HTML source from MD
##
RAW_HTML_SHARED_FH = '''<!doctype html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kroney's Blog</title>
        <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/hack-font@3/build/web/hack-subset.css"/>
        <link rel="stylesheet" href="style.css"/>
    </head>
    <body>
        <div class="navbar">
            <a href="index.html">home</a>
        </div>'''
RAW_HTML_SHARED_SH = '''</body>
</html>'''
POSTS_DIR = 'posts/'
PUBLIC_DIR = 'public/'
with open(os.path.join(PUBLIC_DIR, 'index.html'), 'w') as index_htmlf:
    index_htmlf.write(RAW_HTML_SHARED_FH)
    for index, entry in enumerate(os.listdir(POSTS_DIR)):
        with open(os.path.join(POSTS_DIR, entry), 'r') as posting_mdf:
            base_name = os.path.splitext(entry)[0] + '.html'
            out_path = os.path.join(PUBLIC_DIR, base_name)
            with open(out_path, 'w') as posting_htmlf:
                posting_htmlf.write(RAW_HTML_SHARED_FH)
                for line in posting_mdf.readlines():
                    posting_htmlf.write(md_to_html(line))
                posting_htmlf.write(RAW_HTML_SHARED_SH)
        index_htmlf.write('<a href="' + base_name + '">' + base_name.split('_')[0] + '</a>\n')
    index_htmlf.write(RAW_HTML_SHARED_SH)
