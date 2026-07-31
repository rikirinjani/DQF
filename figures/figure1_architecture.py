"""Figure 1: DQF Architecture — 4 levels with causal flow"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

# Define levels
levels = [
    {'name': 'L1 — Molecular Binding', 'y': 6.5, 'color': '#4C72B0',
     'items': ['COX-1/COX-2 Ki', 'Off-target receptors', 'Active metabolites', 'Selectivity ratios'],
     'sources': 'PDSP Ki database\nLiterature (PubMed RAG)'},
    {'name': 'L2 — Pharmacokinetics', 'y': 5.0, 'color': '#DD8452',
     'items': ['Bioavailability', 'Half-life (plasma/tissue)', 'Volume of distribution', 'Metabolism (CYP, conjug.)'],
     'sources': 'Inxight FRDB\nDrugBank\nPopPK studies'},
    {'name': 'L3 — Systems Response', 'y': 3.2, 'color': '#55A868',
     'items': ['COX inhibition dynamics', 'Tissue penetration', 'Downstream signaling', 'Off-target pathway effects'],
     'sources': 'Literature (PubMed RAG)\nMechanistic studies\nNo structured DB'},
    {'name': 'L4 — Clinical Outcomes', 'y': 1.5, 'color': '#C44E52',
     'items': ['NNT (≥50% pain relief)', 'NNH (GI/CV events)', 'Condition-specific outcomes', 'Dose-response'],
     'sources': 'Cochrane reviews\nOxford League Table\nRCTs'},
]

# Draw level boxes
for level in levels:
    # Main box
    box = mpatches.FancyBboxPatch((0.8, level['y'] - 0.5), 5.5, 0.9,
                                   boxstyle="round,pad=0.1",
                                   facecolor=level['color'], edgecolor='white', alpha=0.9)
    ax.add_patch(box)
    ax.text(1.0, level['y'] + 0.15, level['name'], fontsize=12, fontweight='bold', color='white',
            verticalalignment='center')

    # Items on the right
    for j, item in enumerate(level['items']):
        ax.text(6.5, level['y'] - 0.25 + j*0.08, f"— {item}", fontsize=7, color='#333333',
                verticalalignment='center')

    # Sources on the far right
    ax.text(8.5, level['y'], level['sources'], fontsize=6, color='#666666',
            verticalalignment='center', horizontalalignment='left',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#f5f5f5', edgecolor='#dddddd', alpha=0.8))

# Draw causal arrows between levels
for i in range(len(levels) - 1):
    y_center = (levels[i]['y'] - 0.05 + levels[i+1]['y'] + 0.55) / 2
    ax.annotate('', xy=(3.5, levels[i+1]['y'] + 0.55), xytext=(3.5, levels[i]['y'] - 0.05),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=2.5, connectionstyle='arc3,rad=0'))

# Left side annotation — L2 arrow modifier
ax.annotate('L2 modulates L1→L3\ntranslation',
            xy=(0.3, 4.2), fontsize=7.5, color='#DD8452', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='#DD8452', alpha=0.9),
            horizontalalignment='center')

ax.set_title('Drug Quantification Framework — 4-Level Architecture', fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('C:\\Users\\think\\Project\\drug-quantification-framework\\figures\\figure1_architecture.png', dpi=300)
print("[OK] Figure 1 saved")
