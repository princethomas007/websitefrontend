# -*- coding: utf-8 -*-
import re

with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken href
old_str = '<a href="blog-post.html?id=" class="blog-read" style="text-decoration:none; color:inherit;">Read more \n&rarr;</a>'
# Let's use regex in case of formatting differences
content = re.sub(
    r'<a href="blog-post.html\?id=" class="blog-read"[^>]*>Read more\s*&rarr;</a>',
    '<a href="blog-post.html?id=${blog.id}" class="blog-read" style="text-decoration:none; color:inherit;">Read more &rarr;</a>',
    content
)

with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog.html', 'w', encoding='utf-8') as f:
    f.write(content)
