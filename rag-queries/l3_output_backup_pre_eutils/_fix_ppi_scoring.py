"""
Fix PPI L3 risk scoring based on ACG guideline evidence.
Patches l3_systems.ddi_risk and l3_systems.cdi_risk in drugs.json.
"""
import json, shutil
from pathlib import Path
from datetime import datetime

DRUGS_JSON = Path(r'C:\Users\think\Project_v2\drug-quantification-framework\api\drugs.json')
BACKUP_DIR = Path(r'C:\Users\think\Project_v2\drug-quantification-framework\rag-queries\l3_output\_backups')

# Evidence-based corrected scores
# CDI risk: based on ACG 2020 OR data (Lansoprazole 4.81 > Esomeprazole 4.2 > Pantoprazole 4.15 > Omeprazole 3.24)
# DDI risk: based on CYP2C19 inhibition potency (Li 2004, FDA labeling)
CORRECTED = {
    "omeprazole": {
        "cdi_risk": 2,    # WAS 3 (inverted). ACG OR 3.24 — lowest among PPIs
        "ddi_risk": 3,    # STAYS 3. Strong CYP2C19 inhibitor, most DDIs
    },
    "esomeprazole": {
        "cdi_risk": 2,    # WAS 1 (too low). ACG OR 4.2 — substantial 4x risk
        "ddi_risk": 2,    # WAS 3. Moderate CYP2C19 inhibitor (S-isomer)
    },
    "lansoprazole": {
        "cdi_risk": 3,    # WAS 2 (too low). ACG OR 4.81 — highest risk
        "ddi_risk": 2,    # WAS 3. Moderate, CYP3A4 involvement
    },
    "pantoprazole": {
        "cdi_risk": 2,    # WAS 1 (too low). ACG OR 4.15 — also ~4x risk
        "ddi_risk": 1,    # WAS 3 (over-scored). Weak CYP inhibition, sulfotransferase escape
    },
    "rabeprazole": {
        "cdi_risk": 2,    # WAS 2 (unvalidated, no ACG OR data). Default to class median
        "ddi_risk": 1,    # WAS 3 (over-scored). CYP-independent, non-enzymatic metabolism
    }
}

d = json.load(open(DRUGS_JSON, encoding='utf-8'))
drugs = d.get('drugs', d)
assert isinstance(drugs, list), "drugs must be a list"

# Backup
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = BACKUP_DIR / f"drugs_{ts}.json"
shutil.copy2(DRUGS_JSON, backup)
print(f"Backup: {backup}")

# Apply fixes
fixed = 0
for drug in drugs:
    did = drug.get('id', '')
    if did not in CORRECTED:
        continue
    l3 = drug.get('l3_systems', {})
    fixes = CORRECTED[did]
    for field, new_val in fixes.items():
        old_val = l3.get(field)
        l3[field] = new_val
        arrow = 'FIX' if old_val != new_val else 'SAME'
        print(f"  {did}.{field}: {old_val} -> {new_val}  [{arrow}]")
        if old_val != new_val:
            fixed += 1
    drug['l3_systems'] = l3

# Write
with open(DRUGS_JSON, 'w', encoding='utf-8') as f:
    json.dump({"drugs": drugs}, f, indent=2, ensure_ascii=False)

print(f"\nDone. {fixed} values corrected across {len(CORRECTED)} drugs.")
