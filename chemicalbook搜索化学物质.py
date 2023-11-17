import pandas as pd
import requests
from bs4 import BeautifulSoup

#需要输入headers
headers = {
    'User-Agent': '...'
}

def search_chemical_info(chemical_name):
    url = f'https://www.chemicalbook.com/Search.aspx?keyword={chemical_name}'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data for {chemical_name}. Status code: {response.status_code}")
        return None, None, None, None

    soup = BeautifulSoup(response.text, 'html.parser')

  #mf,mw在表格中，搜索到的第一个一般是需要的
    table = soup.find('table')

    if table:
        chinese_name = get_table_value(table, '中文名称：')
        cas = get_table_value(table, 'CAS：')
        mw = get_table_value(table, 'MW：')
        mf = get_table_value(table, 'MF：')

        return chinese_name, cas, mw, mf

    return None, None, None, None

def get_table_value(table, label):
    td_element = table.find('td', string=label)
    if td_element:
        next_td_element = td_element.find_next('td')
        if next_td_element:
            return next_td_element.text.strip()

    return 'None'

  #文件导入
file_path = r'path'
df = pd.read_excel(file_path, sheet_name='Sheet2')
new_df = pd.DataFrame(columns=['物质', 'CAS', 'MW', 'MF'])

for index, row in df.iterrows():
    chemical_name = row['化合物']
    chinese_name, cas, mw, mf = search_chemical_info(chemical_name)
    
    new_df = new_df.append({'物质': chinese_name, 'CAS': cas, 'MW': mw, 'MF': mf}, ignore_index=True)

# 写入
new_df.to_excel(r'path', index=False)
