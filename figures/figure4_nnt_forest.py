"""Figure 4: L4 NNT Forest Plot — NNT with 95% confidence intervals"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# NNT data: label, NNT, lower_CI, upper_CI
data = [
    ('Ibuprofen 400 mg\n(fast-acting)', 2.1, 1.9, 2.3),
    ('Ibuprofen 400 mg', 2.5, 2.4, 2.6),
    ('Ibuprofen 200 mg', 2.7, 2.5, 3.0),
    ('Diclofenac K 50 mg\n(fast-acting)', 2.1, 1.9, 2.5),
    ('Diclofenac 50 mg', 2.7, 2.4, 3.0),
    ('Celecoxib 400 mg', 2.5, 2.2, 2.9),
    ('Celecoxib 200 mg', 3.0, 2.5, 3.6),
    ('Paracetamol 1000 mg', 3.6, 3.2, 4.1),
    ('Paracetamol 500 mg', 3.5, 2.7, 4.8),
]

# Color by drug
colors = {'Ibuprofen': '#4C72B0', 'Diclofenac': '#DD8452',
          'Celecoxib': '#55A868', 'Paracetamol': '#C44E52'}

fig, ax = plt.subplots(figsize=(8, 6))

drug_colors = []
labels = []
for label, _, _, _ in data:
    if 'Ibuprofen' in label:
        drug_colors.append(colors['Ibuprofen'])
    elif 'Diclofenac' in label:
        drug_colors.append(colors['Diclofenac'])
    elif 'Celecoxib' in label:
        drug_colors.append(colors['Celecoxib'])
    else:
        drug_colors.append(colors['Paracetamol'])
    labels.append(label)

y_pos = np.arange(len(data))

# Plot points with error bars (forest plot style)
for i, (label, nnt, lo, hi) in enumerate(data):
    ax.errorbar(nnt, i, xerr=[[nnt-lo], [hi-nnt]], fmt='o', color=drug_colors[i],
                capsize=4, capthick=1.5, markersize=9, linewidth=1.5)
    ax.plot(nnt, i, 'o', color=drug_colors[i], markersize=9, markeredgecolor='white', markeredgewidth=0.5)

# Reference line at NNT = 2.0
ax.axvline(x=2.0, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.text(2.02, len(data)-0.3, 'NNT = 2.0 (excellent)', fontsize=8, color='gray', fontstyle='italic')

# Reference line at NNT = 4.0
ax.axvline(x=4.0, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.text(4.02, len(data)-0.3, 'NNT = 4.0 (moderate)', fontsize=8, color='gray', fontstyle='italic')

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=9)
ax.set_xlabel('NNT (95% CI) — Number Needed to Treat', fontsize=11)
ax.set_title('L4 — Clinical Efficacy: NNT for ≥50% Pain Relief (Acute Pain)', fontsize=12, fontweight='bold', pad=12)
ax.invert_yaxis()
ax.set_xlim(1.0, 6.0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Custom legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors['Ibuprofen'], label='Ibuprofen'),
                   Patch(facecolor=colors['Diclofenac'], label='Diclofenac'),
                   Patch(facecolor=colors['Celecoxib'], label='Celecoxib'),
                   Patch(facecolor=colors['Paracetamol'], label='Paracetamol')]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9, title='Drug', title_fontsize=10)

plt.tight_layout()
plt.savefig('C:\\Users\\think\\Project\\drug-quantification-framework\\figures\\figure4_nnt_forest.png', dpi=300)
print(f"[OK] Figure 4 saved")
