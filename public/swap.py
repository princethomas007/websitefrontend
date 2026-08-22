import os

filepath = r"c:\Users\sumes\Downloads\rextech_studios_clean\rextech_clean\portfolio.html"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

offerings_start = -1
offerings_end = -1
projects_start = -1
projects_end = -1

for i, line in enumerate(lines):
    if '<!-- Category overview' in line:
        offerings_start = i
    if '<!-- Projects -->' in line:
        projects_start = i
        offerings_end = i - 1
    if '<section class="section-sm"' in line:
        projects_end = i - 2

# Actually based on view_file output:
# offerings chunk starts at 262 and goes to 346
# projects chunk starts at 348 and goes to 395
# let's find the exact indices
for i, line in enumerate(lines):
    if '<!-- Category overview' in line:
        idx_offer_start = i
    if '<!-- Projects -->' in line:
        idx_proj_start = i

idx_offer_end = idx_proj_start - 1

idx_proj_end = -1
for i in range(idx_proj_start, len(lines)):
    if '</div>' in lines[i] and '</div>' in lines[i-1] and '</div>' in lines[i-2] and '<!-- CTA' not in lines[i] and '<section' in lines[i+2]:
        pass
    if '<section class="section-sm"' in lines[i]:
        idx_proj_end = i - 2
        break

chunk_offer = lines[idx_offer_start:idx_offer_end]
chunk_proj = lines[idx_proj_start:idx_proj_end+1]

# Reassemble
new_lines = lines[:idx_offer_start] + chunk_proj + ['\n', '      <br><br>\n'] + chunk_offer + lines[idx_proj_end+1:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Swapped sections. offer_start={idx_offer_start} proj_start={idx_proj_start} proj_end={idx_proj_end}")
