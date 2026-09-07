import re

with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the entire staticBlog div (with all its hardcoded cards) and replace with empty dynamicBlog
pattern = re.compile(
    r'<div id="staticBlog" class="grid-3 reveal">.*?</div>\s*\n(\s*<div id="dynamicBlog")',
    re.DOTALL
)

replacement = r'<div id="dynamicBlog" class="grid-3 reveal"></div>\n'

new_content, count = re.subn(pattern, replacement, content)

if count:
    print(f'Replaced {count} staticBlog block(s) successfully!')
    with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
else:
    print('Pattern not found - checking manually...')
    idx = new_content.find('staticBlog')
    print('staticBlog still present:', idx != -1)
