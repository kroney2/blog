#!/bin/python3
import os
import posixpath

####
# Takes MD line, returns eqv HTML
##
def MDToHTML(md_line):
    out = ''
    prevc = ''
    non_md_so = hash_count = 0
    title_so = title_eo = alt_so = alt_eo = src_so = src_eo = 0
    is_paragraph = is_heading = is_img = is_break = False
    for index, c in enumerate(md_line):
        # Break
        if c == '\n' and index == 0:
            is_break = True

        # Header
        elif (not index and c == '#'):
            is_heading = True

        # Img
        elif (not index and c == '!'):
            is_img = True

        # Paragraph
        elif (not index and c != '#'):
            is_paragraph = True
            non_md_so = 0

        if is_heading:
            if c == '#':
                hash_count += 1
            elif c == ' ' and prevc == '#':
                non_md_so = index + 1
        if (is_img):
            if c == '[':
                alt_so = index + 1
            if c == ']':
                alt_eo = index
            if c == '(':
                src_so = index + 1
            if c == ' ' and not title_so:
                src_eo = index
            if c == '"' and not title_so:
                title_so = index
            elif c == '"' and title_so:
                title_eo = index + 1
        prevc = c

    if (is_heading):
        hlevel = str(hash_count)
        out = '<h' + hlevel + '>' + md_line[non_md_so:-1] + '</h' + hlevel + '>\n'
    elif (is_img):
        out = '<img title=' + md_line[title_so:title_eo] +  ' alt="' + md_line[alt_so:alt_eo] + '" src="' + md_line[src_so:src_eo] + '">\n'
    elif (is_paragraph):
        out = '<p>' + md_line[non_md_so:-1] + '</p>\n'
    elif (is_break):
        out = '<br>'
    else:
        assert(0)
    return out

def InsertLatestPost(LatestPostPath, IndexHTMLStr, nLatestLines):
    PostHTML = "<h2>Latest Post</h2>\n"
    with open(os.path.join(POSTS_DIR, PostMDBaseName), 'r') as PostMDFile:
        for LineIndex, Line in enumerate(PostMDFile.readlines()):
            PostHTML += MDToHTML(Line)

    for CharacterIndex, Character in enumerate(IndexHTMLStr):
        EO = CharacterIndex + len("latest\">")
        if (IndexHTMLStr[CharacterIndex : EO] == "latest\">"):
            IndexHTMLStr = IndexHTMLStr[:EO] + PostHTML + IndexHTMLStr[EO:]
            break
    return IndexHTMLStr
####
# Naively generate HTML source from MD
##
RAW_HTML_SHARED_FH ='''
<!doctype html>
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
        </div>
        '''
RAW_HTML_SHARED_SH ='''
</body>
</html>'''

RAW_INDEX_ONLY = '''
<div id="latest">
</div>
<h2>Posts</h2>
<div id="posts">
</div>
'''

POSTS_DIR = 'posts/'
PUBLIC_DIR = 'public/'
IndexHTMLStr = RAW_HTML_SHARED_FH + RAW_INDEX_ONLY
LatestPost = None;
for PostMDBaseName in os.listdir(POSTS_DIR):
    with open(os.path.join(POSTS_DIR, PostMDBaseName), 'r') as PostMDFile:
        PostHTMLBaseName = os.path.splitext(PostMDBaseName)[0] + '.html'
        PostHTMLPath = os.path.join(PUBLIC_DIR, PostHTMLBaseName)
        with open(PostHTMLPath, 'w') as PostHTMLFile:
            PostHTMLFile.write(RAW_HTML_SHARED_FH)
            for Line in PostMDFile.readlines():
                PostHTMLFile.write(MDToHTML(Line))
            PostHTMLFile.write(RAW_HTML_SHARED_SH)
    IndexHTMLStr += '<a href="' + PostHTMLBaseName + '">' + PostHTMLBaseName.split('_')[0] + '</a>\n'
    if (not LatestPost or int(posixpath.splitext(PostMDBaseName.split('_')[1])[0]) > int(posixpath.splitext(LatestPost.split('_')[1])[0])):
        LatestPost = PostMDBaseName
        print(LatestPost)
IndexHTMLStr += RAW_HTML_SHARED_SH
IndexHTMLStr = InsertLatestPost(os.path.join(POSTS_DIR, LatestPost), IndexHTMLStr, 5);

with open(os.path.join(PUBLIC_DIR, 'index.html'), 'w') as IndexHTMLFile:
    IndexHTMLFile.write(IndexHTMLStr)
