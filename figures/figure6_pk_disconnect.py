"""Figure 6: Plasma vs Tissue Half-Life — The PK-L3 Disconnect"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

drugs = ['Ibuprofen', 'Diclofenac', 'Celecoxib', 'Paracetamol']
plasma_t12 = [1.8, 1.2, 10.0, 2.0]
tissue_t12 = [4.5, 10.0, 12.0, 2.0]  # synovial fluid half-life
dosing_interval = [6, 12, 24, 6]  # typical dosing interval (hours)

x = np.arange(len(drugs))
width = 0.25

fig, ax = plt.subplots(figsize=(8, 5))

bars1 = ax.bar(x - width, plasma_t12, width, label='Plasma t½', color='#4C72B0', edgecolor='white')
bars2 = ax.bar(x, tissue_t12, width, label='Synovial fluid t½', color='#DD8452', edgecolor='white')
bars3 = ax.bar(x + width, dosing_interval, width, label='Typical dosing interval', color='#8E8E8E', edgecolor='white')

ax.set_ylabel('Time (hours)', fontsize=11)
ax.set_title('L2→L3 — Plasma vs. Tissue Half-Life: The PK Disconnect', fontsize=12, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(drugs, fontsize=11)
ax.legend(fontsize=9)
ax.set_ylim(0, 28)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add annotation arrow for diclofenac disconnect
ax.annotate('1.2 h plasma →\n10 h synovial',
            xy=(1, 10.0), xytext=(1.8, 18),
            arrowprops=dict(arrowstyle='->', color='#DD8452', lw=1.5),
            fontsize=8, color='#DD8452', fontweight='bold')

# Add value labels
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2., h + 0.3,
                    f'{h:.1f}', ha='center', va='bottom', fontsize=7.5)

plt.tight_layout()
plt.savefig('C:\\Users\\think\\Project\\drug-quantification-framework\\figures\\figure6_pk_disconnect.png', dpi=300)
print(f"[OK] Figure 6 saved")
