"""Figure 2: L1 Binding Profile Heatmap — 4 drugs × 9 targets
   Annotated with evidence confidence markers for LOW/VERY LOW evidence cells.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

drugs = ['Ibuprofen', 'Diclofenac', 'Celecoxib', 'Paracetamol\n(AM404)']
targets = ['COX-1', 'COX-2', 'P2X3', 'TRPV1', 'ASIC1a',
           'Nav1.8', 'CB1', 'PPARγ', 'COX-2 sel.']

# Binding strength (-log₁₀ M): 0 = no activity, higher = stronger
data = np.array([
    [8.0, 8.3, 6.3, 2.0],   # COX-1
    [6.7, 8.3, 8.3, 5.3],   # COX-2
    [0.0, 3.9, 0.0, 0.0],   # P2X3
    [5.2, 4.7, 0.0, 6.0],   # TRPV1
    [5.0, 0.0, 0.0, 0.0],   # ASIC1a
    [0.0, 0.0, 0.0, 7.0],   # Nav1.8
    [0.0, 0.0, 0.0, 5.0],   # CB1
    [4.0, 0.0, 0.0, 0.0],   # PPARγ
    [1.0, 0.0, 8.0, 0.0],   # COX-2 selectivity
])

# Evidence confidence: 0=HIGH, 1=MODERATE, 2=LOW, 3=VERY LOW
evidence = np.array([
    [0, 0, 0, 1],   # COX-1
    [0, 0, 0, 1],   # COX-2
    [3, 2, 3, 3],   # P2X3
    [1, 2, 3, 1],   # TRPV1
    [2, 3, 3, 3],   # ASIC1a
    [3, 3, 3, 1],   # Nav1.8
    [3, 3, 3, 2],   # CB1
    [2, 3, 3, 3],   # PPARγ
    [1, 3, 0, 3],   # COX-2 selectivity
])

# Build annotation matrix with confidence markers
annot_data = np.full(data.shape, '', dtype=object)
for r in range(data.shape[0]):
    for c in range(data.shape[1]):
        if data[r, c] == 0:
            annot_data[r, c] = '0'
        else:
            s = f"{data[r, c]:.1f}"
            if evidence[r, c] >= 2:
                s += "†"  # LOW/VERY LOW evidence
            annot_data[r, c] = s

fig, ax = plt.subplots(figsize=(8, 7))
cmap = sns.color_palette("YlOrRd", as_cmap=True, n_colors=12)
cmap.set_under('#f8f8f8')

sns.heatmap(data, annot=annot_data, fmt='', xticklabels=drugs, yticklabels=targets,
            cmap=cmap, vmin=1.0, vmax=9.0, linewidths=0.8, linecolor='white',
            cbar_kws={'label': 'Binding Strength (−log₁₀ M)', 'shrink': 0.8},
            ax=ax)

ax.set_title('L1 — Molecular Binding Profiles', fontsize=14, fontweight='bold', pad=16)
ax.set_xlabel('')
ax.set_ylabel('Target', fontsize=11)
ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha='right', fontsize=10)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)

# Footnote
fig.text(0.5, -0.03,
    '† = LOW/VERY LOW evidence (single study, indirect, or expert opinion)',
    ha='center', va='top', fontsize=7.5, color='#555555')

plt.tight_layout()
plt.savefig('C:\\Users\\think\\Project\\drug-quantification-framework\\figures\\figure2_binding_heatmap.png', dpi=300)
print(f"[OK] Figure 2 saved")
