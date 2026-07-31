"""Figure 3: L2 Pharmacokinetics — Grouped bar chart of key PK parameters"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

drugs = ['Ibuprofen', 'Diclofenac', 'Celecoxib', 'Paracetamol']
n = len(drugs)
x = np.arange(n)
width = 0.18

# Normalized PK parameters for comparison
# Bioavailability (%)
bioav = [100, 65, 80, 80]
# Half-life plasma (hours) - cap at 12 for scale
halflife = [1.8, 1.2, 10.0, 2.0]
# Volume of distribution (L/kg) - cap at 6
vd = [0.1, 1.4, 5.5, 0.9]
# Protein binding (%)
protbind = [99, 99, 97, 20]

fig, ax = plt.subplots(figsize=(9, 5.5))

colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52']

bars1 = ax.bar(x - 1.5*width, bioav, width, label='Bioavailability (%)', color=colors[0], edgecolor='white')
bars2 = ax.bar(x - 0.5*width, halflife, width, label='Half-life plasma (h)', color=colors[1], edgecolor='white')
bars3 = ax.bar(x + 0.5*width, vd, width, label='Vd (L/kg × 10 for scale)', color=colors[2], edgecolor='white')
bars4 = ax.bar(x + 1.5*width, protbind, width, label='Protein binding (%)', color=colors[3], edgecolor='white')

ax.set_ylabel('Value (normalized scale)', fontsize=11)
ax.set_title('L2 — Pharmacokinetic Parameters', fontsize=14, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(drugs, fontsize=11)
ax.legend(fontsize=9, loc='upper right')
ax.set_ylim(0, 115)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add value labels on bars
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
            f'{bar.get_height():.0f}', ha='center', va='bottom', fontsize=7, fontweight='bold')
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
            f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=7, fontweight='bold')
for bar in bars3:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
            f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=7, fontweight='bold')
for bar in bars4:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
            f'{bar.get_height():.0f}', ha='center', va='bottom', fontsize=7, fontweight='bold')

plt.tight_layout()
plt.savefig('C:\\Users\\think\\Project\\drug-quantification-framework\\figures\\figure3_pk_comparison.png', dpi=300)
print(f"[OK] Figure 3 saved")
