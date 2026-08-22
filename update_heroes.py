import os
import re
from bs4 import BeautifulSoup, NavigableString

public_dir = r"c:\Rextech new website\Rextech_studios_website\rextech_studios_clean\rextech_clean\public"

def split_to_spans(text, start_delay, word_class):
    words = text.split()
    html = ""
    for i, w in enumerate(words):
        d = start_delay + i * 0.05
        html += f'<span class="{word_class}" style="animation-delay: {d:.2f}s;">{w}</span>\n'
    return html

for filename in os.listdir(public_dir):
    if not filename.endswith('.html'):
        continue
    
    filepath = os.path.join(public_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    changed = False

    # Find hero section
    hero_section = None
    for klass in ['hero', 'page-hero', 'contact-page-hero', 'ar-hero']:
        section = soup.find(class_=klass)
        if section:
            hero_section = section
            break
            
    if hero_section:
        # Find h1
        h1 = hero_section.find('h1')
        if h1 and 'hero-custom-title' not in h1.get('class', []):
            h1['class'] = h1.get('class', []) + ['hero-custom-title']
            h1['style'] = "opacity:1 !important; transform:none !important; filter:none !important; animation:none !important;"
            
            # extract text, handle <br>
            text_lines = []
            for child in h1.children:
                if isinstance(child, NavigableString):
                    if child.strip():
                        text_lines.append(child.strip())
                elif child.name == 'br':
                    pass # We will reconstruct
            
            if not text_lines:
                text_lines = [h1.get_text().strip()]

            h1.clear()
            
            current_delay = 1.30
            for i, line in enumerate(text_lines):
                line_words = line.split()
                for w in line_words:
                    span = soup.new_tag("span")
                    span['class'] = "hero-word"
                    span['style'] = f"animation-delay: {current_delay:.2f}s;"
                    span.string = w
                    h1.append(span)
                    h1.append(" ")
                    current_delay += 0.05
                if i < len(text_lines) - 1:
                    h1.append(soup.new_tag("br"))

            changed = True

        # Find sub
        sub = hero_section.find(class_=re.compile(r'hero-sub|sub'))
        # make sure it is a p tag or div inside hero-content
        if not sub:
            # fallback
            hc = hero_section.find(class_='hero-content')
            if hc:
                sub = hc.find('p')
                
        if sub and 'hero-custom-sub' not in sub.get('class', []):
            sub['class'] = sub.get('class', []) + ['hero-custom-sub']
            sub['style'] = "opacity:1 !important; transform:none !important; filter:none !important; animation:none !important; margin-bottom: 30px;"
            
            # preserve br if any, else break roughly by sentence
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
            
        # Find ctas
        ctas = hero_section.find(class_=re.compile(r'hero-ctas|ctas|btn-beam-wrap'))
        if ctas and 'hero-custom-ctas' not in ctas.get('class', []):
            ctas['class'] = ctas.get('class', []) + ['hero-custom-ctas']
            # Button delay based on end of sub animation.
            # Usually end is around current_delay + 0.3s
            btn_delay = current_delay + 0.3
            if btn_delay < 2.0: btn_delay = 2.75 # fallback for short texts
            ctas['style'] = f"animation-delay: {btn_delay:.2f}s;"
            changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated {filename}")

css_to_append = """
/* Cinematic Text Animations */
@keyframes blurRevealCustom {
  0% {
    opacity: 0;
    filter: blur(12px);
    transform: translateY(30px) scale(0.95);
  }
  100% {
    opacity: 1;
    filter: blur(0);
    transform: translateY(0) scale(1);
  }
}

@keyframes fadeUpBtn {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-custom-title .hero-word {
  display: inline-block;
  opacity: 0;
  animation: blurRevealCustom 1.1s cubic-bezier(0.2, 0.9, 0.2, 1) forwards;
  margin-right: 0.25em;
}

.hero-custom-sub .hero-sub-word {
  display: inline-block;
  opacity: 0;
  animation: blurRevealCustom 1.1s cubic-bezier(0.2, 0.9, 0.2, 1) forwards;
  margin-right: 0.25em;
}

.hero-custom-ctas {
  opacity: 0;
  animation: fadeUpBtn 1s cubic-bezier(0.2, 0.9, 0.2, 1) forwards;
}
"""

style_path = os.path.join(public_dir, "assets", "style.css")
with open(style_path, 'r', encoding='utf-8') as f:
    existing_css = f.read()

if "blurRevealCustom" not in existing_css:
    with open(style_path, 'a', encoding='utf-8') as f:
        f.write(css_to_append)
    print("Appended CSS to style.css")
else:
    print("CSS already appended")
