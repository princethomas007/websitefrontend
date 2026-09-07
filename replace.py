import re

with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the static grid block with just the dynamic container
pattern_grid = re.compile(r'<div class="grid-3 reveal">.*?</div>\s*</div>\s*</div>\s*</section>', re.DOTALL)
replacement_grid = '''<div id="dynamicBlog" class="grid-3 reveal"></div>
            </div>
        </div>
    </section>'''
content = pattern_grid.sub(replacement_grid, content, count=1)

# 2. Remove the old dynamic section
pattern_old_dynamic = re.compile(r'<section class="section" style="background: var\(--black\);">\s*<div style="max-width:1200px;margin:auto;">\s*<div id="dynamicBlog" class="grid-3"></div>\s*</div>\s*</section>', re.DOTALL)
content = pattern_old_dynamic.sub('', content, count=1)

with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done replacing.")
