import json

ppi_ids = ['omeprazole','esomeprazole','lansoprazole','pantoprazole','rabeprazole']

print("=== L3 Profiles ===")
for p in ppi_ids:
    try:
        f = open(r'C:\Users\think\Project_v2\drug-quantification-framework\rag-queries\l3_output\\' + p + '_l3_profile.json', encoding='utf-8')
        d = json.load(f)
        print(f'{p}:')
        for k,v in d.items():
            if k not in ('_evidence','_note'):
                print(f'  {k}: {v}')
        ev = d.get('_evidence', {})
        print(f'  _evidence.pmids: {len(ev.get("pmids",[]))}')
        print()
    except Exception as e:
        print(f'{p}: ERROR {e}')
        print()

print("=== Drugs.json PPI entries ===")
d = json.load(open(r'C:\Users\think\Project_v2\drug-quantification-framework\api\drugs.json', encoding='utf-8'))
drugs = d.get('drugs', d)
for item in drugs:
    name = item.get('id', item.get('name', ''))
    if name in ppi_ids:
        print(f'{name}:')
        for k in ('l1_score','l2_score','l3_score','l3_meta'):
            print(f'  {k}: {item.get(k, "MISSING")}')
        print()

