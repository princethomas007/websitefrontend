import re

with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the read more span with a link
old_str = '<span class="blog-read">Read more +\'</span>'
new_str = '<a href="blog-post.html?id=" class="blog-read" style="text-decoration:none; color:inherit;">Read more &rarr;</a>'

content = content.replace(old_str, new_str)

# also fallback if the unicode character is different
old_str2 = '<span class="blog-read">Read more '
content = re.sub(r'<span class="blog-read">Read more [^<]*</span>', new_str, content)

with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog.html', 'w', encoding='utf-8') as f:
    f.write(content)
