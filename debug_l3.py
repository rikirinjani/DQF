"""Debug L3 page positioning"""
import re

path = r'C:\Users\think\Project\drug-quantification-framework\build_pdf_fpdf.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Insert debug prints after key points in L3 section
insertions = [
    ("    pdf.section_title('5. L3 - Systems Response')",
     "    pdf.section_title('5. L3 - Systems Response')\n"
     "    print(f'  [DBG] After section_title: Y={pdf.get_y():.1f}')"),
    ("pdf.cell(0, 5, 'Key findings (circularity identified):', new_x=XPos.LMARGIN, new_y=YPos.NEXT)",
     "print(f'  [DBG] Before label: Y={pdf.get_y():.1f}')\n"
     "    pdf.cell(0, 5, 'Key findings (circularity identified):', new_x=XPos.LMARGIN, new_y=YPos.NEXT)"),
    ("    for item in compact_bullets:",
     "    for item in compact_bullets:\n"
     "        print(f'  [DBG] Bullet start Y={pdf.get_y():.1f}, item={item[:40]}...')"),
    ("    pdf.ln(4)",
     "    print(f'  [DBG] After bullets: Y={pdf.get_y():.1f}')\n"
     "    pdf.ln(4)\n"
     "    print(f'  [DBG] After ln(4): Y={pdf.get_y():.1f}')\n"
     "    print(f'  [DBG] Page no: {pdf.page_no()}')"),
]

for old, new in insertions:
    if old in content:
        content = content.replace(old, new)
    else:
        print(f'WARNING: pattern not found:\n  {old[:80]}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched with debug')
