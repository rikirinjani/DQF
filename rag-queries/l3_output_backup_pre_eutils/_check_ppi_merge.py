import json

d = json.load(open(r'C:\Users\think\Project_v2\drug-quantification-framework\api\drugs.json', encoding='utf-8'))
drugs = d.get('drugs', d)

for item in drugs:
    name = item.get('id', '')
    if 'prazole' in name:
        l3 = item.get('l3_systems', 'MISSING')
        l2 = item.get('l2_score', 'MISSING')
        l1 = item.get('l1_score', 'MISSING')
        overall = item.get('overall_score', 'MISSING')
        if l3 == 'MISSING':
            print(f'{name}: NO l3_systems field')
        else:
            dd = l3.get('ddi_risk', '?')
            cd = l3.get('cdi_risk', '?')
            print(f'{name}: l3_systems present, ddi={dd}, cdi={cd}')
        print(f'  l1={l1} l2={l2} overall={overall}')
        print()
