"""Check all 5 PPI profiles from the re-extraction for filled fields."""
import json

ppi_ids = ['omeprazole','esomeprazole','lansoprazole','pantoprazole','rabeprazole']
fields = ['healing_ability','cyp2c19_metabolism_pct','ddi_risk','cdi_risk','bone_fracture_risk','acid_rebound']

header = f"{'Drug':<15} {'PMID cnt':<9} " + "  ".join(f"{f:<25}" for f in fields)
print(header)
print("-" * len(header))

for p in ppi_ids:
    f = open(r'C:\Users\think\Project_v2\drug-quantification-framework\rag-queries\l3_output\\' + p + '_l3_profile.json', encoding='utf-8')
    d = json.load(f)
    ev = d.get('_evidence', {})
    pmids = len(ev.get('pmids', []))
    vals = []
    for fld in fields:
        val = d.get(fld)
        if val is None:
            vals.append(f"{'null':<25}")
        elif isinstance(val, (int, float)):
            vals.append(f"{str(val):<25}")
        else:
            vals.append(f"{str(val):<25}")
    print(f"{p:<15} {pmids:<9} " + "  ".join(vals))
