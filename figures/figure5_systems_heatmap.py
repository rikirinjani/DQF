"""Figure 5: L3 Systems Response — Qualitative comparison heatmap
   Annotated: predicted/derived vs independent, with evidence confidence markers.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle

drugs = ['Ibuprofen', 'Diclofenac', 'Celecoxib', 'Paracetamol']

responses = ['COX inhibition potency',
             'Anti-inflammatory',
             'GI prostaglandin sparing',
             'Platelet function preserved',
             'Endothelial PGI₂ sparing',
             'Off-target analgesia',
             'Synovial fluid duration',
             'Therapeutic window']

# Short labels for y-axis
short_labels = ['COX potency', 'Anti-inflam.', 'GI sparing', 'Platelet fn.',
                'PGI₂ sparing', 'Off-target', 'Synovial dur.', 'Ther. window']

# Score: 0 = none/absent, 1 = minimal, 2 = moderate, 3 = strong
data = np.array([
    [2, 3, 1, 0],   # COX inhibition potency
    [2, 3, 2, 0],   # Anti-inflammatory
    [0, 0, 2, 3],   # GI prostaglandin sparing
    [0, 0, 3, 3],   # Platelet preserved
    [0, 0, 0, 3],   # Endothelial PGI2 sparing
    [2, 2, 0, 3],   # Off-target analgesia
    [1, 3, 3, 0],   # Synovial duration (PK-L3 hybrid)
    [3, 3, 3, 1],   # Therapeutic window safety
])

# --- Circularity annotation: which rows are L1→L3 predicted? ---
# True = this row is predicted/consequence of L1, not an independent L3 finding
l1_predicted_rows = [True, True, True, True, True, False, False, False]
row_colors = ['#FFD966' if p else '#A9D18E' for p in l1_predicted_rows]

# --- Confidence overlay for LOW/VERY LOW evidence cells ---
# Matrix of evidence levels: 0=HIGH, 1=MODERATE, 2=LOW, 3=VERY LOW
evidence = np.array([
    [1, 0, 1, 3],   # COX potency
    [1, 1, 1, 3],   # Anti-inflam
    [2, 2, 2, 2],   # GI sparing
    [2, 2, 2, 2],   # Platelet
    [2, 2, 2, 2],   # PGI2
    [1, 2, 3, 2],   # Off-target
    [1, 1, 1, 3],   # Synovial
    [2, 2, 2, 2],   # Ther window
])

# Build annotation matrix: add ✦ for predicted, ✧ for LOW evidence
annot_data = np.full(data.shape, '', dtype=object)
for r in range(data.shape[0]):
    for c in range(data.shape[1]):
        s = f"{data[r,c]}"
        if l1_predicted_rows[r]:
            s += "✦"  # predicted from L1
        if evidence[r, c] >= 2:
            s += "✧"  # LOW evidence
        annot_data[r, c] = s

fig, ax = plt.subplots(figsize=(8.5, 5.5))
cmap = sns.color_palette("RdYlGn", as_cmap=True, n_colors=12)

sns.heatmap(data, annot=annot_data, fmt='', xticklabels=drugs, yticklabels=short_labels,
            cmap=cmap, vmin=0, vmax=3, linewidths=1, linecolor='white',
            cbar_kws={'label': 'Score (0=none, 1=minimal, 2=moderate, 3=strong)',
                      'shrink': 0.7, 'ticks': [0, 1, 2, 3]},
            ax=ax)

# Add row-color strip on the left margin
for i, color in enumerate(row_colors):
    ax.add_patch(Rectangle(
        xy=(-0.05, i + 0.05), width=0.08, height=0.9,
        transform=ax.get_yaxis_transform(), clip_on=False,
        facecolor=color, edgecolor='gray', linewidth=0.5
    ))

ax.set_title('L3 — Systems Response Profiles', fontsize=14, fontweight='bold', pad=16)
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha='right', fontsize=10)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=9)

# Footnote
fig.text(0.5, -0.02,
    '✦ = L1→L3 predicted (derived from binding selectivity, not an independent L3 finding)\n'
    '✧ = LOW/VERY LOW evidence (single study, in vitro only, or expert opinion)',
    ha='center', va='top', fontsize=7, color='#555555')

# Legend column on the right
fig.text(0.92, 0.5,
    'Row strip:\n'
    '■ Yellow = L1→L3 predicted\n'
    '■ Green  = Independent L3',
    ha='center', va='center', fontsize=7, color='#333333',
    transform=ax.transAxes)

plt.tight_layout(rect=[0, 0.06, 0.88, 1])
plt.savefig('C:\\Users\\think\\Project\\drug-quantification-framework\\figures\\figure5_systems_heatmap.png', dpi=300)
print(f"[OK] Figure 5 saved")
