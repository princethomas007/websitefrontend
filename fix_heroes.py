import os
import re
from bs4 import BeautifulSoup, NavigableString

public_dir = r"c:\Rextech new website\Rextech_studios_website\rextech_studios_clean\rextech_clean\public"

for filename in os.listdir(public_dir):
    if not filename.endswith('.html'):
        continue
    
    filepath = os.path.join(public_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    changed = False

    # Remove premium-hero-title from all elements to stop main.js from breaking our HTML
    for el in soup.find_all(class_='premium-hero-title'):
        classes = el.get('class', [])
        if 'premium-hero-title' in classes:
            classes.remove('premium-hero-title')
            el['class'] = classes
            changed = True

    # Find hero section
    hero_section = None
    for klass in ['hero', 'page-hero', 'contact-page-hero', 'ar-hero']:
        section = soup.find(class_=klass)
        if section:
            hero_section = section
            break
            
    if hero_section:
        # Check if paragraph missed the update
        p_tags = hero_section.find_all('p')
        for sub in p_tags:
            # We want to convert this p if it hasn't been converted
            if 'hero-custom-sub' not in sub.get('class', []):
                # We need to remove reveal to stop initReveal
                classes = sub.get('class', [])
                if 'reveal' in classes: classes.remove('reveal')
                classes.append('hero-custom-sub')
                sub['class'] = classes
                sub['style'] = "opacity:1 !important; transform:none !important; filter:none !important; animation:none !important; margin-bottom: 30px;"
                
                text_lines = []
                for child in sub.children:
                    if isinstance(child, NavigableString):
                        if child.strip():
                            text_lines.append(child.strip())
                
                if not text_lines:
                    text_lines = [sub.get_text().strip()]
                    
                sub.clear()
                current_delay = 1.65
                for i, line in enumerate(text_lines):
                    line_words = line.split()
                    for w in line_words:
                        span = soup.new_tag("span")
                        span['class'] = "hero-sub-word"
                        span['style'] = f"animation-delay: {current_delay:.2f}s;"
                        span.string = w
                        sub.append(span)
                        sub.append(" ")
                        current_delay += 0.05
                    if i < len(text_lines) - 1:
                        sub.append(soup.new_tag("br"))
                        
                changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Fixed {filename}")
