import pandas as pd
import requests
import urllib.parse


def search_chemical_info(chemical_name):
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
    properties = ['MolecularFormula',  'MolecularWeight']

    chemical_info = {'物质': chemical_name}

    for prop in properties:
        prop_url = f"{base_url}{urllib.parse.quote(chemical_name)}/property/{prop}/TXT"
        response = requests.get(prop_url)
        
        if response.status_code == 200:
            value = response.text.strip()
            chemical_info[prop] = value
        else:
            print(f"Failed to fetch data for {prop}. Status code: {response.status_code}")

    return chemical_info


#文件遍历行
file_path = r'path'
df = pd.read_excel(file_path,sheet_name='汇总')
new_df = pd.DataFrame(columns=['物质','CAS','MW','MF'])

for index, row in df.iterrows():
    chemical_name = row['化合物'] 
    chemical_info = search_chemical_info(chemical_name)
    new_df = new_df.append({'物质': chemical_name, 'MW': chemical_info.get('MolecularWeight', ''), 'MF': chemical_info.get('MolecularFormula', '')}, ignore_index=True)
                            
# 写入
new_df.to_excel(r'new_path', index=False)
